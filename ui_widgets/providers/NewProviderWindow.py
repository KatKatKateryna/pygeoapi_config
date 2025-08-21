from PyQt5.QtWidgets import (
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
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QIntValidator

from ...models.top_level.providers.records import ProviderTypes
from .provider_features import create_feature_provider_window
from .provider_map import create_map_provider_window
from .provider_tile import create_tile_provider_window
from .StringListWidget import StringListWidget


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

        self.setWindowFlag(Qt.WindowStaysOnTopHint)  # always on top
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
            self.elements_with_values = create_feature_provider_window(
                group_layout, data_list
            )

        elif provider_type == ProviderTypes.MAP:
            self.elements_with_values = create_map_provider_window(
                group_layout, data_list
            )

        elif provider_type == ProviderTypes.TILE:
            self.elements_with_values = create_tile_provider_window(
                group_layout, data_list
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
            values[key] = self.extract_value_from_ui(element)

        # emit values to the parent widget
        self.signal_provider_values.emit(self, values)

        # Close the window
        # self.close()

    def extract_value_from_ui(self, element):

        if isinstance(element, QLineEdit):

            validator = element.validator()
            if isinstance(validator, QIntValidator):
                try:
                    return int(element.text())
                except ValueError:  # e.g. if the field is empty
                    return None
            else:
                return element.text()

        elif isinstance(element, StringListWidget):
            return element.values_to_list()
