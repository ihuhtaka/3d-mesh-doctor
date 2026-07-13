"""Export panel for saving repaired meshes."""

from PySide6.QtWidgets import (
    QComboBox,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class ExportPanel(QWidget):
    """Panel for mesh export controls."""

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)

        # Format selector
        fmt_layout = QHBoxLayout()
        fmt_layout.addWidget(QLabel("Format:"))
        self.format_combo = QComboBox()
        self.format_combo.addItems(["STL", "OBJ"])
        fmt_layout.addWidget(self.format_combo)
        layout.addLayout(fmt_layout)

        # Output directory
        dir_layout = QHBoxLayout()
        self.dir_edit = QLineEdit()
        self.dir_edit.setPlaceholderText("Output directory...")
        self.browse_btn = QPushButton("Browse")
        self.browse_btn.clicked.connect(self._browse_directory)
        dir_layout.addWidget(self.dir_edit)
        dir_layout.addWidget(self.browse_btn)
        layout.addLayout(dir_layout)

        # Export buttons
        btn_layout = QHBoxLayout()
        self.export_btn = QPushButton("Export")
        self.export_all_btn = QPushButton("Export All")
        btn_layout.addWidget(self.export_btn)
        btn_layout.addWidget(self.export_all_btn)
        layout.addLayout(btn_layout)

    def _browse_directory(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Output Directory")
        if folder:
            self.dir_edit.setText(folder)
