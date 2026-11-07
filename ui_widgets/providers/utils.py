from qgis.PyQt.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QGridLayout,
    QComboBox,
    QPushButton,
)
from qgis.PyQt.QtGui import QIntValidator

from .StringListWidget import StringListWidget
from ..utils import get_url_status, set_combo_box_value_from_data


def create_label_lineedit_pair(
    label_text: str, default_value="", placeholder: str = "", validation_callback=None
) -> QHBoxLayout:
    label = QLabel(label_text)
    line_edit = QLineEdit(str(default_value) if default_value is not None else "")
    line_edit.setPlaceholderText(str(placeholder) if placeholder is not None else "")

    return {"label": label, "line_edit": line_edit}


def create_label_dropdown_pair(label_text: str, all_values: list) -> QHBoxLayout:
    label = QLabel(label_text)

    dropdown = QComboBox()
    dropdown.addItems([str(x) for x in all_values])  # make sure all values are strings
    dropdown.setCurrentIndex(0)

    return label, dropdown


def create_list_widget(
    label_text: str, default_new_string: str = "", validation_callback=None
):
    return StringListWidget(label_text, default_new_string, validation_callback)


def add_widgets_to_grid_by_specs(
    specs_list: list[tuple],
    group_layout: QGridLayout,
    data_list: list[str] | None = None,
) -> dict:

    all_data_widgets = {}

    for i, row_specs in enumerate(specs_list):
        label, data_type, default, special_widget_type, placeholder = row_specs

        # if regular widget (QLineEdit for str and int; QListWIdget for list)
        if special_widget_type != "QComboBox":

            # set up defaults
            default_list_entry = ""
            validation_callback = None

            if label.endswith("crs"):
                default_list_entry = "http://www.opengis.net/def/crs/OGC/1.3/CRS84"
                validation_callback = lambda url, parent: get_url_status(url, parent)

            # check data types and create corresponding widgets
            if data_type is list or data_type == (list | None):

                # assign data_widget!
                data_widget = create_list_widget(
                    label, default_list_entry, validation_callback
                )
                group_layout.addWidget(data_widget.label, i, 0)
                group_layout.addWidget(data_widget, i, 1)

            else:
                new_widgets = create_label_lineedit_pair(
                    label, default, placeholder, validation_callback
                )
                # assign data_widget!
                data_widget = new_widgets["line_edit"]
                group_layout.addWidget(new_widgets["label"], i, 0)
                group_layout.addWidget(new_widgets["line_edit"], i, 1)

                if data_type is int:
                    new_widgets["line_edit"].setValidator(QIntValidator())

        else:
            all_values: list = placeholder  # case for dropdowns
            # assign data_widget!
            label_widget, data_widget = create_label_dropdown_pair(label, all_values)
            group_layout.addWidget(label_widget, i, 0)
            group_layout.addWidget(data_widget, i, 1)

        # extra check:
        if special_widget_type == "disabled":
            data_widget.setEnabled(False)

        # add to list of data widgets and fill with data if available
        original_label_value = label.replace("*", "")
        all_data_widgets[original_label_value] = {}
        all_data_widgets[original_label_value]["widget"] = data_widget
        all_data_widgets[original_label_value]["data_type"] = data_type
        if data_list:  # e.g. for dropdown
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
