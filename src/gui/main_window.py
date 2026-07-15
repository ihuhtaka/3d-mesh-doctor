"""Main application window."""

from pathlib import Path

import trimesh
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QDockWidget,
    QMainWindow,
    QMessageBox,
    QVBoxLayout,
    QWidget,
)

from src.core.mesh_analyzer import analyze_mesh
from src.core.mesh_exporter import export_mesh
from src.core.mesh_loader import load_mesh
from src.core.mesh_metrics import compute_quality
from src.core.mesh_reducer import reduce_polygons
from src.core.mesh_repairer import RepairOptions, repair_mesh
from src.core.mesh_smoother import smooth_mesh
from src.gui.export_panel import ExportPanel
from src.gui.file_panel import FilePanel
from src.gui.reduction_panel import ReductionPanel
from src.gui.repair_panel import RepairPanel
from src.gui.smoothing_panel import SmoothingPanel
from src.gui.viewer_widget import ViewerWidget


class MainWindow(QMainWindow):
    """Primary application window with 3D viewer and control panels."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("3D Mesh Doctor")
        self.setMinimumSize(1200, 800)

        # Mesh state
        self._current_mesh: trimesh.Trimesh | None = None
        self._original_mesh: trimesh.Trimesh | None = None
        self._current_path: Path | None = None
        self._distortion_active = False

        # Central 3D viewer
        self.viewer = ViewerWidget()
        self.setCentralWidget(self.viewer)

        # Left dock: file list
        self.file_panel = FilePanel()
        self.file_dock = QDockWidget("Files", self)
        self.file_dock.setWidget(self.file_panel)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.file_dock)

        # Right dock: repair + smoothing + reduction controls
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(0, 0, 0, 0)
        self.repair_panel = RepairPanel()
        self.smoothing_panel = SmoothingPanel()
        self.reduction_panel = ReductionPanel()
        right_layout.addWidget(self.repair_panel)
        right_layout.addWidget(self.smoothing_panel)
        right_layout.addWidget(self.reduction_panel)
        right_layout.addStretch()
        self.controls_dock = QDockWidget("Controls", self)
        self.controls_dock.setWidget(right_widget)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.controls_dock)

        # Bottom dock: export
        self.export_panel = ExportPanel()
        self.export_dock = QDockWidget("Export", self)
        self.export_dock.setWidget(self.export_panel)
        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self.export_dock)

        # Connect signals
        self._connect_signals()

        # Menu bar
        self._create_menus()

    def _connect_signals(self):
        """Connect all panel signals to handlers."""
        # File panel
        self.file_panel.file_selected.connect(self._on_file_selected)

        # Repair panel
        self.repair_panel.analyze_requested.connect(self._on_analyze)
        self.repair_panel.repair_requested.connect(self._on_repair)

        # Smoothing panel
        self.smoothing_panel.preview_requested.connect(self._on_smooth_preview)
        self.smoothing_panel.apply_requested.connect(self._on_smooth_apply)
        self.smoothing_panel.reset_requested.connect(self._on_smooth_reset)

        # Reduction panel
        self.reduction_panel.preview_requested.connect(self._on_reduce_preview)
        self.reduction_panel.apply_requested.connect(self._on_reduce_apply)
        self.reduction_panel.reset_requested.connect(self._on_reduce_reset)
        self.reduction_panel.ratio_spin.valueChanged.connect(self._on_ratio_changed)
        self.reduction_panel.distortion_toggled.connect(self._on_distortion_toggled)
        self.reduction_panel.distortion_limit_changed.connect(self._on_distortion_limit_changed)

        # Export panel
        self.export_panel.export_requested.connect(self._on_export)
        self.export_panel.export_all_requested.connect(self._on_export_all)

    def _create_menus(self):
        menu_bar = self.menuBar()

        # File menu
        file_menu = menu_bar.addMenu("File")
        open_action = QAction("Open Files...", self)
        open_action.triggered.connect(self.file_panel.open_files)
        file_menu.addAction(open_action)

        open_folder_action = QAction("Open Folder...", self)
        open_folder_action.triggered.connect(self.file_panel.open_folder)
        file_menu.addAction(open_folder_action)

        file_menu.addSeparator()

        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # View menu — panel toggles
        view_menu = menu_bar.addMenu("View")
        for label, dock in [
            ("Files", self.file_dock),
            ("Controls", self.controls_dock),
            ("Export", self.export_dock),
        ]:
            action = QAction(label, self)
            action.setCheckable(True)
            action.setChecked(dock.isVisible())
            action.toggled.connect(dock.setVisible)
            view_menu.addAction(action)

    def _show_quality(self, label: str):
        """Compute and display quality metrics comparing original to current."""
        if self._original_mesh is None or self._current_mesh is None:
            return
        q = compute_quality(self._original_mesh, self._current_mesh)
        text = (
            f"{label}\n"
            f"Faces: {q.original_faces:,} → {q.processed_faces:,}\n"
            f"Vertices: {q.original_vertices:,} → {q.processed_vertices:,}\n"
            f"Volume diff: {q.volume_diff_pct:.2f}%\n"
            f"Area diff: {q.area_diff_pct:.2f}%\n"
            f"Roughness: {q.roughness:.3f}\n"
            f"Hausdorff: {q.max_hausdorff:.6f}\n"
            f"Chamfer: {q.mean_chamfer:.6f}"
        )
        self.repair_panel.status_text.setText(text)

    def _set_mesh(self, mesh: trimesh.Trimesh, path: Path | None = None):
        """Update the current mesh and display it."""
        self._current_mesh = mesh
        self._original_mesh = mesh.copy()
        self._current_path = path
        self.viewer.display_mesh(mesh, reset_camera=True)
        self.repair_panel.status_text.clear()
        self.reduction_panel.update_face_counts(len(mesh.faces), len(mesh.vertices))
        self._distortion_active = False
        self.reduction_panel.distortion_btn.setChecked(False)

    def _on_file_selected(self, path: Path):
        """Load and display a mesh file."""
        try:
            mesh = load_mesh(path)
            self._set_mesh(mesh, path)
        except Exception as e:
            QMessageBox.warning(self, "Load Error", f"Failed to load {path.name}:\n{e}")

    def _on_analyze(self):
        """Analyze the current mesh for issues."""
        if self._current_mesh is None:
            self.repair_panel.status_text.setText("No mesh loaded.")
            return

        report = analyze_mesh(self._current_mesh)
        lines = [
            f"Faces: {report.face_count}",
            f"Vertices: {report.vertex_count}",
            f"Watertight: {'Yes' if report.is_watertight else 'No'}",
        ]
        if not report.is_watertight:
            lines.append(f"Holes detected: {report.hole_count}")
        if report.non_manifold_edge_count > 0:
            lines.append(f"Non-manifold edges: {report.non_manifold_edge_count}")
        if report.has_inverted_normals:
            lines.append("Warning: Inverted normals detected")

        self.repair_panel.status_text.setText("\n".join(lines))

        self.viewer.clear_overlays()
        if not report.is_watertight:
            self.viewer.highlight_holes(self._current_mesh, report.hole_edges)

    def _on_repair(self):
        """Repair the current mesh."""
        if self._current_mesh is None:
            self.repair_panel.status_text.setText("No mesh loaded.")
            return

        options_dict = self.repair_panel.get_repair_options()
        options = RepairOptions(**options_dict)

        try:
            repaired = repair_mesh(self._current_mesh, options)
            self._current_mesh = repaired
            self.viewer.display_mesh(repaired, reset_camera=False)
            self.viewer.clear_overlays()
            self._show_quality("Repaired successfully")
        except Exception as e:
            QMessageBox.warning(self, "Repair Error", f"Repair failed:\n{e}")

    def _on_smooth_preview(self, params: dict):
        """Preview smoothing on the current mesh (non-destructive)."""
        if self._current_mesh is None:
            return
        preview = self._current_mesh.copy()
        smooth_mesh(preview, **params)
        self.viewer.display_mesh(preview, opacity=0.8, reset_camera=False)

    def _on_smooth_apply(self, params: dict):
        """Apply smoothing to the current mesh."""
        if self._current_mesh is None:
            return
        smooth_mesh(self._current_mesh, **params)
        self.viewer.display_mesh(self._current_mesh, reset_camera=False)
        self._show_quality("Smoothed")

    def _on_smooth_reset(self):
        """Reset to original mesh."""
        if self._original_mesh is None:
            return
        self._current_mesh = self._original_mesh.copy()
        self.viewer.display_mesh(self._current_mesh)
        self.repair_panel.status_text.clear()
        self._distortion_active = False
        self.reduction_panel.distortion_btn.setChecked(False)

    def _on_ratio_changed(self, value: int):
        """Update the face count estimate when ratio spinner changes."""
        if self._current_mesh is not None:
            ratio = value / 100.0
            estimated = max(1, int(len(self._current_mesh.faces) * ratio))
            self.reduction_panel.estimate_label.setText(
                f"Estimated: {estimated:,} faces"
            )

    def _on_reduce_preview(self, ratio: float):
        """Preview reduction on the current mesh (non-destructive)."""
        if self._current_mesh is None:
            return
        preview = self._current_mesh.copy()
        reduce_polygons(preview, ratio=ratio)
        self.viewer.display_mesh(preview, opacity=0.8, reset_camera=False)

    def _on_reduce_apply(self, ratio: float):
        """Apply reduction to the current mesh."""
        if self._current_mesh is None:
            return
        self._current_mesh = reduce_polygons(self._current_mesh, ratio=ratio)
        self.viewer.display_mesh(self._current_mesh, reset_camera=False)
        self.reduction_panel.update_face_counts(
            len(self._current_mesh.faces), len(self._current_mesh.vertices)
        )
        self._show_quality("Reduced")
        self._distortion_active = False
        self.reduction_panel.distortion_btn.setChecked(False)

    def _on_reduce_reset(self):
        """Reset to original mesh."""
        if self._original_mesh is None:
            return
        self._current_mesh = self._original_mesh.copy()
        self.viewer.display_mesh(self._current_mesh)
        self.reduction_panel.update_face_counts(
            len(self._current_mesh.faces), len(self._current_mesh.vertices)
        )
        self.repair_panel.status_text.clear()
        self._distortion_active = False
        self.reduction_panel.distortion_btn.setChecked(False)

    def _on_distortion_toggled(self, checked: bool):
        """Toggle distortion visualization."""
        if self._original_mesh is None or self._current_mesh is None:
            return
        self._distortion_active = checked
        if checked:
            limit = self.reduction_panel.get_distortion_limit()
            self.viewer.display_distortion(
                self._original_mesh, self._current_mesh, limit=limit
            )
        else:
            self.viewer.display_mesh(self._current_mesh, reset_camera=False)

    def _on_distortion_limit_changed(self, limit: float):
        """Update distortion visualization when limit changes."""
        if (
            self._distortion_active
            and self._original_mesh is not None
            and self._current_mesh is not None
        ):
            self.viewer.display_distortion(
                self._original_mesh, self._current_mesh, limit=limit
            )

    def _on_export(self, output_dir: Path, fmt: str):
        """Export the current mesh."""
        if self._current_mesh is None:
            QMessageBox.warning(self, "Export Error", "No mesh loaded.")
            return

        stem = self._current_path.stem if self._current_path else "mesh"
        out_path = output_dir / f"{stem}_repaired.{fmt}"

        try:
            export_mesh(self._current_mesh, out_path)
            QMessageBox.information(self, "Export Done", f"Saved to {out_path}")
        except Exception as e:
            QMessageBox.warning(self, "Export Error", f"Export failed:\n{e}")

    def _on_export_all(self, output_dir: Path, fmt: str):
        """Export all loaded meshes."""
        paths = self.file_panel.get_all_paths()
        if not paths:
            QMessageBox.warning(self, "Export Error", "No files loaded.")
            return

        exported = 0
        errors = []
        for path in paths:
            try:
                mesh = load_mesh(path)
                repair_mesh(mesh)
                out_path = output_dir / f"{path.stem}_repaired.{fmt}"
                export_mesh(mesh, out_path)
                exported += 1
            except Exception as e:
                errors.append(f"{path.name}: {e}")

        msg = f"Exported {exported} file(s)."
        if errors:
            msg += f"\n\n{len(errors)} error(s):\n" + "\n".join(errors[:5])
        QMessageBox.information(self, "Batch Export", msg)
