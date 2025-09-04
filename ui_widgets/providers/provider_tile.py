from PyQt5.QtWidgets import QGridLayout, QComboBox
from .utils import add_widgets_to_grid_by_specs


def create_tile_provider_window(
    grid_layout: QGridLayout, data_list: list[str] | None = None
):

    # label, data_type, special_widget_type, default, placeholder
    rows = [
        ("name", str, QComboBox, "", ["MVT-proxy"]),
        ("crs", list, None, "", ""),
        ("data", str, None, "", ""),
        ("options.zoom.min", int, None, "", ""),
        ("options.zoom.max", int, None, "", ""),
        ("options.schemes", list, None, "", ""),
        ("format.name", str, None, "", ""),
        ("format.mimetype", str, None, "", ""),
    ]

    return add_widgets_to_grid_by_specs(rows, grid_layout, data_list)
