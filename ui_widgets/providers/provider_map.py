from PyQt5.QtWidgets import QGridLayout
from .utils import add_widgets_to_grid_by_specs


def create_map_provider_window(
    grid_layout: QGridLayout, data_list: list[str] | None = None
):

    rows = [
        ("name", str, "WMSFacade", ""),
        ("crs", str, "", ""),
        ("data", str, "", ""),
        ("layer", str, "", ""),
        ("style", str, "", ""),
        ("version", str, "", ""),
        ("format.name", str, "", ""),
        ("format.mimetype", str, "", ""),
    ]

    return add_widgets_to_grid_by_specs(rows, grid_layout, data_list)
