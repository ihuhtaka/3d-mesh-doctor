"""Repair options and status panel."""

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QCheckBox,
    QHBoxLayout,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


class RepairPanel(QWidget):
    """Panel for mesh analysis and repair controls."""

    analyze_requested = Signal()
    repair_requested = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 2, 4, 2)
        layout.setSpacing(2)

        # Checkboxes in a horizontal row
        opts = QHBoxLayout()
        opts.setSpacing(6)
        self.fill_holes_cb = QCheckBox("Fill Holes")
        self.fill_holes_cb.setChecked(True)
        self.fix_normals_cb = QCheckBox("Fix Normals")
        self.fix_normals_cb.setChecked(True)
        self.remove_degenerate_cb = QCheckBox("Degenerate Faces")
        self.remove_degenerate_cb.setChecked(True)
        opts.addWidget(self.fill_holes_cb)
        opts.addWidget(self.fix_normals_cb)
        opts.addWidget(self.remove_degenerate_cb)
        layout.addLayout(opts)

        # Buttons on one row
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(4)
        self.analyze_btn = QPushButton("Analyze")
        self.analyze_btn.clicked.connect(self.analyze_requested)
        self.repair_btn = QPushButton("Repair")
        self.repair_btn.clicked.connect(self.repair_requested)
        btn_layout.addWidget(self.analyze_btn)
        btn_layout.addWidget(self.repair_btn)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)

        # Status display
        self.status_text = QTextEdit()
        self.status_text.setReadOnly(True)
        self.status_text.setMaximumHeight(100)
        self.status_text.setPlaceholderText("Analysis results...")
        layout.addWidget(self.status_text)

    def get_repair_options(self) -> dict:
        """Get current repair options as a dict."""
        return {
            "fill_holes": self.fill_holes_cb.isChecked(),
            "fix_normals": self.fix_normals_cb.isChecked(),
            "remove_degenerate": self.remove_degenerate_cb.isChecked(),
        }
