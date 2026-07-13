"""3D viewer widget using PyVista + Qt."""

import pyvista as pv
import trimesh
from pyvistaqt import QtInteractor


class ViewerWidget(QtInteractor):
    """Embedded PyVista 3D viewer with mesh display helpers."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.set_background("white")

    def display_mesh(self, mesh: trimesh.Trimesh, color="lightblue", opacity=1.0):
        """Display a trimesh in the viewer."""
        self.clear()
        pv_mesh = pv.PolyData(mesh.vertices, mesh.faces)
        self.add_mesh(pv_mesh, color=color, opacity=opacity, show_edges=True)
        self.reset_camera()

    def highlight_holes(self, mesh: trimesh.Trimesh, edges: list, color="yellow"):
        """Highlight hole boundary edges as lines."""
        if not edges:
            return
        lines = []
        for edge in edges:
            lines.extend([2, int(edge[0]), int(edge[1])])
        line_mesh = pv.LineSegments(mesh.vertices, lines)
        self.add_mesh(line_mesh, color=color, line_width=3, name="holes")

    def highlight_issues(self, mesh: trimesh.Trimesh, edges: list, color="red"):
        """Highlight non-manifold edges as lines."""
        if not edges:
            return
        lines = []
        for edge in edges:
            lines.extend([2, int(edge[0]), int(edge[1])])
        line_mesh = pv.LineSegments(mesh.vertices, lines)
        self.add_mesh(line_mesh, color=color, line_width=3, name="issues")

    def clear_overlays(self):
        """Remove issue/hole overlays."""
        for name in ["issues", "holes"]:
            if name in self.actors:
                self.remove_actor(name)
