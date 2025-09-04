from enum import Enum
from ..models.top_level.utils import STRING_SEPARATOR, is_valid_string

# make imports optional for pytests
try:
    from qgis.gui import QgsMapCanvas
    from qgis.core import (
        QgsRasterLayer,
        QgsVectorLayer,
        QgsFeature,
        QgsGeometry,
        QgsRectangle,
        QgsCoordinateReferenceSystem,
        QgsFillSymbol,
    )
except:
    pass


def fill_combo_box(combo_box, enum_class):
    """Set values to dropdown ComboBox, based on the values expected by the corresponding class."""

    combo_box.clear()
    for item in type(enum_class):
        combo_box.addItem(item.value)


def clear_layout(layout):
    while layout.count():
        item = layout.takeAt(0)
        widget = item.widget()
        if widget is not None:
            widget.setParent(None)
        elif item.layout() is not None:
            clear_layout(item.layout())


def create_rect_layer_from_bbox(bbox: list[float], layer_name="Rectangle"):

    xmin, ymin, xmax, ymax = bbox
    # Create memory vector layer with polygon geometry
    layer = QgsVectorLayer("Polygon?crs=EPSG:4326", layer_name, "memory")
    provider = layer.dataProvider()
    crs = QgsCoordinateReferenceSystem("EPSG:4326")
    layer.setCrs(crs)

    # Create rectangular geometry from bbox
    rect = QgsRectangle(xmin, ymin, xmax, ymax)
    geom = QgsGeometry.fromRect(rect)

    # Create feature and assign geometry
    feature = QgsFeature()
    feature.setGeometry(geom)
    provider.addFeatures([feature])

    # Update layer
    layer.updateExtents()
    _apply_red_transparent_style(layer)

    # QgsProject.instance().addMapLayer(layer)
    return layer


def _apply_red_transparent_style(layer):
    # Create a fill symbol with red color and 50% transparency
    symbol = QgsFillSymbol.createSimple(
        {
            "color": "255,0,0,80",  # Red fill with 128/255 alpha (50% transparent)
            "outline_color": "255,0,0, 128",  # Red outline
            "outline_width": "0.5",  # Outline width in mm
        }
    )

    # Apply symbol to layer renderer
    layer.renderer().setSymbol(symbol)
    layer.triggerRepaint()


def pack_locales_data_into_list(data, list_widget):
    """Use ConfigData (list of strings, dict with strings, or a single string) to fill the UI widget list."""
    list_widget.clear()

    # data can be string, list or dict (for properties like title, description, keywords)
    if isinstance(data, str):
        if is_valid_string(data):
            value = f"en: {data}"
            list_widget.addItem(value)
            return

    for key in data:
        if isinstance(data, dict):
            local_key_content = data[key]
            if isinstance(local_key_content, str):
                if is_valid_string(local_key_content):
                    value = f"{key}: {local_key_content}"
                    list_widget.addItem(value)
            else:  # list
                for local_key in local_key_content:
                    if is_valid_string(local_key):
                        value = f"{key}: {local_key}"
                        list_widget.addItem(value)
        elif isinstance(data, list):  # list of strings
            if is_valid_string(key):
                value = f"en: {key}"
                list_widget.addItem(value)


def pack_list_data_into_list_widget(data: list[list | str], list_widget):
    list_widget.clear()

    for line_data in data:
        all_elements = []

        if isinstance(line_data, str):  # if Provider type not supported yet
            all_elements.append(line_data)

        else:
            for d in line_data:
                # convert all values to strings and joint with SEPARATOR symbol
                if d is not None:
                    if isinstance(d, list):
                        # convert list to a string without brackets (e.g. for bbox)
                        all_elements.append(",".join(d))
                    elif isinstance(d, Enum):  # e.g. Languages Enum
                        all_elements.append(str(d.value))
                    else:
                        all_elements.append(str(d))
                else:
                    all_elements.append("")

        text_entry = STRING_SEPARATOR.join(all_elements)
        list_widget.addItem(text_entry)


def select_list_widget_items_by_texts(*, list_widget, texts_to_select):
    for i in range(list_widget.count()):
        item = list_widget.item(i)
        if item.text() in texts_to_select:
            item.setSelected(True)
        else:
            item.setSelected(False)
