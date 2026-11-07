from qgis.PyQt.QtWidgets import (
    QWidget,
    QComboBox,
    QLineEdit,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QGroupBox,
    QMainWindow,
    QGridLayout,
    QDialog,
)
from qgis.PyQt.QtCore import pyqtSignal, Qt
from qgis.PyQt.QtGui import QIntValidator

from ...models.top_level.providers import (
    ProviderPostgresql,
    ProviderMvtProxy,
    ProviderWmsFacade,
)

from ...models.top_level.providers.records import ProviderTypes
from ...models.utils import cast_list_elements_to_expected_types, cast_element_to_type
from .StringListWidget import StringListWidget
from .utils import add_widgets_to_grid_by_specs


class NewProviderWindow(QDialog):

    elements_with_values: dict
    signal_provider_values = pyqtSignal(object, dict)
    signal_provider_close = pyqtSignal()

    def __init__(
        self,
        provider_type: ProviderTypes,
        data_list: list[str] | None = None,
    ):
        super().__init__()
        self.signal_provider_close.connect(self.close)

        self.setWindowTitle(f"{provider_type.value.title()} Provider Configuration")

        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)  # always on top
        self.setModal(True)  # parent becomes unclickable

        self.main_layout = QVBoxLayout(self)

        # Create group box
        group_box = QGroupBox(f"{provider_type.value.title()} Provider")
        group_layout = QGridLayout()
        group_box.setLayout(group_layout)
        self.main_layout.addWidget(group_box)

        # fill the box depending on the provider type
        self.elements_with_values = {}
        if provider_type == ProviderTypes.FEATURE:
            self.elements_with_values = add_widgets_to_grid_by_specs(
                ProviderPostgresql.ui_elements_grid(), group_layout, data_list
            )

        elif provider_type == ProviderTypes.MAP:
            self.elements_with_values = add_widgets_to_grid_by_specs(
                ProviderWmsFacade.ui_elements_grid(), group_layout, data_list
            )

        elif provider_type == ProviderTypes.TILE:
            self.elements_with_values = add_widgets_to_grid_by_specs(
                ProviderMvtProxy.ui_elements_grid(), group_layout, data_list
            )

        # Add buttons at the bottom
        self.btn_add = QPushButton("Save")
        self.btn_cancel = QPushButton("Cancel")

        # Buttons container layout
        self.btn_layout = QHBoxLayout()
        self.btn_layout.addWidget(self.btn_add)
        self.btn_layout.addWidget(self.btn_cancel)
        self.main_layout.addLayout(self.btn_layout)

        # Connect buttons
        self.btn_cancel.clicked.connect(self.close)
        self.btn_add.clicked.connect(self.on_save_clicked)

        # Show the window
        self.resize(400, 300)
        self.show()

    def on_save_clicked(self):
        values = {}
        # Extract all QLineEdit values into a list
        for key, element in self.elements_with_values.items():
            widget = element["widget"]
            data_type = element["data_type"]

            ui_value: int | list | str | None = self.extract_value_from_ui(widget)
            if ui_value is list:
                values[key] = cast_list_elements_to_expected_types(
                    ui_value, data_type, key
                )
            else:
                try:
                    values[key] = cast_element_to_type(ui_value, data_type, key)
                except ValueError as e:  # if value is not matched
                    if ui_value == "":
                        ui_value = None
                        values[key] = cast_element_to_type(ui_value, data_type, key)
                    else:
                        raise e
        # print(values)
        # emit values to the parent widget
        self.signal_provider_values.emit(self, values)

        # Close the window
        # self.close()

    def extract_value_from_ui(self, widget) -> int | list | str | None:

        if isinstance(widget, QLineEdit):

            validator = widget.validator()
            if isinstance(validator, QIntValidator):
                try:
                    return int(widget.text())
                except ValueError:  # e.g. if the field is empty
                    return None
            else:
                return widget.text()

        elif isinstance(widget, QComboBox):
            return widget.currentText()

        elif isinstance(widget, StringListWidget):
            return widget.values_to_list()
