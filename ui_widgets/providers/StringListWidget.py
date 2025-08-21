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
)
from PyQt5.QtGui import QFontMetrics


class StringListWidget(QWidget):
    label: QLabel
    default_new_string: str = ""

    def __init__(self, label_text: str, default_new_string: str = ""):
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
        self.add_button.clicked.connect(self.add_item)
        button_layout.addWidget(self.add_button)

        self.remove_button = QPushButton("Remove")
        self.remove_button.clicked.connect(self.remove_item)
        button_layout.addWidget(self.remove_button)

    def add_item(self):
        # short option, but the dialog window is too narrow
        r"""
        text, ok = QInputDialog.getText(
            self, "Add Item", "Enter new item:", text=self.default_new_string
        )
        if ok and text.strip():
            self.list_widget.addItem(text.strip())
        """

        # longer option

        # create the dialog instance
        dialog = QInputDialog(self)
        dialog.setWindowTitle("Add Item")
        dialog.setLabelText("Enter new item:")
        dialog.setTextValue(self.default_new_string)

        # auto-size based on text width
        fm = QFontMetrics(dialog.font())
        width = (
            fm.horizontalAdvance(self.default_new_string) + 150
        )  # extra space for padding/buttons
        dialog.resize(width, dialog.height())

        if dialog.exec_() == QInputDialog.Accepted:
            text = dialog.textValue().strip()
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
