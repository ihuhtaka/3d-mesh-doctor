"""File list panel with drag-and-drop support."""

from pathlib import Path

from PySide6.QtGui import QDragEnterEvent, QDropEvent
from PySide6.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from src.core.mesh_loader import SUPPORTED_EXTENSIONS


class FilePanel(QWidget):
    """Panel for managing loaded mesh files."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self._file_paths: list[Path] = []

        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)

        # Buttons
        btn_layout = QHBoxLayout()
        self.add_files_btn = QPushButton("Add Files")
        self.add_files_btn.clicked.connect(self.open_files)
        self.add_folder_btn = QPushButton("Add Folder")
        self.add_folder_btn.clicked.connect(self.open_folder)
        btn_layout.addWidget(self.add_files_btn)
        btn_layout.addWidget(self.add_folder_btn)
        layout.addLayout(btn_layout)

        # File list
        self.file_list = QListWidget()
        self.file_list.currentRowChanged.connect(self._on_file_selected)
        layout.addWidget(self.file_list)

        # Status label
        self.status_label = QLabel("No files loaded")
        layout.addWidget(self.status_label)

    def open_files(self):
        """Open file dialog to select mesh files."""
        ext_filter = " ".join(f"*{e}" for e in SUPPORTED_EXTENSIONS)
        paths, _ = QFileDialog.getOpenFileNames(
            self, "Open Mesh Files", "", f"Mesh Files ({ext_filter})"
        )
        self._add_paths([Path(p) for p in paths])

    def open_folder(self):
        """Open folder dialog to load all mesh files."""
        folder = QFileDialog.getExistingDirectory(self, "Open Folder")
        if folder:
            folder_path = Path(folder)
            files = [
                p
                for p in folder_path.rglob("*")
                if p.suffix.lower() in SUPPORTED_EXTENSIONS
            ]
            self._add_paths(files)

    def _add_paths(self, paths: list[Path]):
        """Add file paths to the list."""
        for path in paths:
            if path not in self._file_paths:
                self._file_paths.append(path)
                self.file_list.addItem(path.name)
        self._update_status()

    def _update_status(self):
        count = len(self._file_paths)
        self.status_label.setText(f"{count} file{'s' if count != 1 else ''} loaded")

    def _on_file_selected(self, row: int):
        """Handle file selection."""
        if 0 <= row < len(self._file_paths):
            # Signal to viewer — to be connected in MainWindow
            pass

    def dragEnterEvent(self, event: QDragEnterEvent):  # noqa: N802
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):  # noqa: N802
        paths = []
        for url in event.mimeData().urls():
            path = Path(url.toLocalFile())
            if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS:
                paths.append(path)
            elif path.is_dir():
                files = [
                    p for p in path.rglob("*") if p.suffix.lower() in SUPPORTED_EXTENSIONS
                ]
                paths.extend(files)
        self._add_paths(paths)
