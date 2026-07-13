"""Batch processing with background thread support."""

from pathlib import Path

from PySide6.QtCore import QThread, Signal

from src.core.mesh_exporter import export_mesh
from src.core.mesh_loader import load_mesh
from src.core.mesh_repairer import RepairOptions, repair_mesh
from src.core.mesh_smoother import SmoothMethod, smooth_mesh


class BatchProcessor(QThread):
    """Process multiple mesh files in a background thread."""

    progress = Signal(int, str)  # (percent, message)
    file_done = Signal(str, bool)  # (filename, success)
    finished_batch = Signal(list)  # list of (path, success) tuples

    def __init__(
        self,
        file_paths: list[Path],
        output_dir: Path,
        repair_options: RepairOptions | None = None,
        smooth_params: dict | None = None,
        export_format: str = "stl",
        parent=None,
    ):
        super().__init__(parent)
        self.file_paths = file_paths
        self.output_dir = output_dir
        self.repair_options = repair_options or RepairOptions()
        self.smooth_params = smooth_params
        self.export_format = export_format
        self._cancelled = False

    def cancel(self):
        self._cancelled = True

    def run(self):
        results = []
        total = len(self.file_paths)

        for i, path in enumerate(self.file_paths):
            if self._cancelled:
                break

            self.progress.emit(int(i / total * 100), f"Processing {path.name}...")

            try:
                mesh = load_mesh(path)
                mesh = repair_mesh(mesh, self.repair_options)

                if self.smooth_params:
                    mesh = smooth_mesh(mesh, **self.smooth_params)

                out_path = self.output_dir / f"{path.stem}_repaired.{self.export_format}"
                export_mesh(mesh, out_path)

                self.file_done.emit(path.name, True)
                results.append((str(path), True))
            except Exception as e:
                self.file_done.emit(f"{path.name}: {e}", False)
                results.append((str(path), False))

        self.progress.emit(100, "Done" if not self._cancelled else "Cancelled")
        self.finished_batch.emit(results)
