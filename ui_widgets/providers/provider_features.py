from PyQt5.QtWidgets import QGridLayout
from .utils import add_widgets_to_grid_by_specs


def create_feature_provider_window(grid_layout: QGridLayout):

    rows = [
        ("name", str, "PostgreSQL", ""),
        ("crs", list, "", ""),
        (
            "storage_crs",
            str,
            "",
            "(optional) http://www.opengis.net/def/crs/OGC/1.3/CRS84",
        ),
        ("host", str, "", ""),
        ("port", str, "", ""),
        ("dbname", str, "", ""),
        ("user", str, "", ""),
        ("password", str, "", ""),
        ("search_path", str, "", "e.g. 'osm, public'"),
        ("id_field", str, "", ""),
        ("table", str, "", ""),
        ("geom_field", str, "", ""),
    ]

    return add_widgets_to_grid_by_specs(rows, grid_layout)
