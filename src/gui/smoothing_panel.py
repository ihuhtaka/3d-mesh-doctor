"""Smoothing controls panel with sliders."""

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QComboBox,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSlider,
    QVBoxLayout,
    QWidget,
)

from src.core.mesh_smoother import SmoothMethod


class SmoothingPanel(QWidget):
    """Panel for mesh smoothing controls."""

    preview_requested = Signal(dict)
    apply_requested = Signal(dict)
    reset_requested = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)

        # Method selector
        method_layout = QHBoxLayout()
        method_layout.addWidget(QLabel("Method:"))
        self.method_combo = QComboBox()
        for method in SmoothMethod:
            self.method_combo.addItem(method.value.title(), method)
        method_layout.addWidget(self.method_combo)
        layout.addLayout(method_layout)

        # Iterations slider
        iter_group = QGroupBox("Iterations")
        iter_layout = QVBoxLayout(iter_group)
        self.iter_slider = QSlider()
        self.iter_slider.setRange(1, 100)
        self.iter_slider.setValue(10)
        self.iter_label = QLabel("10")
        self.iter_slider.valueChanged.connect(
            lambda v: self.iter_label.setText(str(v))
        )
        iter_layout.addWidget(self.iter_slider)
        iter_layout.addWidget(self.iter_label)
        layout.addWidget(iter_group)

        # Strength slider
        strength_group = QGroupBox("Strength")
        strength_layout = QVBoxLayout(strength_group)
        self.strength_slider = QSlider()
        self.strength_slider.setRange(0, 100)
        self.strength_slider.setValue(50)
        self.strength_label = QLabel("0.50")
        self.strength_slider.valueChanged.connect(
            lambda v: self.strength_label.setText(f"{v / 100:.2f}")
        )
        strength_layout.addWidget(self.strength_slider)
        strength_layout.addWidget(self.strength_label)
        layout.addWidget(strength_group)

        # Buttons
        btn_layout = QHBoxLayout()
        self.preview_btn = QPushButton("Preview")
        self.preview_btn.clicked.connect(lambda: self.preview_requested.emit(self.get_params()))
        self.apply_btn = QPushButton("Apply")
        self.apply_btn.clicked.connect(lambda: self.apply_requested.emit(self.get_params()))
        self.reset_btn = QPushButton("Reset")
        self.reset_btn.clicked.connect(self.reset_requested)
        btn_layout.addWidget(self.preview_btn)
        btn_layout.addWidget(self.apply_btn)
        btn_layout.addWidget(self.reset_btn)
        layout.addLayout(btn_layout)

    def get_params(self) -> dict:
        """Get current smoothing parameters."""
        method = self.method_combo.currentData()
        return {
            "method": method,
            "iterations": self.iter_slider.value(),
            "lambd": self.strength_slider.value() / 100.0,
        }
