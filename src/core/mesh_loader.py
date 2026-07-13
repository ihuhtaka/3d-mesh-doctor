"""Mesh loading for STL and OBJ files."""

from pathlib import Path

import trimesh


SUPPORTED_EXTENSIONS = {".stl", ".obj"}


def load_mesh(path: str | Path) -> trimesh.Trimesh:
    """Load a mesh from an STL or OBJ file.

    Parameters
    ----------
    path : str or Path
        Path to the mesh file.

    Returns
    -------
    trimesh.Trimesh
        The loaded mesh.

    Raises
    ------
    FileNotFoundError
        If the file does not exist.
    ValueError
        If the file extension is not supported.
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
        raise ValueError(
            f"Unsupported format '{path.suffix}'. Supported: {SUPPORTED_EXTENSIONS}"
        )
    mesh = trimesh.load(path, force="mesh")
    if not isinstance(mesh, trimesh.Trimesh):
        raise ValueError(f"Could not load mesh from {path}")
    return mesh
