"""Mesh analysis — watertight checks, issue detection, statistics."""

from dataclasses import dataclass, field

import numpy as np
import trimesh


@dataclass
class MeshReport:
    """Results of mesh analysis."""

    is_watertight: bool
    face_count: int
    vertex_count: int
    volume: float
    surface_area: float
    has_inverted_normals: bool
    non_manifold_edge_count: int
    hole_count: int
    hole_edges: list = field(default_factory=list)
    non_manifold_edges: list = field(default_factory=list)


def analyze_mesh(mesh: trimesh.Trimesh) -> MeshReport:
    """Analyze a mesh for issues and compute statistics.

    Parameters
    ----------
    mesh : trimesh.Trimesh
        The mesh to analyze.

    Returns
    -------
    MeshReport
        Analysis results.
    """
    # Watertight check
    is_watertight = mesh.is_watertight

    # Face and vertex counts
    face_count = len(mesh.faces)
    vertex_count = len(mesh.vertices)

    # Volume and surface area (only meaningful for watertight meshes)
    volume = mesh.volume if is_watertight else 0.0
    surface_area = mesh.area

    # Inverted normals
    has_inverted_normals = bool(np.any(mesh.face_normals[:, 2] < 0))

    # Non-manifold edges: edges shared by != 2 faces
    edge_face_count = mesh.edges_face
    unique_edges, counts = np.unique(edge_face_count, axis=0, return_counts=True)
    # edges_face gives face pairs; non-manifold if an edge index appears > 2 times
    # Actually, let's use trimesh's built-in checks
    non_manifold_edge_count = int(
        np.sum(mesh.edges_face[:, 1] == -1) if mesh.edges_face.shape[1] > 1 else 0
    )

    # Holes: boundary edges (edges with only one adjacent face)
    holes = 0
    hole_edges_list: list = []
    non_manifold_edges_list: list = []

    if hasattr(mesh, "edges_sorted") and hasattr(mesh, "faces"):
        # Count edges shared by only one face = boundary edges = holes
        edges_sorted = mesh.edges_sorted
        # Find edges that appear only once (boundary)
        unique, counts = np.unique(edges_sorted, axis=0, return_counts=True)
        boundary_mask = counts == 1
        boundary_edges = unique[boundary_mask]
        holes = len(boundary_edges) // 2 if len(boundary_edges) > 0 else 0
        hole_edges_list = boundary_edges.tolist()

    return MeshReport(
        is_watertight=is_watertight,
        face_count=face_count,
        vertex_count=vertex_count,
        volume=volume,
        surface_area=surface_area,
        has_inverted_normals=has_inverted_normals,
        non_manifold_edge_count=non_manifold_edge_count,
        hole_count=holes,
        hole_edges=hole_edges_list,
        non_manifold_edges=non_manifold_edges_list,
    )
