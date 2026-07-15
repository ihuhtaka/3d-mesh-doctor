# 3D Mesh Doctor

Python GUI and CLI tool for repairing, smoothing, and optimizing 3D meshes and scans for 3D printing.

Built with **PySide6** + **PyVista** for interactive 3D visualization, and **trimesh** for mesh processing.

## Features

### Mesh Repair
- Fill holes in non-watertight meshes
- Fix inverted normals
- Remove degenerate faces
- Detect non-manifold edges
- Watertight analysis with boundary edge highlighting

### Smoothing
- **Laplacian** — standard smoothing (may shrink volume)
- **Taubin** — anti-shrinkage smoothing (preserves volume)
- **Humphrey** — alternative anti-shrinkage method
- Adjustable iterations (1–100) and strength (0.0–1.0)

### Polygon Reduction
- Quadric decimation for best shape preservation
- Configurable reduction ratio (5%–100%)
- Preview before applying

### Quality Metrics
- Volume difference (%)
- Surface area difference (%)
- Roughness (area / convex hull area)
- Hausdorff distance (max vertex-to-surface)
- Chamfer distance (mean vertex-to-surface)

### Distortion Visualization
- Color-mapped overlay showing per-vertex distance to original mesh
- Configurable symmetric limit (in micrometers) with clamped saturation
- Live update when adjusting the limit

### GUI Features
- 3D interactive viewer with PyVista
- Camera position preserved during processing
- Drag-and-drop file loading
- View menu to toggle panel visibility
- Batch export support

## Installation

### Prerequisites

- Python 3.10 or later
- A display server (X11, Wayland, or macOS)

### Setup

```bash
# Clone the repository
git clone https://github.com/ihuhtaka/3d-mesh-doctor.git
cd 3d-mesh-doctor

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
# .venv\Scripts\activate    # Windows

# Install dependencies
pip install -r requirements.txt

# Install in editable mode (for CLI entry points)
pip install -e .
```

### Dev Dependencies

```bash
pip install pytest pytest-cov ruff
```

## Usage

### GUI

```bash
python -m src.main
```

Or after installation:

```bash
mesh-doctor
```

### CLI

#### Analyze a single mesh

```bash
mesh-doctor-cli analyze scan.stl
```

Output:

```
File: scan.stl
  Faces: 45,230
  Vertices: 22,615
  Volume: 12.3456
  Area: 28.7890
  Roughness: 1.023
```

#### Batch process a directory

```bash
mesh-doctor-cli batch ./scans/ -o ./repaired/ --format stl \
  --fill-holes --fix-normals --remove-degenerate
```

#### Full pipeline with smoothing and reduction

```bash
mesh-doctor-cli batch ./scans/ -o ./repaired/ --format obj \
  --fill-holes --fix-normals --remove-degenerate \
  --smooth taubin -i 15 -s 0.4 \
  --reduce 50
```

#### Analyze only (no repair/export)

```bash
mesh-doctor-cli batch ./scans/ -o ./output/ --analyze-only
```

### CLI Reference

```
mesh-doctor-cli {batch,analyze} [options]

batch:
  input                   Input directory with mesh files
  -o, --output DIR        Output directory (required)
  --format {stl,obj}      Output format (default: stl)

  Repair options:
    --fill-holes          Fill holes
    --fix-normals         Fix inverted normals
    --remove-degenerate   Remove degenerate faces

  Smoothing options:
    --smooth {laplacian,taubin,humphrey}
    -i, --smooth-iterations N   (default: 10)
    -s, --smooth-strength F     (default: 0.5, range: 0.0-1.0)

  Reduction:
    --reduce N            Reduce to N% of faces

  Other:
    --analyze-only        Analyze only, no repair/export

analyze:
  file                    Mesh file to analyze
```

## Example Meshes

The `scans/` directory contains example meshes with known issues for testing:

| File | Issue | Use for |
|------|-------|---------|
| `sphere_with_holes.stl` | 3 circular holes cut out (non-watertight) | Repair / hole filling |
| `torus_high_poly.stl` | 2048 faces, clean geometry | Polygon reduction |
| `cube_inverted_normals.stl` | Top face normals flipped | Normal repair |
| `ear_canal.stl` | Tapered tube, open ends (non-watertight) | Real-world scan shape |
| `bumpy_sphere.stl` | Surface noise on a sphere | Smoothing |
| `overlapping_cubes.stl` | Two intersecting cubes | Non-manifold edges |

Try them:

```bash
# Analyze an example
mesh-doctor-cli analyze scans/sphere_with_holes.stl

# Repair and export
mesh-doctor-cli batch scans/ -o output/ --fill-holes --fix-normals --format stl

# Full pipeline: repair + smooth + reduce
mesh-doctor-cli batch scans/ -o output/ \
  --fill-holes --fix-normals --remove-degenerate \
  --smooth taubin -i 10 -s 0.5 \
  --reduce 50
```

## Development

### Project Structure

```
src/
  core/                   Pure mesh processing (no GUI dependencies)
    mesh_loader.py        STL/OBJ loading via trimesh
    mesh_analyzer.py      Watertight checks, hole/non-manifold detection
    mesh_repairer.py      Hole filling, normal fixing, degenerate removal
    mesh_smoother.py      Laplacian/Taubin/Humphrey smoothing
    mesh_reducer.py       Quadric decimation polygon reduction
    mesh_metrics.py       Quality comparison metrics
    mesh_exporter.py      STL/OBJ export
  gui/                    PySide6 GUI
    main_window.py        Main application window
    viewer_widget.py      PyVista 3D viewer
    file_panel.py         File list with drag-and-drop
    repair_panel.py       Repair analysis and controls
    smoothing_panel.py    Smoothing method and parameters
    reduction_panel.py    Reduction ratio and distortion visualization
    export_panel.py       Format selection and export
  batch/
    processor.py          QThread-based batch processor
  cli.py                  CLI entry point
  main.py                 GUI entry point
scans/                    Example meshes with known issues
tests/
  conftest.py             Test fixtures (sphere, cube, cylinder, etc.)
  test_mesh_loader.py     6 tests
  test_mesh_analyzer.py   7 tests
  test_mesh_repairer.py   7 tests
  test_mesh_smoother.py   7 tests
  test_mesh_reducer.py    8 tests
  test_mesh_exporter.py   6 tests
```

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=src

# Run a specific test module
pytest tests/test_mesh_repairer.py -v
```

### Linting

```bash
# Check for issues
ruff check src/ tests/

# Auto-fix issues
ruff check --fix src/ tests/

# Format code
ruff format src/ tests/
```

### Supported Formats

- **Input:** STL, OBJ
- **Output:** STL, OBJ

## License

MIT
