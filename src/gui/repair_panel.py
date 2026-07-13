"""Repair options and status panel."""

from PySide6.QtWidgets import (
    QCheckBox,
    QGroupBox,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


class RepairPanel(QWidget):
    """Panel for mesh analysis and repair controls."""

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)

        # Options group
        options_group = QGroupBox("Repair Options")
        options_layout = QVBoxLayout(options_group)

        self.fill_holes_cb = QCheckBox("Fill Holes")
        self.fill_holes_cb.setChecked(True)
        self.fix_normals_cb = QCheckBox("Fix Normals")
        self.fix_normals_cb.setChecked(True)
        self.remove_degenerate_cb = QCheckBox("Remove Degenerate Faces")
        self.remove_degenerate_cb.setChecked(True)

        options_layout.addWidget(self.fill_holes_cb)
        options_layout.addWidget(self.fix_normals_cb)
        options_layout.addWidget(self.remove_degenerate_cb)
        layout.addWidget(options_group)

        # Action buttons
        self.analyze_btn = QPushButton("Analyze")
        self.repair_btn = QPushButton("Repair")
        layout.addWidget(self.analyze_btn)
        layout.addWidget(self.repair_btn)

        # Status display
        self.status_text = QTextEdit()
        self.status_text.setReadOnly(True)
        self.status_text.setMaximumHeight(150)
        self.status_text.setPlaceholderText("Analysis results will appear here...")
        layout.addWidget(self.status_text)
