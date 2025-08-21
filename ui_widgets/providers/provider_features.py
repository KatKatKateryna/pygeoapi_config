from PyQt5.QtWidgets import QGridLayout
from .utils import create_label_lineedit_pair, create_list_widget


def create_feature_provider_window(group_layout: QGridLayout):

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

    all_lineedits = {}

    for row_idx, (label, data_type, default, placeholder) in enumerate(rows):

        if data_type is str:
            label_widget, line_edit_widget = create_label_lineedit_pair(
                label, default, placeholder
            )
            group_layout.addWidget(label_widget, row_idx, 0)
            group_layout.addWidget(line_edit_widget, row_idx, 1)
            all_lineedits[label] = line_edit_widget

        elif data_type is list:
            list_widget = create_list_widget(
                label, "http://www.opengis.net/def/crs/OGC/1.3/CRS84"
            )
            group_layout.addWidget(list_widget.label, row_idx, 0)
            group_layout.addWidget(list_widget, row_idx, 1)
            all_lineedits[label] = list_widget

    return all_lineedits
