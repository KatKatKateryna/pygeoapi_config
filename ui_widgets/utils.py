from enum import Enum
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


def set_combo_box_value_from_data(*, combo_box, value):
    """Set the combo box value based on the available choice and provided value."""

    for i in range(combo_box.count()):
        if isinstance(value, str):
            if combo_box.itemText(i) == value:
                combo_box.setCurrentIndex(i)
                return

        if isinstance(value, Enum):
            if combo_box.itemText(i) == value.value:
                combo_box.setCurrentIndex(i)
                return

    # If the value is not found, set to the first item or clear it
    if combo_box.count() > 0:
        combo_box.setCurrentIndex(0)
    else:
        combo_box.clear()
