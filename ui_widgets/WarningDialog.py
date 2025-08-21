from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTextEdit, QPushButton
from PyQt5.QtCore import Qt


class ReadOnlyTextDialog(QDialog):
    def __init__(self, parent=None, title="Message", text=""):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setWindowFlag(Qt.WindowStaysOnTopHint)  # optional: always on top
        self.setModal(True)  # blocks parent

        layout = QVBoxLayout(self)

        # Scrollable read-only text area
        text_edit = QTextEdit()
        text_edit.setReadOnly(True)
        text_edit.setPlainText(text)
        text_edit.setMinimumSize(400, 200)  # adjust size as needed
        layout.addWidget(text_edit)

        # Close button
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.accept)
        layout.addWidget(close_button)
