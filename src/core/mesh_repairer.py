"""Mesh repair — fill holes, fix normals, remove degenerate geometry."""

from dataclasses import dataclass

import trimesh


@dataclass
class RepairOptions:
    """Options for mesh repair."""

    fill_holes: bool = True
    fix_normals: bool = True
    remove_degenerate: bool = True
    merge_vertices: bool = True
    remove_duplicates: bool = True


def repair_mesh(
    mesh: trimesh.Trimesh, options: RepairOptions | None = None
) -> trimesh.Trimesh:
    """Repair a mesh by filling holes, fixing normals, and cleaning geometry.

    Parameters
    ----------
    mesh : trimesh.Trimesh
        The mesh to repair (modified in-place).
    options : RepairOptions, optional
        Repair settings. Defaults to all fixes enabled.

    Returns
    -------
    trimesh.Trimesh
        The repaired mesh (same object, modified in-place).
    """
    if options is None:
        options = RepairOptions()

    if options.remove_duplicates:
        mesh.remove_duplicate_faces()
        mesh.remove_unreferenced_vertices()

    if options.merge_vertices:
        mesh.merge_vertices()

    if options.remove_degenerate:
        mesh.remove_degenerate_faces()

    if options.fix_normals:
        mesh.fix_normals()

    if options.fill_holes:
        trimesh.repair.fill_holes(mesh)

    return mesh
