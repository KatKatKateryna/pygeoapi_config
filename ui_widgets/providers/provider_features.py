from PyQt5.QtWidgets import QGridLayout, QLineEdit, QComboBox
from .utils import add_widgets_to_grid_by_specs


def create_feature_provider_window(
    grid_layout: QGridLayout, data_list: list[str] | None = None
):
    # label, data_type, special_widget_type, default, placeholder
    rows = [
        ("name", str, QComboBox, "", ["PostgreSQL"]),
        ("crs", list, None, "", ""),
        (
            "storage_crs",
            str,
            None,
            "",
            "(optional) http://www.opengis.net/def/crs/OGC/1.3/CRS84",
        ),
        ("data.host", str, None, "", ""),
        ("data.port", str, None, "", ""),
        ("data.dbname", str, None, "", ""),
        ("data.user", str, None, "", ""),
        ("data.password", str, None, "", ""),
        ("data.search_path", str, None, "", "e.g. 'osm, public'"),
        ("id_field", str, None, "", ""),
        ("table", str, None, "", ""),
        ("geom_field", str, None, "", ""),
    ]

    return add_widgets_to_grid_by_specs(rows, grid_layout, data_list)
