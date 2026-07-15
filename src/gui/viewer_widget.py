"""3D viewer widget using PyVista + Qt."""

import numpy as np
import pyvista as pv
import trimesh
from pyvistaqt import QtInteractor


class ViewerWidget(QtInteractor):
    """Embedded PyVista 3D viewer with mesh display helpers."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.set_background("white")
        self._has_mesh = False

    def display_mesh(
        self, mesh: trimesh.Trimesh, color="lightblue", opacity=1.0, reset_camera=True
    ):
        """Display a trimesh in the viewer."""
        cam = self.camera.copy() if not reset_camera and self._has_mesh else None
        self.clear()
        pv_mesh = pv.wrap(mesh)
        self.add_mesh(pv_mesh, color=color, opacity=opacity, show_edges=True)
        if reset_camera:
            self.reset_camera()
        elif cam is not None:
            self.camera.copy_from(cam)
        self._has_mesh = True

    def display_distortion(
        self, original: trimesh.Trimesh, processed: trimesh.Trimesh, reset_camera=False
    ):
        """Display processed mesh colored by vertex distance to original."""
        cam = self.camera.copy() if not reset_camera and self._has_mesh else None
        self.clear()
        pv_mesh = pv.wrap(processed)

        _, distances, _ = trimesh.proximity.ProximityQuery(original).on_surface(processed.vertices)
        distances = np.asarray(distances)

        pv_mesh["distance"] = distances

        # Use percentile-based range for better contrast
        if len(distances) > 0 and np.max(distances) > 0:
            vmin = float(np.percentile(distances, 2))
            vmax = float(np.percentile(distances, 98))
            if vmax <= vmin:
                vmax = vmin + 1e-6
        else:
            vmin, vmax = 0.0, 1.0

        self.add_mesh(
            pv_mesh,
            scalars="distance",
            cmap="coolwarm",
            clim=[vmin, vmax],
            show_edges=False,
            opacity=0.95,
            scalar_bar_args={"title": f"Distance ({vmin:.4f} — {vmax:.4f})"},
        )
        if reset_camera:
            self.reset_camera()
        elif cam is not None:
            self.camera.copy_from(cam)
        self._has_mesh = True

    def highlight_holes(self, mesh: trimesh.Trimesh, edges: list, color="yellow"):
        """Highlight hole boundary edges as lines."""
        if not edges or not self._has_mesh:
            return
        points = np.array([mesh.vertices[e] for e in edges]).reshape(-1, 3)
        line_mesh = pv.line_segments_from_points(points)
        self.add_mesh(line_mesh, color=color, line_width=3, name="holes")

    def highlight_issues(self, mesh: trimesh.Trimesh, edges: list, color="red"):
        """Highlight non-manifold edges as lines."""
        if not edges or not self._has_mesh:
            return
        points = np.array([mesh.vertices[e] for e in edges]).reshape(-1, 3)
        line_mesh = pv.line_segments_from_points(points)
        self.add_mesh(line_mesh, color=color, line_width=3, name="issues")

    def clear_overlays(self):
        """Remove issue/hole overlays."""
        for name in ["issues", "holes"]:
            if name in self.actors:
                self.remove_actor(name)
