from PyQt5.QtWidgets import QGridLayout
from .utils import add_widgets_to_grid_by_specs


def create_tile_provider_window(grid_layout: QGridLayout):

    rows = [
        ("name", str, "MVT-proxy", ""),
        ("crs", str, "", ""),
        ("data", str, "", ""),
        ("zoom min", int, "", ""),
        ("zoom max", int, "", ""),
        ("schemes", list, "", ""),
        ("format.name", str, "", ""),
        ("format.mimetype", str, "", ""),
    ]

    return add_widgets_to_grid_by_specs(rows, grid_layout)
