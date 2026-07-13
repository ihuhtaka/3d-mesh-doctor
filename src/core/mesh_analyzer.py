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
    is_watertight = mesh.is_watertight
    face_count = len(mesh.faces)
    vertex_count = len(mesh.vertices)
    volume = mesh.volume if is_watertight else 0.0
    surface_area = mesh.area
    has_inverted_normals = bool(np.any(mesh.face_normals[:, 2] < 0))

    # Detect boundary edges (holes) using edges_sorted
    hole_count = 0
    hole_edges_list: list = []
    non_manifold_edge_count = 0
    non_manifold_edges_list: list = []

    if face_count > 0:
        edges_sorted = mesh.edges_sorted
        unique_edges, counts = np.unique(edges_sorted, axis=0, return_counts=True)
        # Boundary edges appear exactly once
        boundary_mask = counts == 1
        boundary_edges = unique_edges[boundary_mask]
        hole_count = len(boundary_edges) // 2 if len(boundary_edges) > 0 else 0
        hole_edges_list = boundary_edges.tolist()

        # Non-manifold edges appear more than twice
        non_manifold_mask = counts > 2
        non_manifold_edge_count = int(np.sum(non_manifold_mask))
        non_manifold_edges_list = unique_edges[non_manifold_mask].tolist()

    return MeshReport(
        is_watertight=is_watertight,
        face_count=face_count,
        vertex_count=vertex_count,
        volume=volume,
        surface_area=surface_area,
        has_inverted_normals=has_inverted_normals,
        non_manifold_edge_count=non_manifold_edge_count,
        hole_count=hole_count,
        hole_edges=hole_edges_list,
        non_manifold_edges=non_manifold_edges_list,
    )
