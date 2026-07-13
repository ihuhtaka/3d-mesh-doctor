"""Tests for mesh_reducer module."""

import trimesh

from src.core.mesh_reducer import reduce_polygons


class TestMeshReducer:
    """Tests for mesh polygon reduction functions."""

    def test_reduce_by_ratio(self, high_poly_mesh):
        """Test reducing polygon count by ratio."""
        original_count = len(high_poly_mesh.faces)
        reduced = reduce_polygons(high_poly_mesh, ratio=0.5)
        assert len(reduced.faces) < original_count
        assert len(reduced.faces) > 0

    def test_reduce_by_target_count(self, high_poly_mesh):
        """Test reducing to a specific face count."""
        target = 100
        reduced = reduce_polygons(high_poly_mesh, target_face_count=target)
        assert len(reduced.faces) <= target

    def test_reduce_no_change_if_already_small(self, cube_mesh):
        """Test that reduction doesn't happen if already below target."""
        original_count = len(cube_mesh.faces)
        reduced = reduce_polygons(cube_mesh, target_face_count=20)
        # Should not reduce below original since target is higher
        assert len(reduced.faces) == original_count

    def test_reduce_preserves_shape(self, sphere_mesh):
        """Test that reduction roughly preserves shape."""
        reduced = reduce_polygons(sphere_mesh, ratio=0.5)
        # Volume should still be positive and roughly similar
        assert reduced.volume > 0
        assert reduced.area > 0

    def test_reduce_min_ratio(self, high_poly_mesh):
        """Test that very low ratios are clamped."""
        reduced = reduce_polygons(high_poly_mesh, ratio=0.001)
        # Should have at least 1 face
        assert len(reduced.faces) >= 1

    def test_reduce_max_ratio(self, high_poly_mesh):
        """Test that ratio > 1 doesn't change mesh."""
        original_count = len(high_poly_mesh.faces)
        reduced = reduce_polygons(high_poly_mesh, ratio=1.5)
        assert len(reduced.faces) == original_count

    def test_reduce_returns_trimesh(self, sphere_mesh):
        """Test that reduction returns a Trimesh object."""
        reduced = reduce_polygons(sphere_mesh, ratio=0.5)
        assert isinstance(reduced, trimesh.Trimesh)

    def test_reduce_no_params(self, sphere_mesh):
        """Test that no parameters returns original mesh."""
        original_count = len(sphere_mesh.faces)
        reduced = reduce_polygons(sphere_mesh)
        assert len(reduced.faces) == original_count
