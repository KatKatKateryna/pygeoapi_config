from PyQt5.QtWidgets import QGridLayout
from .utils import add_widgets_to_grid_by_specs


def create_feature_provider_window(
    grid_layout: QGridLayout, data_list: list[str] | None = None
):

    rows = [
        ("name", str, "PostgreSQL", ""),
        ("crs", list, "", ""),
        (
            "storage_crs",
            str,
            "",
            "(optional) http://www.opengis.net/def/crs/OGC/1.3/CRS84",
        ),
        ("data.host", str, "", ""),
        ("data.port", str, "", ""),
        ("data.dbname", str, "", ""),
        ("data.user", str, "", ""),
        ("data.password", str, "", ""),
        ("data.search_path", str, "", "e.g. 'osm, public'"),
        ("id_field", str, "", ""),
        ("table", str, "", ""),
        ("geom_field", str, "", ""),
    ]

    return add_widgets_to_grid_by_specs(rows, grid_layout, data_list)
