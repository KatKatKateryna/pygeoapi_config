from PyQt5.QtWidgets import (
    QWidget,
    QComboBox,
    QLineEdit,
    QSpinBox,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QGroupBox,
    QMainWindow,
    QGridLayout,
)
from PyQt5.QtCore import pyqtSignal

from ..models.top_level.providers.records import ProviderTypes
from .provider_features import create_feature_provider_window
from .utils import extract_value_from_ui


class NewProviderWindow(QMainWindow):

    elements_with_values: dict
    signal_provider_values = pyqtSignal(dict)

    def __init__(
        self, comboBoxResProviderType: QComboBox, provider_type: ProviderTypes
    ):
        super().__init__()
        value = comboBoxResProviderType.currentText().lower()
        self.setWindowTitle(f"{value.title()} Provider Configuration")

        # Create the main window
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.main_layout = QVBoxLayout()
        central_widget.setLayout(self.main_layout)

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
        self.btn_add.clicked.connect(self.on_add_clicked)

        # Show the window
        self.resize(400, 300)
        self.show()

    def on_add_clicked(self):
        values = {}
        # Extract all QLineEdit values into a list
        for key, element in self.elements_with_values.items():
            values[key] = extract_value_from_ui(element)

        # emit values to the parent widget
        self.signal_provider_values.emit(values)

        # Close the window
        self.close()
