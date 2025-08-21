from PyQt5.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QGridLayout
from PyQt5.QtGui import QIntValidator

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


def add_widgets_to_grid_by_specs(
    specs_list: list[tuple], group_layout: QGridLayout
) -> dict:

    all_data_widgets = {}

    for row_idx, row_specs in enumerate(specs_list):
        label, data_type, default, placeholder = row_specs

        if data_type is str or data_type is int:
            label_widget, line_edit_widget = create_label_lineedit_pair(
                label, default, placeholder
            )
            group_layout.addWidget(label_widget, row_idx, 0)
            group_layout.addWidget(line_edit_widget, row_idx, 1)
            all_data_widgets[label] = line_edit_widget

            if data_type is int:
                line_edit_widget.setValidator(QIntValidator())

        elif data_type is list:
            list_widget = create_list_widget(
                label, "http://www.opengis.net/def/crs/OGC/1.3/CRS84"
            )
            group_layout.addWidget(list_widget.label, row_idx, 0)
            group_layout.addWidget(list_widget, row_idx, 1)
            all_data_widgets[label] = list_widget

    return all_data_widgets
