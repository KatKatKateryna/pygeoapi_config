from enum import Enum
import requests
from urllib.parse import urlparse

from PyQt5.QtWidgets import QComboBox, QLineEdit, QMessageBox


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


def _is_url_responsive(url: str) -> bool:

    parsed_url = urlparse(url)
    if not all([parsed_url.scheme, parsed_url.netloc]):
        return False, "Invalid URL"

    try:
        # Detect OGC ExceptionReport (invalid request)
        response = requests.get(url, allow_redirects=True, timeout=5)
        if response.status_code != 200:
            return False, f"HTTP response status code: {response.status_code}"
        else:
            text = response.text
            if "ExceptionReport" in text or "ExceptionText" in text:
                return False, "Invalid CRS URL"
            return True, "Valid CRS URL"

    except requests.ConnectionError:
        # No internet or server unreachable
        return False, "No internet connection or cannot reach server."

    except requests.Timeout:
        return False, "Request timed out."

    except requests.RequestException:
        return False, "Something went wrong with the request :("


def get_url_status(url, parent=None):

    response = _is_url_responsive(url)
    if response[0]:
        QMessageBox.information(
            parent,
            "Information",
            f"{response[1]}",
        )
    else:
        QMessageBox.warning(
            parent,
            "Warning",
            f"{response[1]}",
        )
