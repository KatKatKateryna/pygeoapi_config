from enum import Enum

from ..models.top_level.providers.records import ProviderTypes

from ..models.top_level.providers import (
    ProviderMvtProxy,
    ProviderPostgresql,
    ProviderWmsFacade,
)

from ..models.top_level.ResourceConfigTemplate import ResourceVisibilityEnum

from ..models.top_level.utils import (
    STRING_SEPARATOR,
    get_enum_value_from_string,
    is_valid_string,
)
from ..models.top_level import ResourceConfigTemplate


from PyQt5.QtGui import QRegularExpressionValidator, QIntValidator
from PyQt5.QtCore import (
    QRegularExpression,
    QFile,
    QTextStream,
    Qt,
    QStringListModel,
    QSortFilterProxyModel,
)
from PyQt5.QtWidgets import (
    QMainWindow,
    QFileDialog,
    QMessageBox,
    QDialogButtonBox,
    QApplication,
)

from qgis.gui import QgsMapCanvas
from qgis.core import (
    QgsMessageLog,
    QgsRasterLayer,
    QgsVectorLayer,
    QgsFeature,
    QgsGeometry,
    QgsRectangle,
    QgsProject,
    QgsCoordinateReferenceSystem,
    QgsFillSymbol,
)


class UiSetter:

    @staticmethod
    def set_ui_from_data(config_data, dialog):

        # bind
        dialog.lineEditHost.setText(config_data.server.bind.host)
        dialog.spinBoxPort.setValue(config_data.server.bind.port)

        # gzip
        dialog.checkBoxGzip.setChecked(config_data.server.gzip)

        # mimetype
        UiSetter._set_combo_box_value_from_data(
            combo_box=dialog.comboBoxMime,
            value=config_data.server.mimetype,
        )

        # encoding
        UiSetter._set_combo_box_value_from_data(
            combo_box=dialog.comboBoxEncoding,
            value=config_data.server.encoding,
        )

        # pretty print
        dialog.checkBoxPretty.setChecked(config_data.server.pretty_print)

        # admin
        dialog.checkBoxAdmin.setChecked(config_data.server.admin)

        # cors
        dialog.checkBoxCors.setChecked(config_data.server.cors)

        # templates
        if config_data.server.templates:
            dialog.lineEditTemplatesPath.setText(config_data.server.templates.path)
            dialog.lineEditTemplatesStatic.setText(config_data.server.templates.static)
        else:
            dialog.lineEditTemplatesPath.setText("")
            dialog.lineEditTemplatesStatic.setText("")

        # map
        dialog.lineEditMapUrl.setText(config_data.server.map.url)
        dialog.lineEditAttribution.setText(config_data.server.map.attribution)

        dialog.lineEditUrl.setText(config_data.server.url)

        # language
        UiSetter._select_list_widget_items_by_texts(
            list_widget=dialog.listWidgetLang,
            texts_to_select=config_data.server.languages,
        )

        # limits
        dialog.spinBoxDefault.setValue(config_data.server.limits.default_items)
        dialog.spinBoxMax.setValue(config_data.server.limits.max_items)

        UiSetter._set_combo_box_value_from_data(
            combo_box=dialog.comboBoxExceed,
            value=config_data.server.limits.on_exceed,
        )

        # logging
        UiSetter._set_combo_box_value_from_data(
            combo_box=dialog.comboBoxLog,
            value=config_data.logging.level,
        )

        if config_data.logging.logfile:
            dialog.lineEditLogfile.setText(config_data.logging.logfile)
        else:
            dialog.lineEditLogfile.setText("")

        if config_data.logging.logformat:
            dialog.lineEditLogformat.setText(config_data.logging.logformat)
        else:
            dialog.lineEditLogformat.setText("")

        if config_data.logging.dateformat:
            dialog.lineEditDateformat.setText(config_data.logging.dateformat)
        else:
            dialog.lineEditDateformat.setText("")

        # metadata identification

        # DATA WITH LOCALES
        # incoming type: possible list of strings or dictionary
        # limitation: even if YAML had just a list of strings, it will be interpreted here as "en" locale by default

        # title
        UiSetter._pack_locales_data_into_list(
            config_data.metadata.identification.title,
            dialog.listWidgetMetadataIdTitle,
        )

        # description
        UiSetter._pack_locales_data_into_list(
            config_data.metadata.identification.description,
            dialog.listWidgetMetadataIdDescription,
        )

        # keywords
        UiSetter._pack_locales_data_into_list(
            config_data.metadata.identification.keywords,
            dialog.listWidgetMetadataIdKeywords,
        )
        UiSetter._set_combo_box_value_from_data(
            combo_box=dialog.comboBoxMetadataIdKeywordsType,
            value=config_data.metadata.identification.keywords_type,
        )
        dialog.lineEditMetadataIdTerms.setText(
            config_data.metadata.identification.terms_of_service
        )
        dialog.lineEditMetadataIdUrl.setText(config_data.metadata.identification.url)

        # metadata license
        dialog.lineEditMetadataLicenseName.setText(config_data.metadata.license.name)
        dialog.lineEditMetadataLicenseUrl.setText(config_data.metadata.license.url)

        # metadata provider
        dialog.lineEditMetadataProviderName.setText(config_data.metadata.provider.name)
        dialog.lineEditMetadataProviderUrl.setText(config_data.metadata.provider.url)

        # metadata contact
        dialog.lineEditMetadataContactName.setText(config_data.metadata.contact.name)
        dialog.lineEditMetadataContactPosition.setText(
            config_data.metadata.contact.position
        )
        dialog.lineEditMetadataContactAddress.setText(
            config_data.metadata.contact.address
        )
        dialog.lineEditMetadataContactCity.setText(config_data.metadata.contact.city)
        dialog.lineEditMetadataContactState.setText(
            config_data.metadata.contact.stateorprovince
        )
        dialog.lineEditMetadataContactPostal.setText(
            config_data.metadata.contact.postalcode
        )
        dialog.lineEditMetadataContactCountry.setText(
            config_data.metadata.contact.country
        )
        dialog.lineEditMetadataContactPhone.setText(config_data.metadata.contact.phone)
        dialog.lineEditMetadataContactFax.setText(config_data.metadata.contact.fax)
        dialog.lineEditMetadataContactEmail.setText(config_data.metadata.contact.email)
        dialog.lineEditMetadataContactUrl.setText(config_data.metadata.contact.url)
        dialog.lineEditMetadataContactHours.setText(config_data.metadata.contact.hours)
        dialog.lineEditMetadataContactInstructions.setText(
            config_data.metadata.contact.instructions
        )
        UiSetter._set_combo_box_value_from_data(
            combo_box=dialog.comboBoxMetadataContactRole,
            value=config_data.metadata.contact.role,
        )

        # collections
        UiSetter.refresh_resources_list_ui(config_data, dialog)

    @staticmethod
    def refresh_resources_list_ui(config_data, dialog):
        """Refresh ListWidget with resources from ConfigData."""
        dialog.model.setStringList([k for k, _ in config_data.resources.items()])
        dialog.proxy.setSourceModel(dialog.model)
        dialog.listViewCollection.setModel(dialog.proxy)

    @staticmethod
    def _set_combo_box_value_from_data(*, combo_box, value):
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

    @staticmethod
    def _pack_locales_data_into_list(data, list_widget):
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

    @staticmethod
    def set_resource_ui_from_data(dialog, res_data: ResourceConfigTemplate):

        # alias
        dialog.lineEditResAlias.setText(dialog.current_res_name)

        # type
        UiSetter._set_combo_box_value_from_data(
            combo_box=dialog.comboBoxResType,
            value=res_data.type,
        )

        # title
        UiSetter._pack_locales_data_into_list(
            res_data.title,
            dialog.listWidgetResTitle,
        )

        # description
        UiSetter._pack_locales_data_into_list(
            res_data.description,
            dialog.listWidgetResDescription,
        )

        # keywords
        UiSetter._pack_locales_data_into_list(
            res_data.keywords, dialog.listWidgetResKeywords
        )

        # visibility
        UiSetter._set_combo_box_value_from_data(
            combo_box=dialog.comboBoxResVisibility,
            value=res_data.visibility or ResourceVisibilityEnum.NONE,
        )

        # spatial bbox
        bbox_str = (
            str(res_data.extents.spatial.bbox)
            .replace("[", "")
            .replace("]", "")
            .replace(" ", "")
        )
        dialog.lineEditResExtentsSpatialBbox.setText(bbox_str)

        # spatial CRS authority
        UiSetter._set_combo_box_value_from_data(
            combo_box=dialog.comboBoxResExtentsSpatialCrsType,
            value=res_data.extents.spatial.crs_authority,
        )

        # spatial crs id
        dialog.lineEditResExtentsSpatialCrs.setText(res_data.extents.spatial.crs_id)

        # temporal extents
        if res_data.extents.temporal:
            # temporal begin
            if res_data.extents.temporal.begin:
                dialog.lineEditResExtentsTemporalBegin.setText(
                    res_data.extents.temporal.begin.strftime("%Y-%m-%dT%H:%M:%SZ")
                )
            else:
                dialog.lineEditResExtentsTemporalBegin.setText("")

            # temporal end
            if res_data.extents.temporal.end:
                dialog.lineEditResExtentsTemporalEnd.setText(
                    res_data.extents.temporal.end.strftime("%Y-%m-%dT%H:%M:%SZ")
                )
            else:
                dialog.lineEditResExtentsTemporalEnd.setText("")

            # temporal end
            if res_data.extents.temporal.trs:
                dialog.lineEditResExtentsTemporalTrs.setText(
                    res_data.extents.temporal.trs
                )
            else:
                dialog.lineEditResExtentsTemporalTrs.setText("")

        # links
        UiSetter._pack_list_data_into_list_widget(
            [
                [l.type, l.rel, l.href, l.title, l.hreflang, l.length]
                for l in res_data.links
            ],
            dialog.listWidgetResLinks,
        )

        # providers
        UiSetter.set_providers_ui_from_data(dialog, res_data)

    @staticmethod
    def set_providers_ui_from_data(dialog, res_data: ResourceConfigTemplate):
        """Setting provider data separately, to not refresh entire UI when adding a provider.
        Resreshing all when adding a provider can lead to loosing other unsaved data from the Resource UI.
        """

        data_lists = []
        for p in res_data.providers:
            if isinstance(p, ProviderPostgresql):
                data_chunk = [
                    p.type.value,
                    p.name,
                    p.crs,
                    p.data.host,
                    p.data.port,
                    p.data.dbname,
                    p.data.user,
                    p.data.password,
                    p.data.search_path,
                    p.id_field,
                    p.table,
                    p.geom_field,
                ]
            elif isinstance(p, ProviderWmsFacade):
                data_chunk = [
                    p.type.value,
                    p.name,
                    p.crs,
                    p.data,
                    p.options.layer,
                    p.options.style,
                    p.options.version,
                    p.format.name,
                    p.format.mimetype,
                ]
            elif isinstance(p, ProviderMvtProxy):
                data_chunk = [
                    p.type.value,
                    p.name,
                    p.crs,
                    p.data,
                    p.options.zoom.min,
                    p.options.zoom.max,
                    p.format.name,
                    p.format.mimetype,
                ]

            data_lists.append(data_chunk)

        UiSetter._pack_list_data_into_list_widget(
            data_lists,
            dialog.listWidgetResProvider,
        )

    @staticmethod
    def _pack_list_data_into_list_widget(data: list[list], list_widget):
        list_widget.clear()

        for line_data in data:
            all_elements = []
            for d in line_data:
                # convert all values to strings and joint with SEPARATOR symbol
                if d:
                    if isinstance(d, list):
                        # convert list to a string without brackets
                        all_elements.append(",".join(d))
                    else:
                        all_elements.append(str(d))
                else:
                    all_elements.append("")

            text_entry = STRING_SEPARATOR.join(all_elements)
            list_widget.addItem(text_entry)

    @staticmethod
    def _select_list_widget_items_by_texts(*, list_widget, texts_to_select):
        for i in range(list_widget.count()):
            item = list_widget.item(i)
            if item.text() in texts_to_select:
                item.setSelected(True)
            else:
                item.setSelected(False)

    @staticmethod
    def customize_ui_on_launch(dialog):
        """Pre-fill ComboBoxes, assign validators to LineEdits where needed."""

        # add default values to the UI
        UiSetter.fill_combo_box(
            dialog.comboBoxExceed, dialog.config_data.server.limits.on_exceed
        )
        UiSetter.fill_combo_box(dialog.comboBoxLog, dialog.config_data.logging.level)
        UiSetter.fill_combo_box(
            dialog.comboBoxMetadataIdKeywordsType,
            dialog.config_data.metadata.identification.keywords_type,
        )
        UiSetter.fill_combo_box(
            dialog.comboBoxMetadataContactRole,
            dialog.config_data.metadata.contact.role,
        )

        # set validators for come fields

        # resource bbox
        regex_bbox = QRegularExpression(
            r"-?\d+(\.\d+)?,-?\d+(\.\d+)?,-?\d+(\.\d+)?,-?\d+(\.\d+)?"
        )
        validator_bbox = QRegularExpressionValidator(regex_bbox)
        dialog.lineEditResExtentsSpatialBbox.setValidator(validator_bbox)

        # resource content size
        dialog.addResLinksLengthLineEdit.setValidator(QIntValidator())

    @staticmethod
    def setup_map_widget(dialog):

        # Define base tile layer (OSM)
        urlWithParams = "type=xyz&url=https://tile.openstreetmap.org/{z}/{x}/{y}.png"
        dialog.bbox_base_layer = QgsRasterLayer(urlWithParams, "OpenStreetMap", "wms")

        # Create QgsMapCanvas with OSM layer
        dialog.bbox_map_canvas = QgsMapCanvas()
        crs = QgsCoordinateReferenceSystem("EPSG:4326")
        dialog.bbox_map_canvas.setDestinationCrs(crs)
        dialog.bbox_map_canvas.setCanvasColor(Qt.white)
        dialog.bbox_map_canvas.setLayers([dialog.bbox_base_layer])
        dialog.bbox_map_canvas.zoomToFullExtent()
        # self.canvas.setExtent(layer.extent(), True)
        # self.canvas.refreshAllLayers()

        # Add QgsMapCanvas as a widget to the Resource Tab
        UiSetter.clear_layout(dialog.bboxMapPlaceholder)
        dialog.bboxMapPlaceholder.addWidget(dialog.bbox_map_canvas)

    @staticmethod
    def preview_resource(dialog, model_index: "QModelIndex" = None):

        # if called as a generic preview, no selected collection
        if not model_index:
            dialog.lineEditTitle.setText("")
            dialog.lineEditDescription.setText("")
            UiSetter.setup_map_widget(dialog)

            dialog.groupBoxCollectionLoaded.hide()
            dialog.groupBoxCollectionSelect.show()
            dialog.groupBoxCollectionPreview.show()
            return

        # hide detailed collection UI, show preview
        dialog.groupBoxCollectionLoaded.hide()
        dialog.groupBoxCollectionSelect.show()
        dialog.groupBoxCollectionPreview.show()

        dialog.current_res_name = model_index.data()

        # If title is a dictionary, use the first (default) value
        title = dialog.config_data.resources[dialog.current_res_name].title
        if isinstance(title, dict):
            title = next(iter(title.values()), "")
        dialog.lineEditTitle.setText(title)

        # If description is a dictionary, use the first (default) value
        description = dialog.config_data.resources[dialog.current_res_name].description
        if isinstance(description, dict):
            description = next(iter(description.values()), "")
        dialog.lineEditDescription.setText(description)

        # load bbox
        bbox = dialog.config_data.resources[
            dialog.current_res_name
        ].extents.spatial.bbox

        dialog.bbox_extents_layer = UiSetter.create_rect_layer_from_bbox(bbox)
        dialog.bbox_map_canvas.setLayers(
            [dialog.bbox_extents_layer, dialog.bbox_base_layer]
        )
        # self.bbox_map_canvas.zoomToFullExtent()
        dialog.bbox_map_canvas.setExtent(dialog.bbox_extents_layer.extent(), True)
        # self.canvas.refreshAllLayers()

    @staticmethod
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
        UiSetter.apply_red_transparent_style(layer)

        # QgsProject.instance().addMapLayer(layer)
        return layer

    @staticmethod
    def apply_red_transparent_style(layer):
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

    @staticmethod
    def select_listcollection_item_by_text(dialog, target_text: str):
        model = dialog.listViewCollection.model()
        for row in range(model.rowCount()):
            index = model.index(row, 0)
            if model.data(index) == target_text:
                dialog.listViewCollection.setCurrentIndex(index)
                break

    @staticmethod
    def clear_layout(layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
            elif item.layout() is not None:
                UiSetter.clear_layout(item.layout())

    @staticmethod
    def fill_combo_box(combo_box, enum_class):
        """Set values to dropdown ComboBox, based on the values expected by the corresponding class."""

        combo_box.clear()
        for item in type(enum_class):
            combo_box.addItem(item.value)

    @staticmethod
    def setup_resouce_loaded_ui(dialog, res_data: ResourceConfigTemplate):

        UiSetter.fill_combo_box(
            dialog.comboBoxResType,
            res_data.type,
        )
        UiSetter.fill_combo_box(
            dialog.comboBoxResVisibility,
            res_data.visibility
            or ResourceVisibilityEnum.NONE,  # mock value, as default is None
        )
        UiSetter.fill_combo_box(
            dialog.comboBoxResExtentsSpatialCrsType,
            res_data.extents.spatial.crs_authority,
        )
        UiSetter.fill_combo_box(
            dialog.comboBoxResProviderType,
            ProviderTypes.FEATURE,  # mock value if we don't yet have an object to get the value from
        )
