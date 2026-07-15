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
        self._saved_cam: dict | None = None

    def _save_camera(self):
        """Save current camera state."""
        cam = self.camera
        self._saved_cam = {
            "position": cam.position,
            "focal_point": cam.focal_point,
            "up": cam.up,
            "parallel_scale": cam.parallel_scale,
        }

    def _restore_camera(self):
        """Restore previously saved camera state."""
        if self._saved_cam is None:
            return
        cam = self.camera
        cam.position = self._saved_cam["position"]
        cam.focal_point = self._saved_cam["focal_point"]
        cam.up = self._saved_cam["up"]
        cam.parallel_scale = self._saved_cam["parallel_scale"]

    def display_mesh(
        self, mesh: trimesh.Trimesh, color="lightblue", opacity=1.0, reset_camera=True
    ):
        """Display a trimesh in the viewer."""
        if not reset_camera and self._has_mesh:
            self._save_camera()
        self.clear()
        pv_mesh = pv.wrap(mesh)
        self.add_mesh(pv_mesh, color=color, opacity=opacity, show_edges=True)
        if reset_camera:
            self.reset_camera()
        else:
            self._restore_camera()
        self._has_mesh = True

    def display_distortion(
        self,
        original: trimesh.Trimesh,
        processed: trimesh.Trimesh,
        reset_camera=False,
        limit: float | None = None,
    ):
        """Display processed mesh colored by vertex distance to original.

        Parameters
        ----------
        limit : float, optional
            Symmetric color range in meters. Colors map from -limit to +limit.
            Values beyond the range are clamped (saturated red/blue).
            If None, uses auto-scaling (percentile-based).
        """
        if not reset_camera and self._has_mesh:
            self._save_camera()
        self.clear()
        pv_mesh = pv.wrap(processed)

        _, distances, _ = trimesh.proximity.ProximityQuery(original).on_surface(processed.vertices)
        distances = np.asarray(distances)

        if limit is not None and limit > 0:
            clamped = np.clip(distances, -limit, limit)
            pv_mesh["distance"] = clamped
            vmin, vmax = -limit, limit
            title = f"Dist (±{limit * 1000:.0f} um)"
        else:
            pv_mesh["distance"] = distances
            if len(distances) > 0 and np.max(distances) > 0:
                vmin = float(np.percentile(distances, 2))
                vmax = float(np.percentile(distances, 98))
                if vmax <= vmin:
                    vmax = vmin + 1e-6
            else:
                vmin, vmax = 0.0, 1.0
            title = f"Distance ({vmin:.4f} — {vmax:.4f})"

        self.add_mesh(
            pv_mesh,
            scalars="distance",
            cmap="coolwarm",
            clim=[vmin, vmax],
            show_edges=False,
            opacity=0.95,
            scalar_bar_args={"title": title},
        )
        if reset_camera:
            self.reset_camera()
        else:
            self._restore_camera()
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
