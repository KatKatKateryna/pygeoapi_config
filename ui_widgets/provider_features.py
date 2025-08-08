from PyQt5.QtWidgets import QGridLayout
from .utils import create_label_lineedit_pair


def create_feature_provider_window(group_layout: QGridLayout):

    rows = [
        ("name", "PostgreSQL", ""),
        ("crs", "http://www.opengis.net/def/crs/OGC/1.3/CRS84", ""),
        ("host", "", ""),
        ("port", "", ""),
        ("dbname", "", ""),
        ("user", "", ""),
        ("password", "", ""),
        ("search_path", "", "e.g. 'osm, public'"),
        ("id_field", "", "(optional)"),
        ("table", "", "(optional)"),
        ("geom_field", "", "(optional)"),
    ]

    all_lineedits = {}

    for row_idx, (label, default, placeholder) in enumerate(rows):
        label_widget, line_edit_widget = create_label_lineedit_pair(
            label, default, placeholder
        )
        group_layout.addWidget(label_widget, row_idx, 0)
        group_layout.addWidget(line_edit_widget, row_idx, 1)

        all_lineedits[label] = line_edit_widget

    return all_lineedits
