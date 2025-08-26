from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QListWidget,
    QPushButton,
    QHBoxLayout,
    QInputDialog,
    QLabel,
    QLineEdit,
    QMessageBox,
    QDialog,
    QDialogButtonBox,
)
from PyQt5.QtGui import QFontMetrics


class StringListWidget(QWidget):
    label: QLabel
    default_new_string: str = ""

    def __init__(
        self, label_text: str, default_new_string: str = "", validation_callback=None
    ):
        super().__init__()
        # self.setWindowTitle(label_text)

        # Main layout
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        self.label = QLabel(label_text)
        self.default_new_string = default_new_string

        # List widget
        self.list_widget = QListWidget()
        layout.addWidget(self.list_widget)

        # Buttons
        button_layout = QHBoxLayout()
        layout.addLayout(button_layout)

        self.add_button = QPushButton("Add")
        self.add_button.clicked.connect(lambda: self.add_item(validation_callback))
        button_layout.addWidget(self.add_button)

        self.remove_button = QPushButton("Remove")
        self.remove_button.clicked.connect(self.remove_item)
        button_layout.addWidget(self.remove_button)

    def add_item(self, validation_callback):
        # short option, but the dialog window is too narrow
        r"""
        text, ok = QInputDialog.getText(
            self, "Add Item", "Enter new item:", text=self.default_new_string
        )
        if ok and text.strip():
            self.list_widget.addItem(text.strip())
        """

        # longer option
        dialog = InputWithValidateDialog(
            self.default_new_string, validation_callback, self
        )
        if dialog.exec_() == QDialog.Accepted:
            text = dialog.line_edit.text().strip()
            if text:
                self.list_widget.addItem(text)

    def remove_item(self):
        selected_items = self.list_widget.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Remove Item", "No item selected")
            return
        for item in selected_items:
            self.list_widget.takeItem(self.list_widget.row(item))

    def values_to_list(self):

        all_values = []
        for i in range(self.list_widget.count()):
            # using count to access data entries of 'list_widget' via .item(i)
            value = self.list_widget.item(i).text()
            all_values.append(value)

        return all_values


class InputWithValidateDialog(QDialog):
    def __init__(self, default_text="", validation_callback=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Item")

        layout = QVBoxLayout(self)

        # Label + input row
        label = QLabel("Enter new item:")
        layout.addWidget(label)

        input_row = QHBoxLayout()
        self.line_edit = QLineEdit(default_text)
        input_row.addWidget(self.line_edit)

        # Add validate button if requested
        if validation_callback is not None:
            self.validate_btn = QPushButton("Validate")
            self.validate_btn.clicked.connect(
                lambda: validation_callback(self.line_edit.text().strip(), self)
            )
            input_row.addWidget(self.validate_btn)

        layout.addLayout(input_row)

        # Standard OK/Cancel buttons
        self.button_box = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        layout.addWidget(self.button_box)

        # Auto-size based on default text
        fm = QFontMetrics(self.font())
        width = fm.horizontalAdvance(default_text) + 150
        self.resize(width, self.height())
