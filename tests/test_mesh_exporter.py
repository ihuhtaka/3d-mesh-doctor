"""Tests for mesh_exporter module."""

import trimesh

from src.core.mesh_exporter import export_mesh


class TestMeshExporter:
    """Tests for mesh export functions."""

    def test_export_stl(self, sphere_mesh, tmp_path_factory):
        """Test exporting to STL format."""
        path = tmp_path_factory / "output.stl"
        result = export_mesh(sphere_mesh, path)
        assert result.exists()
        assert result.suffix == ".stl"
        # Verify the exported file can be loaded
        loaded = trimesh.load(str(result))
        assert isinstance(loaded, trimesh.Trimesh)
        assert len(loaded.faces) == len(sphere_mesh.faces)

    def test_export_obj(self, cube_mesh, tmp_path_factory):
        """Test exporting to OBJ format."""
        path = tmp_path_factory / "output.obj"
        result = export_mesh(cube_mesh, path)
        assert result.exists()
        assert result.suffix == ".obj"
        loaded = trimesh.load(str(result))
        assert isinstance(loaded, trimesh.Trimesh)

    def test_export_creates_directory(self, sphere_mesh, tmp_path_factory):
        """Test that export creates parent directories."""
        path = tmp_path_factory / "subdir" / "nested" / "output.stl"
        result = export_mesh(sphere_mesh, path)
        assert result.exists()

    def test_export_with_explicit_type(self, sphere_mesh, tmp_path_factory):
        """Test export with explicit file_type parameter."""
        path = tmp_path_factory / "output.stl"
        result = export_mesh(sphere_mesh, path, file_type="stl")
        assert result.exists()

    def test_export_preserves_mesh(self, sphere_mesh, tmp_path_factory):
        """Test that export doesn't modify the original mesh."""
        original_faces = len(sphere_mesh.faces)
        original_vertices = len(sphere_mesh.vertices)
        path = tmp_path_factory / "output.stl"
        export_mesh(sphere_mesh, path)
        assert len(sphere_mesh.faces) == original_faces
        assert len(sphere_mesh.vertices) == original_vertices

    def test_export_returns_path(self, sphere_mesh, tmp_path_factory):
        """Test that export returns the output path."""
        path = tmp_path_factory / "output.stl"
        result = export_mesh(sphere_mesh, path)
        assert result == path
