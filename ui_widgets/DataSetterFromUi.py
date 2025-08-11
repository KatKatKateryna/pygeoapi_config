from datetime import datetime

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
from ..models.top_level.providers.records import ProviderTypes

from ..models.top_level.utils import (
    STRING_SEPARATOR,
    InlineList,
    get_enum_value_from_string,
    is_valid_string,
)

from PyQt5.QtWidgets import (
    QMainWindow,
    QFileDialog,
    QMessageBox,
    QDialogButtonBox,
    QApplication,
)

from qgis.core import (
    QgsMessageLog,
)


class DataSetterFromUi:

    @staticmethod
    def set_data_from_ui(dialog):
        """Collect all data from the main UI tabs and save to ConfigData."""
        config_data = dialog.config_data
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
        config_data.metadata.identification.title = (
            DataSetterFromUi._unpack_locales_values_list_to_dict(
                dialog.listWidgetMetadataIdTitle, False
            )
        )
        config_data.metadata.identification.description = (
            DataSetterFromUi._unpack_locales_values_list_to_dict(
                dialog.listWidgetMetadataIdDescription, False
            )
        )
        config_data.metadata.identification.keywords = (
            DataSetterFromUi._unpack_locales_values_list_to_dict(
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

    @staticmethod
    def set_resource_data_from_ui(dialog):
        """Collect data from Resource UI and add to ConfigData."""
        config_data = dialog.config_data
        res_name = dialog.current_res_name

        config_data.resources[res_name].type = get_enum_value_from_string(
            ResourceTypesEnum, dialog.comboBoxResType.currentText()
        )
        config_data.resources[res_name].title = (
            DataSetterFromUi._unpack_locales_values_list_to_dict(
                dialog.listWidgetResTitle, False
            )
        )
        config_data.resources[res_name].description = (
            DataSetterFromUi._unpack_locales_values_list_to_dict(
                dialog.listWidgetResDescription, False
            )
        )
        config_data.resources[res_name].keywords = (
            DataSetterFromUi._unpack_locales_values_list_to_dict(
                dialog.listWidgetResKeywords, True
            )
        )

        # visibility: if empty, ignore
        if is_valid_string(dialog.comboBoxResVisibility.currentText()):
            config_data.resources[res_name].visibility = get_enum_value_from_string(
                ResourceVisibilityEnum, dialog.comboBoxResVisibility.currentText()
            )
        else:
            config_data.resources[res_name].visibility = None

        # spatial bbox
        raw_bbox_str = dialog.lineEditResExtentsSpatialBbox.text()
        # this loop is to not add empty decimals unnecessarily
        config_data.resources[res_name].extents.spatial.bbox = InlineList(
            DataSetterFromUi._bbox_from_string(raw_bbox_str)
        )

        # spatial crs
        config_data.resources[res_name].extents.spatial.crs = (
            "http://www.opengis.net/def/crs/"
            + dialog.comboBoxResExtentsSpatialCrsType.currentText()
            + "/"
            + dialog.lineEditResExtentsSpatialCrs.text()
        )

        # temporal: only initialize if any of the values are present, otherwise leave as default None
        if (
            is_valid_string(dialog.lineEditResExtentsTemporalBegin.text())
            or is_valid_string(dialog.lineEditResExtentsTemporalEnd.text())
            or is_valid_string(dialog.lineEditResExtentsTemporalTrs.text())
        ):
            config_data.resources[res_name].extents.temporal = ResourceTemporalConfig()
        else:
            config_data.resources[res_name].extents.temporal = None

        # if initialized or already existed:
        if config_data.resources[res_name].extents.temporal:
            if is_valid_string(dialog.lineEditResExtentsTemporalBegin.text()):
                config_data.resources[res_name].extents.temporal.begin = (
                    datetime.strptime(
                        dialog.lineEditResExtentsTemporalBegin.text(),
                        "%Y-%m-%dT%H:%M:%SZ",
                    )
                )
            else:
                config_data.resources[res_name].extents.temporal.begin = None

            if is_valid_string(dialog.lineEditResExtentsTemporalEnd.text()):
                config_data.resources[res_name].extents.temporal.end = (
                    datetime.strptime(
                        dialog.lineEditResExtentsTemporalEnd.text(),
                        "%Y-%m-%dT%H:%M:%SZ",
                    )
                )
            else:
                config_data.resources[res_name].extents.temporal.end = None

            if is_valid_string(dialog.lineEditResExtentsTemporalTrs.text()):
                config_data.resources[res_name].extents.temporal.trs = (
                    dialog.lineEditResExtentsTemporalTrs.text()
                )
            else:
                config_data.resources[res_name].extents.temporal.trs = None

        # links
        config_data.resources[res_name].links = []
        links_data_lists = DataSetterFromUi._unpack_listwidget_values_to_sublists(
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
                new_link.hreflang = link[4]
            if is_valid_string(link[5]):
                new_link.length = int(link[5])

            config_data.resources[res_name].links.append(new_link)

        # providers
        config_data.resources[res_name].providers = []
        providers_data_lists = DataSetterFromUi._unpack_listwidget_values_to_sublists(
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

    @staticmethod
    def _bbox_from_string(raw_bbox_str):

        # this loop is to not add empty decimals unnecessarily
        list_bbox_val = []
        for part in raw_bbox_str.split(","):
            part = part.strip()
            if "." in part:
                list_bbox_val.append(float(part))
            else:
                list_bbox_val.append(int(part))

        if len(list_bbox_val) != 4 and len(list_bbox_val) != 6:
            raise ValueError(
                f"Wrong number of values: {len(list_bbox_val)}. Expected: 4 or 6"
            )

        return InlineList(list_bbox_val)

    @staticmethod
    def _unpack_locales_values_list_to_dict(list_widget, allow_list: bool):
        # unpack string values with locales

        all_locales_dict = {}
        for i in range(list_widget.count()):
            full_line_text = list_widget.item(i).text()
            locale = full_line_text.split(": ", 1)[0]
            value = full_line_text.split(": ", 1)[1]

            if allow_list:  # for multiple entries per language
                if locale not in all_locales_dict:
                    all_locales_dict[locale] = []
                all_locales_dict[locale].append(value)
            else:
                all_locales_dict[locale] = value

        return all_locales_dict

    @staticmethod
    def get_invalid_resource_ui_fields(dialog) -> list[str]:
        """Get list of invalid UI values in Resource UI."""

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
            raw_bbox_str = dialog.lineEditResExtentsSpatialBbox.text()
            DataSetterFromUi._bbox_from_string(raw_bbox_str)
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

    @staticmethod
    def _unpack_listwidget_values_to_sublists(
        list_widget, expected_members: int | None = None
    ):
        # unpack string values with locales

        all_sublists = []
        for i in range(list_widget.count()):
            full_line_text = list_widget.item(i).text()
            values = full_line_text.split(STRING_SEPARATOR)

            if expected_members and len(values) != expected_members:
                raise ValueError(
                    f"Not enough values to unpack in {list_widget}: {len(all_sublists)}. Expected: {expected_members}"
                )
            all_sublists.append(values)

        return all_sublists

    @staticmethod
    def save_resource_edit_and_preview(dialog):
        """Save current changes to the resource data, reset widgets to Preview. Called from .ui."""

        invalid_fields = DataSetterFromUi.get_invalid_resource_ui_fields(dialog)
        if len(invalid_fields) > 0:
            QMessageBox.warning(
                dialog,
                "Warning",
                f"Invalid fields' values: {invalid_fields}",
            )
            return

        DataSetterFromUi.set_resource_data_from_ui(dialog)

        # reset the current resource name, refresh UI list
        dialog.current_res_name = dialog.lineEditResAlias.text()
        dialog.exit_resource_edit()

    @staticmethod
    def validate_config_data(dialog) -> int:
        # validate mandatory fields before saving to file
        invalid_props = []
        invalid_props.extend(dialog.config_data.server.get_invalid_properties())
        invalid_props.extend(dialog.config_data.metadata.get_invalid_properties())
        for key, resource in dialog.config_data.resources.items():
            invalid_res_props = [
                f"resources.{key}.{prop}" for prop in resource.get_invalid_properties()
            ]
            invalid_props.extend(invalid_res_props)

        return invalid_props
