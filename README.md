# 📐 Photogrammetry Pipeline

A modular pipeline combining spatial intersection and bundle adjustment to compute and refine 3D point positions from 2D observations and camera poses. Supports both **synthetic datasets** for validation and **real photogrammetric datasets** (e.g., COLMAP exports).

---

## 🚩 Purpose

This repository orchestrates the two core stages of a photogrammetric pipeline:

1. **Spatial Intersection:** Computes initial 3D points from camera poses and 2D observations.
2. **Bundle Adjustment:** Refines both camera poses and 3D points to minimize reprojection errors.

Both stages are implemented as submodules:
- [`bundle_adjustment/`](./bundle_adjustment) — Bundle Adjustment Tool
- [`Spatial_Intersection_Tool/`](./Spatial_Intersection_Tool) — Spatial Intersection Tool

---

## 📊 Key Features
- End-to-end photogrammetric pipeline (intersection ➔ refinement)
- Supports synthetic and real datasets (COLMAP exports)
- Consistent data structures between stages
- Modular, extensible codebase
- Visualization tools for 3D points, camera poses, and error diagnostics

---

## 📂 Repository Structure

```
Photogrammetry_Pipeline/
├─ bundle_adjustment/           # Submodule: Bundle Adjustment Tool
├─ Spatial_Intersection_Tool/   # Submodule: Spatial Intersection Tool
├─ pipeline_main.py             # Orchestrates both tools
└─ .gitmodules                  # Submodule configuration
```

---

## 🚀 Usage

### 1️⃣ Synthetic Data Example (`pipeline_main.py`)
Demonstrates seamless handoff between tools using synthetic data.

```bash
python pipeline_main.py
```

### 2️⃣ Real Data Example (COLMAP)
Run Spatial Intersection first:

```bash
python Spatial_Intersection_Tool/src/main.py --dataset colmap --images_txt path/to/images.txt --points3D_txt path/to/points3D.txt
```

Then feed outputs into Bundle Adjustment by adapting your inputs in `pipeline_main.py` or separately via the CLI:

```bash
python bundle_adjustment/src/main.py --dataset colmap --images_txt ... --points3D_txt ...
```

---

## 📈 Outputs
- 3D plots (cameras, rays, points)
- Reprojection error histograms
- Console summaries of intersection and adjustment results

---

## 🔮 Future Extensions
- Robust intersection (RANSAC) for noisy observations
- Control point integration for georeferencing
- Integration with SfM outputs from OpenMVG, Metashape

---

## 🤝 Acknowledgments
Built on top of the separately maintained:
- [Bundle Adjustment Tool](./bundle_adjustment)
- [Spatial Intersection Tool](./Spatial_Intersection_Tool)

Both tools share consistent conventions and data structures for easy interoperability.

---

*For photogrammetry, computer vision, and educational use.* 