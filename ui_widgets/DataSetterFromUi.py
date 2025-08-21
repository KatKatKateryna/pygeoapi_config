from __future__ import annotations
from typing import TYPE_CHECKING

from datetime import datetime

from .utils import get_widget_text_value

from .data_from_ui_setter_utils import (
    unpack_locales_values_list_to_dict,
    unpack_listwidget_values_to_sublists,
)
from ..models.top_level.utils import bbox_from_list

from ..models.top_level import (
    ResourceLinkTemplate,
    ResourceTemporalConfig,
    ResourceTypesEnum,
    ResourceVisibilityEnum,
    LoggingLevel,
    MetadataKeywordTypeEnum,
    MetadataRoleEnum,
    ServerOnExceedEnum,
    ServerTemplatesConfig,
)
from ..models.top_level.providers import (
    ProviderMvtProxy,
    ProviderPostgresql,
    ProviderWmsFacade,
)
from ..models.top_level.providers.records import (
    Languages,
    ProviderTypes,
    TrsAuthorities,
)

from ..models.top_level.utils import (
    InlineList,
    get_enum_value_from_string,
    is_valid_string,
)


if TYPE_CHECKING:
    # preserve type checking, but don't import in runtime to avoid circular import
    from ..pygeoapi_config_dialog import PygeoapiConfigDialog
    from ..models.ConfigData import ConfigData


