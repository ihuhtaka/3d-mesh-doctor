"""Progress dialog for batch processing."""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QProgressBar,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
)


class ProgressDialog(QDialog):
    """Modal dialog showing batch processing progress."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Processing...")
        self.setMinimumWidth(400)
        self.setModal(True)

        layout = QVBoxLayout(self)

        self.status_label = QLabel("Preparing...")
        layout.addWidget(self.status_label)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        layout.addWidget(self.progress_bar)

        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(150)
        layout.addWidget(self.log_text)

        btn_layout = QHBoxLayout()
        self.cancel_btn = QPushButton("Cancel")
        btn_layout.addStretch()
        btn_layout.addWidget(self.cancel_btn)
        layout.addLayout(btn_layout)

    def update_progress(self, value: int, message: str):
        """Update progress bar and status."""
        self.progress_bar.setValue(value)
        self.status_label.setText(message)
        self.log_text.append(message)

    def set_finished(self, message: str):
        """Mark processing as finished."""
        self.status_label.setText(message)
        self.progress_bar.setValue(100)
        self.cancel_btn.setText("Close")
