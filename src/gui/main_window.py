"""Main application window."""

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QDockWidget,
    QHBoxLayout,
    QMainWindow,
    QMessageBox,
    QVBoxLayout,
    QWidget,
)

from src.gui.file_panel import FilePanel
from src.gui.repair_panel import RepairPanel
from src.gui.smoothing_panel import SmoothingPanel
from src.gui.viewer_widget import ViewerWidget


class MainWindow(QMainWindow):
    """Primary application window with 3D viewer and control panels."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("3D Mesh Doctor")
        self.setMinimumSize(1200, 800)

        # Central 3D viewer
        self.viewer = ViewerWidget()
        self.setCentralWidget(self.viewer)

        # Left dock: file list
        self.file_panel = FilePanel()
        file_dock = QDockWidget("Files", self)
        file_dock.setWidget(self.file_panel)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, file_dock)

        # Right dock: repair controls
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(0, 0, 0, 0)
        self.repair_panel = RepairPanel()
        self.smoothing_panel = SmoothingPanel()
        right_layout.addWidget(self.repair_panel)
        right_layout.addWidget(self.smoothing_panel)
        right_layout.addStretch()
        right_dock = QDockWidget("Controls", self)
        right_dock.setWidget(right_widget)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, right_dock)

        # Menu bar
        self._create_menus()

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
