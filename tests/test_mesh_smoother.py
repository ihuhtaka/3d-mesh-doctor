"""Tests for mesh_smoother module."""

import numpy as np
import trimesh

from src.core.mesh_smoother import SmoothMethod, smooth_mesh


class TestMeshSmoother:
    """Tests for mesh smoothing functions."""

    def test_smooth_laplacian(self, sphere_mesh):
        """Test Laplacian smoothing."""
        original_vertices = sphere_mesh.vertices.copy()
        smoothed = smooth_mesh(
            sphere_mesh,
            method=SmoothMethod.LAPLACIAN,
            iterations=5,
            lambd=0.3,
        )
        assert isinstance(smoothed, trimesh.Trimesh)
        # Vertices should have changed
        assert not np.allclose(smoothed.vertices, original_vertices)

    def test_smooth_taubin(self, sphere_mesh):
        """Test Taubin smoothing (preserves volume better)."""
        original_volume = sphere_mesh.volume
        smoothed = smooth_mesh(
            sphere_mesh,
            method=SmoothMethod.TAUBIN,
            iterations=10,
            lambd=0.5,
            mu=0.5,
        )
        assert isinstance(smoothed, trimesh.Trimesh)
        # Taubin should preserve volume better than Laplacian
        volume_change = abs(smoothed.volume - original_volume) / original_volume
        assert volume_change < 0.2  # Should preserve most volume

    def test_smooth_humphrey(self, sphere_mesh):
        """Test Humphrey smoothing."""
        smoothed = smooth_mesh(
            sphere_mesh,
            method=SmoothMethod.HUMPHREY,
            iterations=5,
            lambd=0.5,
            mu=0.5,
        )
        assert isinstance(smoothed, trimesh.Trimesh)

    def test_smooth_iterations_clamped(self, sphere_mesh):
        """Test that iterations are clamped to valid range."""
        # Should not raise, even with extreme values
        smoothed = smooth_mesh(
            sphere_mesh,
            method=SmoothMethod.LAPLACIAN,
            iterations=200,  # Should be clamped to 100
            lambd=0.5,
        )
        assert isinstance(smoothed, trimesh.Trimesh)

    def test_smooth_strength_clamped(self, sphere_mesh):
        """Test that strength is clamped to 0-1 range."""
        smoothed = smooth_mesh(
            sphere_mesh,
            method=SmoothMethod.LAPLACIAN,
            iterations=5,
            lambd=2.0,  # Should be clamped to 1.0
        )
        assert isinstance(smoothed, trimesh.Trimesh)

    def test_smooth_preserves_face_count(self, sphere_mesh):
        """Test that smoothing doesn't change face count."""
        original_face_count = len(sphere_mesh.faces)
        smoothed = smooth_mesh(
            sphere_mesh,
            method=SmoothMethod.TAUBIN,
            iterations=10,
        )
        assert len(smoothed.faces) == original_face_count

    def test_smooth_preserves_vertex_count(self, sphere_mesh):
        """Test that smoothing doesn't change vertex count."""
        original_vertex_count = len(sphere_mesh.vertices)
        smoothed = smooth_mesh(
            sphere_mesh,
            method=SmoothMethod.LAPLACIAN,
            iterations=10,
        )
        assert len(smoothed.vertices) == original_vertex_count

    def test_smooth_method_enum(self):
        """Test that all smoothing methods are available."""
        assert SmoothMethod.LAPLACIAN.value == "laplacian"
        assert SmoothMethod.TAUBIN.value == "taubin"
        assert SmoothMethod.HUMPHREY.value == "humphrey"
