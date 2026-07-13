"""Tests for mesh_loader module."""

import pytest
import trimesh

from src.core.mesh_loader import SUPPORTED_EXTENSIONS, load_mesh


class TestLoadMesh:
    """Tests for the load_mesh function."""

    def test_load_stl(self, sample_stl_path):
        """Test loading an STL file."""
        mesh = load_mesh(sample_stl_path)
        assert isinstance(mesh, trimesh.Trimesh)
        assert len(mesh.vertices) > 0
        assert len(mesh.faces) > 0

    def test_load_obj(self, sample_obj_path):
        """Test loading an OBJ file."""
        mesh = load_mesh(sample_obj_path)
        assert isinstance(mesh, trimesh.Trimesh)
        assert len(mesh.vertices) > 0
        assert len(mesh.faces) > 0

    def test_file_not_found(self):
        """Test that FileNotFoundError is raised for missing files."""
        with pytest.raises(FileNotFoundError, match="File not found"):
            load_mesh("/nonexistent/path/file.stl")

    def test_unsupported_extension(self, tmp_path_factory):
        """Test that ValueError is raised for unsupported formats."""
        unsupported = tmp_path_factory / "model.txt"
        unsupported.write_text("not a mesh")
        with pytest.raises(ValueError, match="Unsupported format"):
            load_mesh(unsupported)

    def test_supported_extensions(self):
        """Test that expected extensions are supported."""
        assert ".stl" in SUPPORTED_EXTENSIONS
        assert ".obj" in SUPPORTED_EXTENSIONS

    def test_load_returns_trimesh(self, sphere_mesh, tmp_path_factory):
        """Test that loaded mesh is a proper Trimesh object."""
        path = tmp_path_factory / "test.stl"
        sphere_mesh.export(str(path))
        mesh = load_mesh(path)
        assert hasattr(mesh, "vertices")
        assert hasattr(mesh, "faces")
        assert hasattr(mesh, "is_watertight")
