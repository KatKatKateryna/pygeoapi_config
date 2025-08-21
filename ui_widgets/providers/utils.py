from PyQt5.QtWidgets import (
    QHBoxLayout,
    QInputDialog,
    QLabel,
    QLineEdit,
)
from .StringListWidget import StringListWidget


def create_label_lineedit_pair(
    label_text: str, default_value="", placeholder: str = ""
) -> QHBoxLayout:
    label = QLabel(label_text)
    line_edit = QLineEdit(default_value)
    line_edit.setPlaceholderText(placeholder)

    return label, line_edit


def create_list_widget(label_text: str, default_new_string: str = ""):
    return StringListWidget(label_text, default_new_string)
