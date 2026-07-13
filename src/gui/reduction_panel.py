"""Polygon reduction controls panel."""

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSlider,
    QVBoxLayout,
    QWidget,
)


class ReductionPanel(QWidget):
    """Panel for mesh polygon reduction controls."""

    preview_requested = Signal(float)
    apply_requested = Signal(float)
    reset_requested = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)

        # Info label (shows current face count)
        info_group = QGroupBox("Mesh Info")
        info_layout = QVBoxLayout(info_group)
        self.face_count_label = QLabel("Faces: —")
        self.vertex_count_label = QLabel("Vertices: —")
        info_layout.addWidget(self.face_count_label)
        info_layout.addWidget(self.vertex_count_label)
        layout.addWidget(info_group)

        # Reduction slider
        reduce_group = QGroupBox("Reduction")
        reduce_layout = QVBoxLayout(reduce_group)

        ratio_row = QHBoxLayout()
        ratio_row.addWidget(QLabel("Keep:"))
        self.ratio_slider = QSlider()
        self.ratio_slider.setRange(5, 100)
        self.ratio_slider.setValue(50)
        self.ratio_slider.setTickPosition(QSlider.TickPosition.NoTicks)
        self.ratio_label = QLabel("50%")
        self.ratio_slider.valueChanged.connect(
            lambda v: self.ratio_label.setText(f"{v}%")
        )
        ratio_row.addWidget(self.ratio_slider)
        ratio_row.addWidget(self.ratio_label)
        reduce_layout.addLayout(ratio_row)

        self.estimate_label = QLabel("Estimated output: — faces")
        reduce_layout.addWidget(self.estimate_label)
        layout.addWidget(reduce_group)

        # Buttons
        btn_layout = QHBoxLayout()
        self.preview_btn = QPushButton("Preview")
        self.preview_btn.clicked.connect(lambda: self.preview_requested.emit(self.get_ratio()))
        self.apply_btn = QPushButton("Apply")
        self.apply_btn.clicked.connect(lambda: self.apply_requested.emit(self.get_ratio()))
        self.reset_btn = QPushButton("Reset")
        self.reset_btn.clicked.connect(self.reset_requested)
        btn_layout.addWidget(self.preview_btn)
        btn_layout.addWidget(self.apply_btn)
        btn_layout.addWidget(self.reset_btn)
        layout.addLayout(btn_layout)

    def get_ratio(self) -> float:
        """Get the current reduction ratio (0.0-1.0)."""
        return self.ratio_slider.value() / 100.0

    def update_face_counts(self, face_count: int, vertex_count: int):
        """Update the displayed face/vertex counts."""
        self.face_count_label.setText(f"Faces: {face_count:,}")
        self.vertex_count_label.setText(f"Vertices: {vertex_count:,}")
        estimated = max(1, int(face_count * self.get_ratio()))
        self.estimate_label.setText(f"Estimated output: {estimated:,} faces")

    def _on_ratio_changed(self, value: int):
        """Update estimate when ratio slider changes."""
        # This will be connected in MainWindow after a mesh is loaded
        pass
