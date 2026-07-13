"""Shared test fixtures for 3D Mesh Doctor tests."""

import tempfile
from pathlib import Path

import numpy as np
import pytest
import trimesh


@pytest.fixture
def tmp_path_factory():
    """Provide a temporary directory for test outputs."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def sphere_mesh():
    """A simple watertight sphere mesh."""
    return trimesh.creation.icosphere(radius=1.0, subdivisions=3)


@pytest.fixture
def cube_mesh():
    """A simple watertight cube mesh."""
    return trimesh.creation.box(extents=[1, 1, 1])


@pytest.fixture
def cylinder_mesh():
    """A simple watertight cylinder mesh."""
    return trimesh.creation.cylinder(radius=0.5, height=2.0)


@pytest.fixture
def non_watertight_mesh():
    """A mesh with an open edge (not watertight)."""
    # Create a box and remove one face to create a hole
    mesh = trimesh.creation.box(extents=[1, 1, 1])
    # Remove the top face (index 5 in box with 6 faces)
    mask = np.ones(len(mesh.faces), dtype=bool)
    mask[5] = False
    mesh.update_faces(mask)
    return mesh


@pytest.fixture
def non_manifold_mesh():
    """A mesh with non-manifold edges."""
    # Create two triangles sharing an edge (non-manifold)
    vertices = np.array(
        [
            [0, 0, 0],
            [1, 0, 0],
            [0, 1, 0],
            [1, 1, 0],
            [0.5, 0.5, 1],
        ],
        dtype=float,
    )
    # Three triangles all sharing the edge (0,1) - non-manifold
    faces = np.array(
        [
            [0, 1, 2],
            [1, 0, 3],
            [0, 1, 4],
        ]
    )
    return trimesh.Trimesh(vertices=vertices, faces=faces)


@pytest.fixture
def inverted_normals_mesh():
    """A mesh with some inverted face normals."""
    mesh = trimesh.creation.icosphere(radius=1.0, subdivisions=2)
    # Flip normals on first half of faces
    half = len(mesh.faces) // 2
    mesh.faces[:half] = mesh.faces[:half][:, ::-1]
    mesh.fix_normals()
    return mesh


@pytest.fixture
def high_poly_mesh():
    """A higher polygon count mesh for reduction tests."""
    return trimesh.creation.icosphere(radius=1.0, subdivisions=5)


@pytest.fixture
def sample_stl_path(sphere_mesh, tmp_path_factory):
    """Save a watertight sphere as STL and return path."""
    path = tmp_path_factory / "sphere.stl"
    sphere_mesh.export(str(path))
    return path


@pytest.fixture
def sample_obj_path(cube_mesh, tmp_path_factory):
    """Save a watertight cube as OBJ and return path."""
    path = tmp_path_factory / "cube.obj"
    cube_mesh.export(str(path))
    return path


@pytest.fixture
def broken_stl_path(non_watertight_mesh, tmp_path_factory):
    """Save a non-watertight mesh as STL and return path."""
    path = tmp_path_factory / "broken.stl"
    non_watertight_mesh.export(str(path))
    return path
