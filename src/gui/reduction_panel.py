"""Polygon reduction controls panel."""

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)


class ReductionPanel(QWidget):
    """Panel for mesh polygon reduction controls."""

    preview_requested = Signal(float)
    apply_requested = Signal(float)
    reset_requested = Signal()
    distortion_toggled = Signal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 2, 4, 2)
        layout.setSpacing(2)

        # Info labels + ratio on one row
        row1 = QHBoxLayout()
        row1.setSpacing(6)
        self.face_count_label = QLabel("Faces: —")
        self.vertex_count_label = QLabel("Vertices: —")
        row1.addWidget(self.face_count_label)
        row1.addWidget(self.vertex_count_label)
        row1.addStretch()
        row1.addWidget(QLabel("Keep:"))
        self.ratio_spin = QSpinBox()
        self.ratio_spin.setRange(5, 100)
        self.ratio_spin.setValue(50)
        self.ratio_spin.setSuffix("%")
        self.ratio_spin.setFixedWidth(56)
        row1.addWidget(self.ratio_spin)
        layout.addLayout(row1)

        # Estimate + distortion toggle
        row2 = QHBoxLayout()
        row2.setSpacing(6)
        self.estimate_label = QLabel("Estimated: — faces")
        row2.addWidget(self.estimate_label)
        row2.addStretch()
        self.distortion_btn = QPushButton("Show Diff")
        self.distortion_btn.setCheckable(True)
        self.distortion_btn.setFixedWidth(72)
        self.distortion_btn.toggled.connect(self.distortion_toggled)
        row2.addWidget(self.distortion_btn)
        layout.addLayout(row2)

        # Buttons on one row
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(4)
        self.preview_btn = QPushButton("Preview")
        self.preview_btn.clicked.connect(lambda: self.preview_requested.emit(self.get_ratio()))
        self.apply_btn = QPushButton("Apply")
        self.apply_btn.clicked.connect(lambda: self.apply_requested.emit(self.get_ratio()))
        self.reset_btn = QPushButton("Reset")
        self.reset_btn.clicked.connect(self.reset_requested)
        btn_layout.addWidget(self.preview_btn)
        btn_layout.addWidget(self.apply_btn)
        btn_layout.addWidget(self.reset_btn)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)

    def get_ratio(self) -> float:
        """Get the current reduction ratio (0.0-1.0)."""
        return self.ratio_spin.value() / 100.0

    def update_face_counts(self, face_count: int, vertex_count: int):
        """Update the displayed face/vertex counts."""
        self.face_count_label.setText(f"Faces: {face_count:,}")
        self.vertex_count_label.setText(f"Vertices: {vertex_count:,}")
        estimated = max(1, int(face_count * self.get_ratio()))
        self.estimate_label.setText(f"Estimated: {estimated:,} faces")

    def _on_ratio_changed(self, value: int):
        """Update estimate when ratio spinner changes."""
        pass