class DataSetterFromUi:

    dialog: PygeoapiConfigDialog

    def __init__(self, dialog: PygeoapiConfigDialog):
        self.dialog = dialog

    def set_data_from_ui(self):
        """Collect all data from the main UI tabs and save to ConfigData."""
        dialog: PygeoapiConfigDialog = self.dialog
        config_data: ConfigData = dialog.config_data

        # bind
        config_data.server.bind.host = dialog.lineEditHost.text()
        config_data.server.bind.port = dialog.spinBoxPort.value()

        # gzip
        config_data.server.gzip = dialog.checkBoxGzip.isChecked()

        # pretty print
        config_data.server.pretty_print = dialog.checkBoxPretty.isChecked()

        # admin
        config_data.server.admin = dialog.checkBoxAdmin.isChecked()

        # cors
        config_data.server.cors = dialog.checkBoxCors.isChecked()

        # templates
        if is_valid_string(dialog.lineEditTemplatesPath.text()) or is_valid_string(
            dialog.lineEditTemplatesStatic.text()
        ):
            config_data.server.templates = ServerTemplatesConfig()
        else:
            config_data.server.templates = None

        if config_data.server.templates:
            config_data.server.templates.path = dialog.lineEditTemplatesPath.text()
            config_data.server.templates.static = dialog.lineEditTemplatesStatic.text()

        # map
        config_data.server.map.url = dialog.lineEditMapUrl.text()
        config_data.server.map.attribution = dialog.lineEditAttribution.text()

        # url
        config_data.server.url = dialog.lineEditUrl.text()

        # language
        config_data.server.languages = []
        for i in range(dialog.listWidgetLang.count()):
            item = dialog.listWidgetLang.item(i)
            if item.isSelected():
                config_data.server.languages.append(item.text())

        # limits
        config_data.server.limits.default_items = dialog.spinBoxDefault.value()
        config_data.server.limits.max_items = dialog.spinBoxMax.value()

        config_data.server.limits.on_exceed = get_enum_value_from_string(
            ServerOnExceedEnum, dialog.comboBoxExceed.currentText()
        )

        # logging
        config_data.logging.level = get_enum_value_from_string(
            LoggingLevel, dialog.comboBoxLog.currentText()
        )

        if is_valid_string(dialog.lineEditLogfile.text()):
            config_data.logging.logfile = dialog.lineEditLogfile.text()
        else:
            config_data.logging.logfile = None

        if is_valid_string(dialog.lineEditLogformat.text()):
            config_data.logging.logformat = dialog.lineEditLogformat.text()
        else:
            config_data.logging.logformat = None

        if is_valid_string(dialog.lineEditDateformat.text()):
            config_data.logging.dateformat = dialog.lineEditDateformat.text()
        else:
            config_data.logging.dateformat = None

        # metadata identification
        config_data.metadata.identification.title = unpack_locales_values_list_to_dict(
            dialog.listWidgetMetadataIdTitle, False
        )
        config_data.metadata.identification.description = (
            unpack_locales_values_list_to_dict(
                dialog.listWidgetMetadataIdDescription, False
            )
        )
        config_data.metadata.identification.keywords = (
            unpack_locales_values_list_to_dict(
                dialog.listWidgetMetadataIdKeywords, True
            )
        )

        config_data.metadata.identification.keywords_type = get_enum_value_from_string(
            MetadataKeywordTypeEnum, dialog.comboBoxMetadataIdKeywordsType.currentText()
        )
        config_data.metadata.identification.terms_of_service = (
            dialog.lineEditMetadataIdTerms.text()
        )
        config_data.metadata.identification.url = dialog.lineEditMetadataIdUrl.text()

        # metadata license
        config_data.metadata.license.name = dialog.lineEditMetadataLicenseName.text()
        config_data.metadata.license.url = dialog.lineEditMetadataLicenseUrl.text()

        # metadata provider
        config_data.metadata.provider.name = dialog.lineEditMetadataProviderName.text()
        config_data.metadata.provider.url = dialog.lineEditMetadataProviderUrl.text()

        # metadata contact
        config_data.metadata.contact.name = dialog.lineEditMetadataContactName.text()
        config_data.metadata.contact.position = (
            dialog.lineEditMetadataContactPosition.text()
        )
        config_data.metadata.contact.address = (
            dialog.lineEditMetadataContactAddress.text()
        )
        config_data.metadata.contact.city = dialog.lineEditMetadataContactCity.text()
        config_data.metadata.contact.stateorprovince = (
            dialog.lineEditMetadataContactState.text()
        )
        config_data.metadata.contact.postalcode = (
            dialog.lineEditMetadataContactPostal.text()
        )
        config_data.metadata.contact.country = (
            dialog.lineEditMetadataContactCountry.text()
        )
        config_data.metadata.contact.phone = dialog.lineEditMetadataContactPhone.text()
        config_data.metadata.contact.fax = dialog.lineEditMetadataContactFax.text()
        config_data.metadata.contact.email = dialog.lineEditMetadataContactEmail.text()
        config_data.metadata.contact.url = dialog.lineEditMetadataContactUrl.text()
        config_data.metadata.contact.hours = dialog.lineEditMetadataContactHours.text()
        config_data.metadata.contact.instructions = (
            dialog.lineEditMetadataContactInstructions.text()
        )
        config_data.metadata.contact.role = get_enum_value_from_string(
            MetadataRoleEnum,
            dialog.comboBoxMetadataContactRole.currentText(),
        )

    def set_resource_data_from_ui(self):
        """Collect data from Resource UI and add to ConfigData."""
        dialog: PygeoapiConfigDialog = self.dialog
        config_data: ConfigData = dialog.config_data
        res_name = dialog.current_res_name

        config_data.resources[res_name].type = get_enum_value_from_string(
            ResourceTypesEnum, dialog.comboBoxResType.currentText()
        )
        config_data.resources[res_name].title = unpack_locales_values_list_to_dict(
            dialog.listWidgetResTitle, False
        )
        config_data.resources[res_name].description = (
            unpack_locales_values_list_to_dict(dialog.listWidgetResDescription, False)
        )
        config_data.resources[res_name].keywords = unpack_locales_values_list_to_dict(
            dialog.listWidgetResKeywords, True
        )

        # visibility: if empty, ignore
        if is_valid_string(dialog.comboBoxResVisibility.currentText()):
            config_data.resources[res_name].visibility = get_enum_value_from_string(
                ResourceVisibilityEnum, dialog.comboBoxResVisibility.currentText()
            )
        else:
            config_data.resources[res_name].visibility = None

        # spatial bbox
        raw_bbox_list = [
            get_widget_text_value(x)
            for x in [
                dialog.lineEditResExtentsSpatialXMin,
                dialog.lineEditResExtentsSpatialYMin,
                dialog.lineEditResExtentsSpatialXMax,
                dialog.lineEditResExtentsSpatialYMax,
            ]
        ]
        # this loop is to not add empty decimals unnecessarily
        config_data.resources[res_name].extents.spatial.bbox = InlineList(
            bbox_from_list(raw_bbox_list)
        )

        # spatial crs
        config_data.resources[res_name].extents.spatial.crs = (
            self.get_extents_crs_from_ui(dialog)
        )

        # temporal: only initialize if any of the values are present, otherwise leave as default None
        # IGNORE trs if no other values are present
        temporal_begin = None
        temporal_end = None
        if is_valid_string(dialog.lineEditResExtentsTemporalBegin.text()):
            temporal_begin = datetime.strptime(
                dialog.lineEditResExtentsTemporalBegin.text(),
                "%Y-%m-%dT%H:%M:%SZ",
            )
        if is_valid_string(dialog.lineEditResExtentsTemporalEnd.text()):
            temporal_end = datetime.strptime(
                dialog.lineEditResExtentsTemporalEnd.text(),
                "%Y-%m-%dT%H:%M:%SZ",
            )

        if temporal_begin or temporal_end:
            config_data.resources[res_name].extents.temporal = ResourceTemporalConfig()

            config_data.resources[res_name].extents.temporal.begin = temporal_begin
            config_data.resources[res_name].extents.temporal.end = temporal_end
            config_data.resources[res_name].extents.temporal.trs = (
                get_enum_value_from_string(
                    TrsAuthorities,
                    get_widget_text_value(dialog.comboBoxResExtentsTemporalTrs),
                )
            )

        # links
        config_data.resources[res_name].links = []
        links_data_lists = unpack_listwidget_values_to_sublists(
            dialog.listWidgetResLinks, 6
        )
        for link in links_data_lists:
            new_link = ResourceLinkTemplate()
            new_link.type = link[0]
            new_link.rel = link[1]
            new_link.href = link[2]

            if is_valid_string(link[3]):
                new_link.title = link[3]
            if is_valid_string(link[4]):
                new_link.hreflang = get_enum_value_from_string(
                    Languages,
                    link[4],
                )
            if is_valid_string(link[5]):
                new_link.length = int(link[5])

            config_data.resources[res_name].links.append(new_link)

        # providers
        config_data.resources[res_name].providers = []
        providers_data_lists = unpack_listwidget_values_to_sublists(
            dialog.listWidgetResProvider
        )

        for pr in providers_data_lists:
            if len(pr) == 0:
                # unknown/failed provider
                continue

            if len(pr) == 12 and pr[0] == ProviderTypes.FEATURE.value:

                new_pr = ProviderPostgresql()
                new_pr.type = get_enum_value_from_string(ProviderTypes, pr[0])
                new_pr.name = pr[1]
                new_pr.crs = pr[2]
                new_pr.data.host = pr[3]
                new_pr.data.port = pr[4]
                new_pr.data.dbname = pr[5]
                new_pr.data.user = pr[6]
                new_pr.data.password = pr[7]
                new_pr.data.search_path = InlineList(pr[8].split(","))

                if is_valid_string(pr[9]):
                    new_pr.id_field = pr[9]
                if is_valid_string(pr[10]):
                    new_pr.table = pr[10]
                if is_valid_string(pr[11]):
                    new_pr.geom_field = pr[11]

                config_data.resources[res_name].providers.append(new_pr)

            elif len(pr) == 9 and pr[0] == ProviderTypes.MAP.value:
                new_pr = ProviderWmsFacade()
                new_pr.type = get_enum_value_from_string(ProviderTypes, pr[0])
                new_pr.name = pr[1]
                new_pr.crs = pr[2]
                new_pr.data = pr[3]
                new_pr.options.layer = pr[4]
                new_pr.options.style = pr[5]
                new_pr.options.version = pr[6]
                new_pr.format.name = pr[7]
                new_pr.format.mimetype = pr[8]

                config_data.resources[res_name].providers.append(new_pr)

            elif len(pr) == 8 and pr[0] == ProviderTypes.TILE.value:
                new_pr = ProviderMvtProxy()
                new_pr.type = get_enum_value_from_string(ProviderTypes, pr[0])
                new_pr.name = pr[1]
                new_pr.crs = pr[2]
                new_pr.data = pr[3]
                new_pr.options.zoom.min = int(pr[4])
                new_pr.options.zoom.max = int(pr[5])
                new_pr.format.name = pr[6]
                new_pr.format.mimetype = pr[7]

                config_data.resources[res_name].providers.append(new_pr)
            else:
                # unknown provider
                continue

        # change resource key to a new alias
        new_alias = dialog.lineEditResAlias.text()
        if res_name in config_data.resources:
            config_data.resources[new_alias] = config_data.resources.pop(res_name)

    def get_extents_crs_from_ui(self, dialog):
        return (
            "http://www.opengis.net/def/crs/"
            + get_widget_text_value(dialog.comboBoxResExtentsSpatialCrsType)
            + "/"
            + get_widget_text_value(dialog.lineEditResExtentsSpatialCrs)
        )

    def get_invalid_resource_ui_fields(self) -> list[str]:
        """Get list of invalid UI values in Resource UI."""

        dialog: PygeoapiConfigDialog = self.dialog
        invalid_fields = []

        if not is_valid_string(dialog.lineEditResAlias.text()):
            invalid_fields.append("alias")
        if dialog.listWidgetResTitle.count() == 0:
            invalid_fields.append("title")
        if dialog.listWidgetResDescription.count() == 0:
            invalid_fields.append("description")
        if dialog.listWidgetResKeywords.count() == 0:
            invalid_fields.append("keywords")

        try:
            raw_bbox_list = [
                get_widget_text_value(x)
                for x in [
                    dialog.lineEditResExtentsSpatialXMin,
                    dialog.lineEditResExtentsSpatialYMin,
                    dialog.lineEditResExtentsSpatialXMax,
                    dialog.lineEditResExtentsSpatialYMax,
                ]
            ]
            bbox_from_list(raw_bbox_list)
        except Exception as e:
            invalid_fields.append("spatial extents (bbox)")

        if not is_valid_string(dialog.lineEditResExtentsSpatialCrs.text()):
            invalid_fields.append("spatial extents (crs)")

        if dialog.listWidgetResProvider.count() == 0:
            invalid_fields.append("providers")

        # optional fields, but can cause crash if wrong format
        if is_valid_string(dialog.lineEditResExtentsTemporalBegin.text()):
            try:
                datetime.strptime(
                    dialog.lineEditResExtentsTemporalBegin.text(), "%Y-%m-%dT%H:%M:%SZ"
                )
            except:
                invalid_fields.append("temporal extents (begin)")

        if is_valid_string(dialog.lineEditResExtentsTemporalEnd.text()):
            try:
                datetime.strptime(
                    dialog.lineEditResExtentsTemporalEnd.text(), "%Y-%m-%dT%H:%M:%SZ"
                )
            except:
                invalid_fields.append("temporal extents (end)")

        return invalid_fields
