from PyQt5.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QGridLayout, QComboBox
from PyQt5.QtGui import QIntValidator

from .StringListWidget import StringListWidget
from ..utils import set_combo_box_value_from_data


def create_label_lineedit_pair(
    label_text: str, default_value="", placeholder: str = ""
) -> QHBoxLayout:
    label = QLabel(label_text)
    line_edit = QLineEdit(default_value)
    line_edit.setPlaceholderText(placeholder)

    return label, line_edit


def create_label_dropdown_pair(label_text: str, all_values: list) -> QHBoxLayout:
    label = QLabel(label_text)

    dropdown = QComboBox()
    dropdown.addItems([str(x) for x in all_values])  # make sure all values are strings
    dropdown.setCurrentIndex(0)

    return label, dropdown


def create_list_widget(label_text: str, default_new_string: str = ""):
    return StringListWidget(label_text, default_new_string)


def add_widgets_to_grid_by_specs(
    specs_list: list[tuple],
    group_layout: QGridLayout,
    data_list: list[str] | None = None,
) -> dict:

    all_data_widgets = {}

    for i, row_specs in enumerate(specs_list):
        label, data_type, special_widget_type, default, placeholder = row_specs

        # if regular widget (QLineEdit for str and int; QListWIdget for list)
        if not special_widget_type:
            if data_type is str or data_type is int:
                label_widget, data_widget = create_label_lineedit_pair(
                    label, default, placeholder
                )
                group_layout.addWidget(label_widget, i, 0)
                group_layout.addWidget(data_widget, i, 1)

                if data_type is int:
                    data_widget.setValidator(QIntValidator())

            elif data_type is list:
                default_list_entry = ""
                if label.endswith("crs"):
                    default_list_entry = "http://www.opengis.net/def/crs/OGC/1.3/CRS84"

                data_widget = create_list_widget(label, default_list_entry)
                group_layout.addWidget(data_widget.label, i, 0)
                group_layout.addWidget(data_widget, i, 1)

        else:
            if special_widget_type is QComboBox:
                all_values: list = placeholder  # case for dropdowns
                label_widget, data_widget = create_label_dropdown_pair(
                    label, all_values
                )
                group_layout.addWidget(label_widget, i, 0)
                group_layout.addWidget(data_widget, i, 1)

        # add to list of data widgets and fill with data if available
        all_data_widgets[label] = data_widget
        if data_list:
            assign_value_to_field(data_widget, data_list[i])

    return all_data_widgets


def assign_value_to_field(widget, text_data):
    if isinstance(widget, QLineEdit):
        widget.setText(text_data)
    if isinstance(widget, QComboBox):
        set_combo_box_value_from_data(combo_box=widget, value=text_data)
    if isinstance(widget, StringListWidget):
        widget.list_widget.clear()
        if len(text_data) > 0:
            for item in text_data.split(","):
                widget.list_widget.addItem(item)
