from PyQt5.QtWidgets import QComboBox, QLineEdit


def get_widget_text_value(widget):
    if isinstance(widget, QLineEdit):
        return widget.text().strip()
    elif isinstance(widget, QComboBox):
        return widget.currentText().strip()
    else:
        raise TypeError(f"Unsupported widget type: {type(widget)}")


def reset_widget(widget):
    if isinstance(widget, QLineEdit):
        return widget.clear()
    elif isinstance(widget, QComboBox):
        return widget.setCurrentIndex(0)
    else:
        raise TypeError(f"Unsupported widget type: {type(widget)}")
