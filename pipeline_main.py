#!/usr/bin/env python3
"""
Photogrammetry Pipeline - End-to-End Orchestration Script

This script demonstrates a full photogrammetric workflow:
1. Generate synthetic cameras and 2D observations (once)
2. Run spatial intersection to obtain initial 3D points
3. Adapt and feed results into bundle adjustment for refinement
4. Visualize and summarize both stages

"""

import sys
import traceback
import numpy as np

# --- Spatial Intersection Tool Imports ---
from Spatial_Intersection_Tool.src.data.io_utils import create_synthetic_dataset as create_synthetic_si_dataset
from Spatial_Intersection_Tool.src.core.spatial_intersection import run_spatial_intersection, compute_triangulation_quality
from Spatial_Intersection_Tool.src.visualizations.plot_intersections import plot_3d_scene
from Spatial_Intersection_Tool.src.visualizations.plot_summary import print_intersection_summary

# --- Bundle Adjustment Tool Imports ---
from bundle_adjustment.src.data.observations import BundleAdjustmentData, Observation
from bundle_adjustment.src.core.residuals import compute_reprojection_error
from bundle_adjustment.src.solvers.sparse_lm_solver import SparseLMSolver
from bundle_adjustment.src.visualizations.plot_cameras import plot_cameras_and_points


def main():
    print("=" * 70)
    print("Photogrammetry Pipeline: Spatial Intersection ➔ Bundle Adjustment")
    print("=" * 70)

    try:
        # 1️⃣ Generate Synthetic Data (Once)
        print("\n[1] Generating synthetic dataset for spatial intersection...")
        si_data = create_synthetic_si_dataset(num_cameras=5, num_points=50, noise_std=1.0, random_seed=42)
        print(f"  Cameras: {len(si_data.camera_poses)} | Observations: {len(si_data.points_2d)}")

        # 2️⃣ Run Spatial Intersection
        print("\n[2] Running spatial intersection...")
        points_3d_initial = run_spatial_intersection(si_data)
        si_quality = compute_triangulation_quality(si_data, points_3d_initial)
        print_intersection_summary(points_3d_initial, np.array([]), title="Spatial Intersection Summary")
        plot_3d_scene(si_data.camera_poses, points_3d_initial, title="Spatial Intersection: 3D Points")
        print("  [✓] Spatial Intersection completed.")

        # 3️⃣ Adapt Data for Bundle Adjustment
        print("\n[3] Adapting data for bundle adjustment...")
        # Convert SpatialIntersectionData observations to BA Observations if needed
        ba_observations = []
        for obs in si_data.points_2d:
            # BundleAdjustmentData expects Observation with camera_index, point_index, image_point
            ba_observations.append(Observation(
                camera_index=obs.camera_index,
                point_index=obs.point_index,
                image_point=obs.location
            ))
        # Construct BundleAdjustmentData
        ba_data = BundleAdjustmentData(
            camera_poses=si_data.camera_poses,
            points_3d=points_3d_initial,
            observations=ba_observations,
            camera_model=si_data.camera_model
        )
        print(f"  Cameras: {len(ba_data.camera_poses)} | Observations: {len(ba_data.observations)} | Initial 3D points: {ba_data.points_3d.shape[0]}")

        # 4️⃣ Run Bundle Adjustment
        print("\n[4] Running bundle adjustment...")
        solver = SparseLMSolver(
            data=ba_data,
            max_iterations=15,
            initial_damping=1.0,
            damping_factor=10.0,
            convergence_threshold=1e-6
        )
        optimized_camera_poses, optimized_points_3d, final_residual_norm = solver.run()
        print(f"  [✓] Bundle Adjustment completed. Final residual norm: {final_residual_norm:.3f}")

        # 5️⃣ Visualization and Comparison
        print("\n[5] Visualizing results...")
        print("  [A] Initial intersection points:")
        plot_3d_scene(si_data.camera_poses, points_3d_initial, title="Initial 3D Points (Spatial Intersection)")
        print("  [B] Refined points after bundle adjustment:")
        plot_cameras_and_points(optimized_camera_poses, optimized_points_3d, title="Refined 3D Points (Bundle Adjustment)")

        # 6️⃣ Summary and Improvement
        print("\n[6] Pipeline Summary:")
        initial_reproj_error = compute_reprojection_error(ba_data, ba_data.camera_poses, ba_data.points_3d)
        final_reproj_error = compute_reprojection_error(ba_data, optimized_camera_poses, optimized_points_3d)
        print(f"  Initial mean reprojection error: {initial_reproj_error:.3f} px")
        print(f"  Final mean reprojection error: {final_reproj_error:.3f} px")
        print(f"  Improvement: {initial_reproj_error - final_reproj_error:.3f} px")
        print("\nPipeline completed successfully.")

        # --- Future Integration Point ---
        # To use real data, replace synthetic dataset creation with I/O from COLMAP or other sources.
        # Pass outputs from spatial intersection directly into bundle adjustment for real-world workflows.

    except Exception as e:
        print("\n[ERROR] Pipeline failed:")
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main() 