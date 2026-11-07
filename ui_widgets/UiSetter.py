from __future__ import annotations
import json
from typing import TYPE_CHECKING

from ..models.top_level import ResourceConfigTemplate, ServerLimitsConfig
from ..models.top_level.ResourceConfigTemplate import (
    ResourceTypesEnum,
    ResourceVisibilityEnum,
)
from ..models.top_level.ServerConfig import ServerOnExceedEnum, ServerOptionalBoolsEnum
from ..models.top_level.MetadataConfig import MetadataKeywordTypeEnum, MetadataRoleEnum
from ..models.top_level.providers.records import (
    CrsAuthorities,
    Languages,
    ProviderTypes,
    TrsAuthorities,
)

from ..models.top_level.utils import (
    STRING_SEPARATOR,
)

from .utils import set_combo_box_value_from_data

from .ui_setter_utils import (
    clear_layout,
    create_rect_layer_from_bbox,
    fill_combo_box,
    pack_locales_data_into_list,
    pack_list_data_into_list_widget,
    get_default_language,
)
from .utils import get_widget_text_value, reset_widget


from qgis.PyQt.QtGui import QIntValidator, QDoubleValidator
from qgis.PyQt.QtCore import (
    Qt,
)
from qgis.PyQt.QtWidgets import QMessageBox

# make imports optional for pytests
try:
    from qgis.gui import QgsMapCanvas
    from qgis.core import (
        QgsRasterLayer,
        QgsCoordinateReferenceSystem,
    )
except:
    pass # nosec

if TYPE_CHECKING:
    # preserve type checking, but don't import in runtime to avoid circular import
    from ..pygeoapi_config_dialog import PygeoapiConfigDialog
    from ..models.ConfigData import ConfigData


