from PyQt5.QtWidgets import QHBoxLayout, QLabel, QLineEdit


def create_label_lineedit_pair(
    label_text: str, default_value="", placeholder: str = ""
) -> QHBoxLayout:
    label = QLabel(label_text)
    line_edit = QLineEdit(default_value)
    line_edit.setPlaceholderText(placeholder)

    return label, line_edit
