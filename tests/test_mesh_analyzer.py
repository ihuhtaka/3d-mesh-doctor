"""Tests for mesh_analyzer module."""


from src.core.mesh_analyzer import MeshReport, analyze_mesh


class TestMeshAnalyzer:
    """Tests for mesh analysis functions."""

    def test_analyze_watertight_sphere(self, sphere_mesh):
        """Test analysis of a watertight sphere."""
        report = analyze_mesh(sphere_mesh)
        assert isinstance(report, MeshReport)
        assert report.is_watertight is True
        assert report.face_count > 0
        assert report.vertex_count > 0
        assert report.volume > 0
        assert report.surface_area > 0

    def test_analyze_watertight_cube(self, cube_mesh):
        """Test analysis of a watertight cube."""
        report = analyze_mesh(cube_mesh)
        assert report.is_watertight is True
        assert report.face_count == 12  # Cube has 12 triangles
        assert report.vertex_count == 8

    def test_analyze_non_watertight(self, non_watertight_mesh):
        """Test analysis of a non-watertight mesh."""
        report = analyze_mesh(non_watertight_mesh)
        assert report.is_watertight is False
        assert report.hole_count > 0

    def test_analyze_non_manifold(self, non_manifold_mesh):
        """Test analysis of a non-manifold mesh."""
        report = analyze_mesh(non_manifold_mesh)
        # Non-manifold meshes may or may not be watertight
        assert report.face_count == 3
        assert report.vertex_count == 5

    def test_volume_only_for_watertight(self, non_watertight_mesh):
        """Test that volume is 0 for non-watertight meshes."""
        report = analyze_mesh(non_watertight_mesh)
        assert report.volume == 0.0

    def test_surface_area_positive(self, sphere_mesh):
        """Test that surface area is always positive."""
        report = analyze_mesh(sphere_mesh)
        assert report.surface_area > 0

    def test_report_fields(self, sphere_mesh):
        """Test that all report fields are populated."""
        report = analyze_mesh(sphere_mesh)
        assert isinstance(report.is_watertight, bool)
        assert isinstance(report.face_count, int)
        assert isinstance(report.vertex_count, int)
        assert isinstance(report.volume, float)
        assert isinstance(report.surface_area, float)
        assert isinstance(report.has_inverted_normals, bool)
        assert isinstance(report.non_manifold_edge_count, int)
        assert isinstance(report.hole_count, int)
        assert isinstance(report.hole_edges, list)
        assert isinstance(report.non_manifold_edges, list)