class UiSetter:

    dialog: PygeoapiConfigDialog

    def __init__(self, dialog: PygeoapiConfigDialog):
        self.dialog = dialog

    def set_ui_from_data(self):
        """Set values for all main UI tabs from ConfigData."""
        config_data: ConfigData = self.dialog.config_data

        # bind
        self.dialog.lineEditHost.setText(config_data.server.bind.host)
        self.dialog.lineEditPort.setText(str(config_data.server.bind.port))

        # gzip
        set_combo_box_value_from_data(
            combo_box=self.dialog.comboBoxGzip,
            value=(
                str(config_data.server.gzip.value) if config_data.server.gzip else None
            ),
        )

        # pretty print
        set_combo_box_value_from_data(
            combo_box=self.dialog.comboBoxPretty,
            value=(
                str(config_data.server.pretty_print.value)
                if config_data.server.pretty_print
                else None
            ),
        )

        # admin
        set_combo_box_value_from_data(
            combo_box=self.dialog.comboBoxAdmin,
            value=(
                str(config_data.server.admin.value)
                if config_data.server.admin
                else None
            ),
        )

        # cors
        set_combo_box_value_from_data(
            combo_box=self.dialog.comboBoxCors,
            value=(
                str(config_data.server.cors.value) if config_data.server.cors else None
            ),
        )

        # mimetype
        set_combo_box_value_from_data(
            combo_box=self.dialog.comboBoxMime,
            value=config_data.server.mimetype,
        )

        # encoding
        set_combo_box_value_from_data(
            combo_box=self.dialog.comboBoxEncoding,
            value=config_data.server.encoding,
        )

        # templates
        if config_data.server.templates:
            self.dialog.lineEditTemplatesPath.setText(config_data.server.templates.path)
            self.dialog.lineEditTemplatesStatic.setText(
                config_data.server.templates.static
            )
        else:
            self.dialog.lineEditTemplatesPath.setText("")
            self.dialog.lineEditTemplatesStatic.setText("")

        # manager (only for display, data is kept without changes)
        config_data_server_manager = config_data.server.manager or {}
        pack_list_data_into_list_widget(
            (
                [str(json.dumps(config_data_server_manager))]
                if len(config_data_server_manager) > 0
                else []
            ),
            self.dialog.listWidgetServerManager,
        )

        # ogc schemas location
        ogc_schemas_location = config_data.server.ogc_schemas_location or ""
        self.dialog.lineEditServerOgcSchemasLocation.setText(ogc_schemas_location)

        # icon
        icon = config_data.server.icon or ""
        self.dialog.lineEditServerIcon.setText(icon)

        # logo
        logo = config_data.server.logo or ""
        self.dialog.lineEditServerLogo.setText(logo)

        # locale_dir
        locale_dir = config_data.server.locale_dir or ""
        self.dialog.lineEditServerLocaleDir.setText(locale_dir)

        # api_rules
        config_data_server_api_rules = config_data.server.api_rules or {}
        pack_list_data_into_list_widget(
            (
                [str(json.dumps(config_data_server_api_rules))]
                if len(config_data_server_api_rules) > 0
                else []
            ),
            self.dialog.listWidgetApiRules,
        )

        # map
        self.dialog.lineEditMapUrl.setText(config_data.server.map.url)
        self.dialog.lineEditAttribution.setText(config_data.server.map.attribution)

        self.dialog.lineEditUrl.setText(config_data.server.url)

        # language single
        set_combo_box_value_from_data(
            combo_box=self.dialog.comboBoxLangSingle,
            value=config_data.server.language,
        )

        # languages
        if config_data.server.languages is not None:
            pack_list_data_into_list_widget(
                [l for l in config_data.server.languages],
                self.dialog.listWidgetServerLangs,
            )

        # limits
        if config_data.server.limits is None:
            config_data.server.limits = ServerLimitsConfig()

        self.dialog.spinBoxDefault.setValue(config_data.server.limits.default_items)
        self.dialog.spinBoxMax.setValue(config_data.server.limits.max_items)

        max_distance_x = config_data.server.limits.max_distance_x or ""
        self.dialog.lineEditServerLimitsMaxDistX.setText(str(max_distance_x))

        max_distance_y = config_data.server.limits.max_distance_y or ""
        self.dialog.lineEditServerLimitsMaxDistY.setText(str(max_distance_y))

        max_distance_units = config_data.server.limits.max_distance_units or ""
        self.dialog.lineEditServerLimitsMaxDistUnits.setText(str(max_distance_units))

        set_combo_box_value_from_data(
            combo_box=self.dialog.comboBoxExceed or ServerOnExceedEnum.NONE,
            value=config_data.server.limits.on_exceed,
        )

        # logging
        set_combo_box_value_from_data(
            combo_box=self.dialog.comboBoxLog,
            value=config_data.logging.level,
        )

        # logfile
        logfile = config_data.logging.logfile or ""
        self.dialog.lineEditLogfile.setText(logfile)

        # logformat
        logformat = config_data.logging.logformat or ""
        self.dialog.lineEditLogformat.setText(logformat)

        # dateformat
        dateformat = config_data.logging.dateformat or ""
        self.dialog.lineEditDateformat.setText(dateformat)

        config_data_logging_rotation = config_data.logging.rotation or {}
        pack_list_data_into_list_widget(
            (
                [str(json.dumps(config_data_logging_rotation))]
                if len(config_data_logging_rotation) > 0
                else []
            ),
            self.dialog.listWidgetLogRotation,
        )

        # metadata identification

        # DATA WITH LOCALES
        # incoming type: possible list of strings or dictionary
        # limitation: even if YAML had just a list of strings, it will be interpreted here as "en" locale by default

        default_language = get_default_language(config_data)

        # title
        pack_locales_data_into_list(
            config_data.metadata.identification.title,
            self.dialog.listWidgetMetadataIdTitle,
            default_language,
        )

        # description
        pack_locales_data_into_list(
            config_data.metadata.identification.description,
            self.dialog.listWidgetMetadataIdDescription,
            default_language,
        )

        # keywords
        pack_locales_data_into_list(
            config_data.metadata.identification.keywords,
            self.dialog.listWidgetMetadataIdKeywords,
            default_language,
        )
        set_combo_box_value_from_data(
            combo_box=self.dialog.comboBoxMetadataIdKeywordsType,
            value=config_data.metadata.identification.keywords_type,
        )
        self.dialog.lineEditMetadataIdTerms.setText(
            config_data.metadata.identification.terms_of_service
        )
        self.dialog.lineEditMetadataIdUrl.setText(
            config_data.metadata.identification.url
        )

        # metadata license
        self.dialog.lineEditMetadataLicenseName.setText(
            config_data.metadata.license.name
        )
        self.dialog.lineEditMetadataLicenseUrl.setText(config_data.metadata.license.url)

        # metadata provider
        self.dialog.lineEditMetadataProviderName.setText(
            config_data.metadata.provider.name
        )
        self.dialog.lineEditMetadataProviderUrl.setText(
            config_data.metadata.provider.url
        )

        # metadata contact
        self.dialog.lineEditMetadataContactName.setText(
            config_data.metadata.contact.name
        )
        self.dialog.lineEditMetadataContactPosition.setText(
            config_data.metadata.contact.position
        )
        self.dialog.lineEditMetadataContactAddress.setText(
            config_data.metadata.contact.address
        )
        self.dialog.lineEditMetadataContactCity.setText(
            config_data.metadata.contact.city
        )
        self.dialog.lineEditMetadataContactState.setText(
            config_data.metadata.contact.stateorprovince
        )
        self.dialog.lineEditMetadataContactPostal.setText(
            config_data.metadata.contact.postalcode
        )
        self.dialog.lineEditMetadataContactCountry.setText(
            config_data.metadata.contact.country
        )
        self.dialog.lineEditMetadataContactPhone.setText(
            config_data.metadata.contact.phone
        )
        self.dialog.lineEditMetadataContactFax.setText(config_data.metadata.contact.fax)
        self.dialog.lineEditMetadataContactEmail.setText(
            config_data.metadata.contact.email
        )
        self.dialog.lineEditMetadataContactUrl.setText(config_data.metadata.contact.url)
        self.dialog.lineEditMetadataContactHours.setText(
            config_data.metadata.contact.hours
        )
        self.dialog.lineEditMetadataContactInstructions.setText(
            config_data.metadata.contact.instructions
        )
        set_combo_box_value_from_data(
            combo_box=self.dialog.comboBoxMetadataContactRole,
            value=config_data.metadata.contact.role,
        )

        # collections
        self.refresh_resources_list_ui()

    def refresh_resources_list_ui(self):
        """Refresh ListWidget with resources from ConfigData."""
        self.dialog.model.setStringList(
            [k for k, _ in self.dialog.config_data.resources.items()]
        )
        self.dialog.proxy.setSourceModel(self.dialog.model)
        self.dialog.listViewCollection.setModel(self.dialog.proxy)

    def set_resource_ui_from_data(self, res_data: ResourceConfigTemplate):
        """Set values for Resource UI from resource data."""
        dialog = self.dialog
        config_data: ConfigData = self.dialog.config_data

        # first, reset some fields to defaults (e.g. for data setting, or optional - they might not have a new value to overwrite it)
        # data entry fields
        dialog.addResTitleLineEdit.setText("")
        dialog.addResDescriptionLineEdit.setText("")
        dialog.addResKeywordsLineEdit.setText("")

        dialog.addResLinksTypeLineEdit.setText("")
        dialog.addResLinksRelLineEdit.setText("")
        dialog.addResLinksHrefLineEdit.setText("")
        dialog.addResLinksTitleLineEdit.setText("")
        dialog.addResLinkshreflangComboBox.setCurrentIndex(0)
        dialog.addResLinksLengthLineEdit.setText("")

        # optional temporal extents
        dialog.lineEditResExtentsTemporalBegin.setText("")
        dialog.lineEditResExtentsTemporalEnd.setText("")
        dialog.comboBoxResExtentsTemporalTrs.setCurrentIndex(0)

        # alias
        dialog.lineEditResAlias.setText(dialog.current_res_name)

        # type
        set_combo_box_value_from_data(
            combo_box=dialog.comboBoxResType,
            value=res_data.type,
        )

        # data with locales
        default_language = get_default_language(config_data)

        # title
        pack_locales_data_into_list(
            res_data.title, dialog.listWidgetResTitle, default_language
        )

        # description
        pack_locales_data_into_list(
            res_data.description, dialog.listWidgetResDescription, default_language
        )

        # keywords
        pack_locales_data_into_list(
            res_data.keywords, dialog.listWidgetResKeywords, default_language
        )

        # visibility
        set_combo_box_value_from_data(
            combo_box=dialog.comboBoxResVisibility,
            value=res_data.visibility or ResourceVisibilityEnum.NONE,
        )

        # spatial bbox
        dialog.lineEditResExtentsSpatialXMin.setText(
            str(res_data.extents.spatial.bbox[0])
        )
        dialog.lineEditResExtentsSpatialYMin.setText(
            str(res_data.extents.spatial.bbox[1])
        )
        dialog.lineEditResExtentsSpatialXMax.setText(
            str(res_data.extents.spatial.bbox[2])
        )
        dialog.lineEditResExtentsSpatialYMax.setText(
            str(res_data.extents.spatial.bbox[3])
        )

        # spatial CRS authority
        set_combo_box_value_from_data(
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

            # temporal trs
            set_combo_box_value_from_data(
                combo_box=dialog.comboBoxResExtentsTemporalTrs,
                value=res_data.extents.temporal.trs,
            )
        else:
            dialog.lineEditResExtentsTemporalBegin.setText("")
            dialog.lineEditResExtentsTemporalEnd.setText("")

        # links
        res_data_links = (
            res_data.links or []
        )  # make sure to set UI even if it's an empty value
        pack_list_data_into_list_widget(
            (
                [
                    [l.type, l.rel, l.href, l.title, l.hreflang, l.length]
                    for l in res_data_links
                ]
                if len(res_data_links) > 0
                else []
            ),
            dialog.listWidgetResLinks,
        )

        # linked-data
        res_data_linked__data = (
            res_data.linked__data or {}
        )  # make sure to set UI even if it's an empty value
        pack_list_data_into_list_widget(
            (
                [str(json.dumps(res_data_linked__data))]
                if len(res_data_linked__data) > 0
                else []
            ),
            dialog.listWidgetResLinkedData,
        )

        # providers
        self.set_providers_ui_from_data(res_data)

    def set_providers_ui_from_data(self, res_data: ResourceConfigTemplate):
        """Setting provider data separately, to not refresh entire UI when adding a provider.
        Resreshing all when adding a provider can lead to loosing other unsaved data from the Resource UI.
        """
        dialog = self.dialog

        data_lists = []
        read_only_data_lists = []
        for p in res_data.providers:

            if isinstance(p, dict):  # provider type not supported yet
                read_only_data_lists.append(str(json.dumps(p)))
            else:

                data_chunk: list = p.pack_data_to_list()
                data_lists.append(data_chunk)

        pack_list_data_into_list_widget(
            data_lists,
            dialog.listWidgetResProvider,
        )
        pack_list_data_into_list_widget(
            read_only_data_lists,
            dialog.listWidgetResReadOnlyProviders,
        )

    def customize_ui_on_launch(self):
        """Pre-fill ComboBoxes, assign validators to LineEdits where needed."""
        dialog = self.dialog
        config_data: ConfigData = dialog.config_data

        # add default values to the main UI
        fill_combo_box(dialog.comboBoxLangSingle, Languages.NONE)
        fill_combo_box(dialog.comboBoxExceed, ServerOnExceedEnum.NONE)
        fill_combo_box(dialog.comboBoxLog, config_data.logging.level)
        fill_combo_box(
            dialog.comboBoxMetadataIdKeywordsType,
            MetadataKeywordTypeEnum.NONE,
        )
        fill_combo_box(
            dialog.comboBoxMetadataContactRole,
            MetadataRoleEnum.NONE,
        )
        fill_combo_box(dialog.comboBoxGzip, ServerOptionalBoolsEnum.NONE)
        fill_combo_box(dialog.comboBoxPretty, ServerOptionalBoolsEnum.NONE)
        fill_combo_box(dialog.comboBoxAdmin, ServerOptionalBoolsEnum.NONE)
        fill_combo_box(dialog.comboBoxCors, ServerOptionalBoolsEnum.NONE)

        # add default values to the Resource UI
        fill_combo_box(
            dialog.comboBoxResType,
            ResourceTypesEnum.COLLECTION,
        )
        fill_combo_box(
            dialog.comboBoxResVisibility,
            ResourceVisibilityEnum.NONE,  # mock value, as default is None
        )
        fill_combo_box(
            dialog.comboBoxResExtentsSpatialCrsType,
            CrsAuthorities.OGC13,
        )
        fill_combo_box(
            dialog.comboBoxResExtentsTemporalTrs,
            TrsAuthorities.NONE,
        )

        fill_combo_box(
            dialog.comboBoxResProviderType,
            ProviderTypes.FEATURE,  # mock value to get type
        )

        fill_combo_box(
            self.dialog.addResLinkshreflangComboBox,
            Languages.NONE,  # mock value, as default is None. Only for setting data - not actual resource value
        )

        # set validators for some fields
        # resource bbox
        self.dialog.lineEditResExtentsSpatialXMin.setValidator(QDoubleValidator())
        self.dialog.lineEditResExtentsSpatialYMin.setValidator(QDoubleValidator())
        self.dialog.lineEditResExtentsSpatialXMax.setValidator(QDoubleValidator())
        self.dialog.lineEditResExtentsSpatialYMax.setValidator(QDoubleValidator())
        # regex_bbox = QRegularExpression(r"-?\d+(\.\d+)?,-?\d+(\.\d+)?,-?\d+(\.\d+)?,-?\d+(\.\d+)?")
        # validator_bbox = QRegularExpressionValidator(regex_bbox)
        # self.dialog.lineEditResExtentsSpatialBbox.setValidator(validator_bbox)

        # resource content size
        self.dialog.addResLinksLengthLineEdit.setValidator(QIntValidator())

    def setup_map_widget(self):
        try:  # using qgis imports, so we should ignore for pytests
            dialog = self.dialog

            # Define base tile layer (OSM)
            urlWithParams = (
                "type=xyz&url=https://tile.openstreetmap.org/{z}/{x}/{y}.png"
            )
            dialog.bbox_base_layer = QgsRasterLayer(
                urlWithParams, "OpenStreetMap", "wms"
            )

            # Create QgsMapCanvas with OSM layer
            dialog.bbox_map_canvas = QgsMapCanvas()
            crs = QgsCoordinateReferenceSystem("EPSG:4326")
            dialog.bbox_map_canvas.setDestinationCrs(crs)
            dialog.bbox_map_canvas.setCanvasColor(Qt.GlobalColor.white)
            dialog.bbox_map_canvas.setLayers([dialog.bbox_base_layer])
            dialog.bbox_map_canvas.zoomToFullExtent()
            # self.canvas.setExtent(layer.extent(), True)
            # self.canvas.refreshAllLayers()

            # Add QgsMapCanvas as a widget to the Resource Tab
            clear_layout(dialog.bboxMapPlaceholder)
            dialog.bboxMapPlaceholder.addWidget(dialog.bbox_map_canvas)
        except NameError:
            pass

    def preview_resource(self, model_index: "QModelIndex" = None):
        dialog = self.dialog

        # if called as a generic preview, no selected collection
        if not model_index:
            dialog.lineEditTitle.setText("")
            dialog.lineEditDescription.setText("")
            self.setup_map_widget()

            dialog.groupBoxCollectionLoaded.hide()
            dialog.groupBoxCollectionSelect.show()
            dialog.groupBoxCollectionPreview.show()

            dialog.current_res_name = ""
            return

        dialog.current_res_name = model_index.data()

        # do nothing, if resource is unsupported
        if isinstance(dialog.config_data.resources[dialog.current_res_name], dict):
            QMessageBox.warning(
                self.dialog,
                "Message",
                f"Preview is not supported for the Resource type '{dialog.config_data.resources[dialog.current_res_name].get('type')}'.",
            )
            return

        # hide detailed collection UI, show preview
        dialog.groupBoxCollectionLoaded.hide()
        dialog.groupBoxCollectionSelect.show()
        dialog.groupBoxCollectionPreview.show()

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

        dialog.bbox_extents_layer = create_rect_layer_from_bbox(bbox)
        dialog.bbox_map_canvas.setLayers(
            [dialog.bbox_extents_layer, dialog.bbox_base_layer]
        )
        # self.bbox_map_canvas.zoomToFullExtent()
        dialog.bbox_map_canvas.setExtent(dialog.bbox_extents_layer.extent(), True)
        # self.canvas.refreshAllLayers()

    def select_listcollection_item_by_text(self, target_text: str):
        dialog = self.dialog

        model = dialog.listViewCollection.model()
        for row in range(model.rowCount()):
            index = model.index(row, 0)
            if model.data(index) == target_text:
                dialog.listViewCollection.setCurrentIndex(index)
                break

    def _lang_entry_exists_in_list_widget(
        self, list_widget, locale, punctuation=True
    ) -> bool:
        for i in range(list_widget.count()):
            if punctuation:
                if list_widget.item(i).text().startswith(f"{locale}: "):
                    QMessageBox.warning(
                        self.dialog,
                        "Message",
                        f"Data entry in selected language already exists: {locale}",
                    )
                    return True
            else:
                if list_widget.item(i).text().startswith(locale):
                    QMessageBox.warning(
                        self.dialog,
                        "Message",
                        f"Data entry in selected language already exists: {locale}",
                    )
                    return True

        return False

    def add_listwidget_element_from_lineedit(
        self,
        *,
        line_edit_widget,
        list_widget,
        locale_combobox=None,
        allow_repeated_locale=True,
        sort=True,
    ):
        """Take the content of LineEdit and add it as a new List entry."""

        dialog = self.dialog
        text = line_edit_widget.text().strip() if line_edit_widget else ""
        if (line_edit_widget and text) or not line_edit_widget:

            text_to_print = text
            if locale_combobox and line_edit_widget:
                # get text with locale
                locale = locale_combobox.currentText()
                text_to_print = f"{locale}: {text}"

                # check if repeated language entries are allowed
                if allow_repeated_locale or not self._lang_entry_exists_in_list_widget(
                    list_widget, locale
                ):
                    list_widget.addItem(text_to_print)
                    line_edit_widget.clear()

            elif (
                locale_combobox and not line_edit_widget
            ):  # if locale box is the only text to use: don't wrap in extra punctuation
                locale = locale_combobox.currentText()
                text_to_print = locale

                # check if repeated language entries are allowed
                if allow_repeated_locale or not self._lang_entry_exists_in_list_widget(
                    list_widget, locale, False
                ):
                    list_widget.addItem(text_to_print)

            else:
                list_widget.addItem(text_to_print)
                line_edit_widget.clear()

            # sort the content
            if sort:
                list_widget.model().sort(0)

    def add_listwidget_element_from_multi_widgets(
        self,
        *,
        line_widgets_mandatory: list,
        line_widgets_optional: list,
        list_widget,
        sort=False,
    ):
        """Add new QListWidget entry from combined data from several widgets (e.g. Providers, Links)."""
        dialog = self.dialog

        final_text = ""
        mandatory_fields_count = len(line_widgets_mandatory)
        for i, widget in enumerate(line_widgets_mandatory + line_widgets_optional):
            text = get_widget_text_value(widget)

            # check if the field is in a 'mandatory' list and empty
            if i < mandatory_fields_count and not text:
                QMessageBox.warning(dialog, "Warning", "Mandatory field is empty")
                return

            # add separator if not the first value
            if len(final_text) > 0:
                final_text += STRING_SEPARATOR
            final_text += text
            reset_widget(widget)

        list_widget.addItem(final_text)

        # sort the content
        if sort:
            list_widget.model().sort(0)

    def delete_list_widget_selected_item(self, list_widget):
        """Delete selected List item from widget."""
        selected_index = list_widget.currentRow()
        if selected_index >= 0:
            list_widget.takeItem(selected_index)
