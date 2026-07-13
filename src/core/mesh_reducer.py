"""Mesh polygon reduction via quadric decimation."""

import trimesh


def reduce_polygons(
    mesh: trimesh.Trimesh, target_face_count: int | None = None, ratio: float | None = None
) -> trimesh.Trimesh:
    """Reduce polygon count while preserving shape.

    Parameters
    ----------
    mesh : trimesh.Trimesh
        The mesh to simplify (modified in-place).
    target_face_count : int, optional
        Exact target number of faces.
    ratio : float, optional
        Target ratio of faces (0.0-1.0). E.g., 0.5 = reduce to 50%.

    Returns
    -------
    trimesh.Trimesh
        The simplified mesh.
    """
    original_count = len(mesh.faces)

    if ratio is not None:
        ratio = max(0.01, min(1.0, ratio))
        if ratio < 1.0:
            mesh = mesh.simplify_quadric_decimation(percent=ratio)
    elif target_face_count is not None:
        target_face_count = max(1, min(original_count, target_face_count))
        if target_face_count < original_count:
            mesh = mesh.simplify_quadric_decimation(face_count=target_face_count)

    return mesh
