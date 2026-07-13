"""3D viewer widget using PyVista + Qt."""

import numpy as np
import pyvista as pv
import trimesh
from pyvistaqt import QtInteractor


class ViewerWidget(QtInteractor):
    """Embedded PyVista 3D viewer with mesh display helpers."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._current_mesh_actor = None
        self._issue_actor = None
        self._hole_actor = None

    def display_mesh(self, mesh: trimesh.Trimesh, color="lightblue", opacity=1.0):
        """Display a trimesh in the viewer."""
        self.clear()
        pv_mesh = pv.wrap(mesh.vertices, mesh.faces)
        self.add_mesh(pv_mesh, color=color, opacity=opacity, show_edges=True)
        self.reset_camera()

    def highlight_issues(self, mesh: trimesh.Trimesh, edges: list, color="red"):
        """Highlight non-manifold edges as wireframe overlay."""
        if not edges:
            return
        pv_mesh = pv.wrap(mesh.vertices, mesh.faces)
        self.add_mesh(
            pv_mesh,
            style="wireframe",
            color=color,
            opacity=0.3,
            name="issues",
        )

    def highlight_holes(self, mesh: trimesh.Trimesh, edges: list, color="yellow"):
        """Highlight hole boundaries."""
        if not edges:
            return
        pv_mesh = pv.wrap(mesh.vertices, mesh.faces)
        self.add_mesh(
            pv_mesh,
            style="wireframe",
            color=color,
            opacity=0.3,
            name="holes",
        )

    def clear_overlays(self):
        """Remove issue/hole overlays."""
        if "issues" in self.actors:
            del self.actors["issues"]
        if "holes" in self.actors:
            del self.actors["holes"]
