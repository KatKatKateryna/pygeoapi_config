from datetime import datetime
import json
from qgis.PyQt.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QTextEdit,
    QPushButton,
    QDialogButtonBox,
)
from qgis.PyQt.QtCore import Qt


def default_serializer(obj):
    """Convert unsupported objects to serializable types."""
    if isinstance(obj, datetime):
        return obj.strftime("%Y-%m-%dT%H:%M:%SZ")
    return str(obj)  # fallback for anything else


class ReadOnlyTextDialog(QDialog):
    def __init__(
        self, parent=None, title="Message", text="", add_true_false_btns=False
    ):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)  # optional: always on top
        self.setModal(True)  # blocks parent

        layout = QVBoxLayout(self)

        # Scrollable read-only text area
        text_edit = QTextEdit()
        text_edit.setReadOnly(True)
        text_edit.setMinimumSize(200, 200)  # adjust size as needed

        if isinstance(text, dict):
            formatted = json.dumps(
                text, indent=4, ensure_ascii=False, default=default_serializer
            )
        else:
            formatted = str(text)

        text_edit.setPlainText(formatted)
        layout.addWidget(text_edit)

        # Close button
        if not add_true_false_btns:
            close_button = QPushButton("Close")
            close_button.clicked.connect(self.accept)
            layout.addWidget(close_button)

        else:
            # OK / Cancel buttons
            button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
            button_box.accepted.connect(self.accept)
            button_box.rejected.connect(self.reject)
            layout.addWidget(button_box)
