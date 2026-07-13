"""Smoothing controls panel."""

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QComboBox,
    QDoubleSpinBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSpinBox,
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
        layout.setContentsMargins(4, 2, 4, 2)
        layout.setSpacing(2)

        # Method selector + Iterations on one row
        row1 = QHBoxLayout()
        row1.setSpacing(4)
        row1.addWidget(QLabel("Method:"))
        self.method_combo = QComboBox()
        for method in SmoothMethod:
            self.method_combo.addItem(method.value.title(), method)
        row1.addWidget(self.method_combo)
        row1.addWidget(QLabel("Iter:"))
        self.iter_spin = QSpinBox()
        self.iter_spin.setRange(1, 100)
        self.iter_spin.setValue(10)
        self.iter_spin.setFixedWidth(52)
        row1.addWidget(self.iter_spin)
        row1.addStretch()
        layout.addLayout(row1)

        # Strength on its own row
        row2 = QHBoxLayout()
        row2.setSpacing(4)
        row2.addWidget(QLabel("Strength:"))
        self.strength_spin = QDoubleSpinBox()
        self.strength_spin.setRange(0.01, 1.0)
        self.strength_spin.setSingleStep(0.05)
        self.strength_spin.setDecimals(2)
        self.strength_spin.setValue(0.50)
        self.strength_spin.setFixedWidth(60)
        row2.addWidget(self.strength_spin)
        row2.addStretch()
        layout.addLayout(row2)

        # Buttons on one row
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(4)
        self.preview_btn = QPushButton("Preview")
        self.preview_btn.clicked.connect(lambda: self.preview_requested.emit(self.get_params()))
        self.apply_btn = QPushButton("Apply")
        self.apply_btn.clicked.connect(lambda: self.apply_requested.emit(self.get_params()))
        self.reset_btn = QPushButton("Reset")
        self.reset_btn.clicked.connect(self.reset_requested)
        btn_layout.addWidget(self.preview_btn)
        btn_layout.addWidget(self.apply_btn)
        btn_layout.addWidget(self.reset_btn)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)

    def get_params(self) -> dict:
        """Get current smoothing parameters."""
        method = self.method_combo.currentData()
        return {
            "method": method,
            "iterations": self.iter_spin.value(),
            "lambd": self.strength_spin.value(),
        }
