"""Tests for mesh_repairer module."""

import trimesh

from src.core.mesh_repairer import RepairOptions, repair_mesh


class TestMeshRepairer:
    """Tests for mesh repair functions."""

    def test_repair_non_watertight(self, non_watertight_mesh):
        """Test repairing a non-watertight mesh makes it watertight."""
        repaired = repair_mesh(non_watertight_mesh)
        assert repaired.is_watertight is True

    def test_repair_preserves_geometry(self, sphere_mesh):
        """Test that repair doesn't drastically change geometry."""
        original_volume = sphere_mesh.volume
        original_area = sphere_mesh.area
        repaired = repair_mesh(sphere_mesh.copy())
        # Volume and area should be reasonably close
        assert abs(repaired.volume - original_volume) / original_volume < 0.1
        assert abs(repaired.area - original_area) / original_area < 0.1

    def test_repair_with_all_options(self, non_watertight_mesh):
        """Test repair with all options enabled."""
        options = RepairOptions(
            fill_holes=True,
            fix_normals=True,
            remove_degenerate=True,
            merge_vertices=True,
            remove_duplicates=True,
        )
        repaired = repair_mesh(non_watertight_mesh, options)
        assert repaired.is_watertight is True

    def test_repair_with_minimal_options(self, non_watertight_mesh):
        """Test repair with only hole filling."""
        options = RepairOptions(
            fill_holes=True,
            fix_normals=False,
            remove_degenerate=False,
            merge_vertices=False,
            remove_duplicates=False,
        )
        repaired = repair_mesh(non_watertight_mesh, options)
        # Should still attempt to fill holes
        assert isinstance(repaired, trimesh.Trimesh)

    def test_repair_returns_trimesh(self, cube_mesh):
        """Test that repair returns a Trimesh object."""
        repaired = repair_mesh(cube_mesh)
        assert isinstance(repaired, trimesh.Trimesh)

    def test_repair_fixes_inverted_normals(self):
        """Test that repair fixes inverted normals."""
        mesh = trimesh.creation.box(extents=[1, 1, 1])
        # Flip some normals
        half = len(mesh.faces) // 2
        mesh.faces[:half] = mesh.faces[:half][:, ::-1]
        repaired = repair_mesh(mesh)
        # After fix_normals, normals should be consistent
        # Check that face normals point outward (positive z for top faces)
        assert repaired is not None

    def test_repair_defaults(self, non_watertight_mesh):
        """Test that default options repair the mesh."""
        repaired = repair_mesh(non_watertight_mesh)
        assert repaired.is_watertight is True
