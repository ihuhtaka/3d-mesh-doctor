# AGENTS.md

## Project

**3D Mesh Doctor** — Python GUI tool (PySide6 + PyVista) that opens head scans (STL/OBJ), checks mesh watertightness, repairs holes/non-manifold edges, smooths, reduces polygon count, and exports for 3D printing. Supports batch processing.

GitHub: https://github.com/ihuhtaka/3d-mesh-doctor

## Architecture

- `src/core/` — Pure mesh processing (no GUI deps): loader, analyzer, repairer, smoother, reducer, exporter
- `src/gui/` — PySide6 GUI: main window, PyVista 3D viewer, file panel, repair/smoothing/export panels
- `src/batch/` — Background batch processing via QThread
- `tests/` — pytest tests (fixtures in `tests/fixtures/`)

## Dev Commands

```bash
# Setup
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pip install pytest pytest-cov ruff

# Run
python -m src.main

# Test
pytest tests/ -v
pytest tests/ -v --cov=src

# Lint
ruff check src/ tests/
ruff format src/ tests/
```

## Conventions

- Follow PEP 8, enforced by ruff
- Use virtual environments
- Modular code: `src/core/` has zero GUI imports
- Robust error handling with informative messages
- Unit tests required for all `src/core/` functionality

## Stack

- Python 3.10+, PySide6, PyVista + pyvistaqt, trimesh[easy], scipy, numpy
