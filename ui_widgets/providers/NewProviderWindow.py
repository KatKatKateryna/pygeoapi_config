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

from ..data_from_ui_setter_utils import unpack_listwidget_values_to_sublists
from ...models.top_level.providers.records import ProviderTypes
from .provider_features import create_feature_provider_window
from .StringListWidget import StringListWidget


class NewProviderWindow(QDialog):

    elements_with_values: dict
    signal_provider_values = pyqtSignal(dict)

    def __init__(
        self, comboBoxResProviderType: QComboBox, provider_type: ProviderTypes
    ):
        super().__init__()
        value = comboBoxResProviderType.currentText().lower()
        self.setWindowTitle(f"{value.title()} Provider Configuration")

        self.setWindowFlag(Qt.WindowStaysOnTopHint)  # always on top
        self.setModal(True)  # parent becomes unclickable

        self.main_layout = QVBoxLayout(self)

        # Create group box
        group_box = QGroupBox(f"{value.title()} Provider")
        group_layout = QGridLayout()
        group_box.setLayout(group_layout)
        self.main_layout.addWidget(group_box)

        # fill the box depending on the provider type
        self.elements_with_values = {}
        if value == provider_type.FEATURE.value:
            self.elements_with_values = create_feature_provider_window(group_layout)

        elif value == provider_type.MAP.value:
            pass

        elif value == provider_type.TILE.value:
            pass

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
        self.signal_provider_values.emit(values)

        # Close the window
        self.close()

    def extract_value_from_ui(self, element):

        if isinstance(element, QLineEdit):
            return element.text()
        elif isinstance(element, StringListWidget):
            return element.values_to_list()
