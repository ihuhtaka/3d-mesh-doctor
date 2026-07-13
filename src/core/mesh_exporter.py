"""Mesh export to STL and OBJ formats."""

from pathlib import Path

import trimesh


def export_mesh(mesh: trimesh.Trimesh, path: str | Path, file_type: str | None = None) -> Path:
    """Export a mesh to a file.

    Parameters
    ----------
    mesh : trimesh.Trimesh
        The mesh to export.
    path : str or Path
        Output file path.
    file_type : str, optional
        File type override (e.g., 'stl', 'obj'). Inferred from extension if None.

    Returns
    -------
    Path
        The path to the exported file.
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    if file_type is None:
        file_type = path.suffix.lstrip(".")

    mesh.export(str(path), file_type=file_type)
    return path
