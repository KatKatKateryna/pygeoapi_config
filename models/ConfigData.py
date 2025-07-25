from dataclasses import dataclass, field

from .utils import update_dataclass_from_dict
from .top_level import (
    ServerConfig,
    LoggingConfig,
    MetadataConfig,
    ResourceConfigTemplate,
)


@dataclass(kw_only=True)
class ConfigData:
    """Placeholder class for Config file data.
    Only 2-3 levels of properties have an assigned type,
    the deeper nested properties (as well as optional properties) are defined as generic dictionaries.
    """

    server: ServerConfig = field(default_factory=lambda: ServerConfig())
    logging: LoggingConfig = field(default_factory=lambda: LoggingConfig())
    metadata: MetadataConfig = field(default_factory=lambda: MetadataConfig())
    resources: dict[str, ResourceConfigTemplate] = field(default_factory=lambda: {})

    def set_data_from_yaml(self, dict_content: dict):
        """Parse YAML file content and overwride .config_data properties where available."""

        # Read the content of the YAML file for each of the top level properties
        server_config = dict_content.get("server", {})
        logging_config = dict_content.get("logging", {})
        metadata_config = dict_content.get("metadata", {})
        resources_config = dict_content.get("resources", {})
        resources_dict_list = [{k: v} for k, v in resources_config.items()]

        # Update the dataclass properties with the new values
        # keep track of missing values of wrong types (replaced with defaults)
        default_fields = []
        wrong_types = []

        defaults_server, wrong_types_server = update_dataclass_from_dict(
            self.server, server_config, "server"
        )

        defaults_logging, wrong_types_logging = update_dataclass_from_dict(
            self.logging, logging_config, "logging"
        )

        defaults_metadata, wrong_types_metadata = update_dataclass_from_dict(
            self.metadata, metadata_config, "metadata"
        )

        default_fields.extend(defaults_server)
        default_fields.extend(defaults_logging)
        default_fields.extend(defaults_metadata)
        wrong_types.extend(wrong_types_server)
        wrong_types.extend(wrong_types_logging)
        wrong_types.extend(wrong_types_metadata)

        self.resources = {}
        for res_config in resources_dict_list:
            if isinstance(res_config, dict):
                resource_instance_name = next(iter(res_config))
                resource_data = res_config[resource_instance_name]

                # Create a new ResourceConfigTemplate instance and update with available values
                new_resource_item = ResourceConfigTemplate(
                    instance_name=resource_instance_name
                )
                defaults_resource, wrong_types_resource = update_dataclass_from_dict(
                    new_resource_item,
                    resource_data,
                    f"resources: {resource_instance_name}",
                )
                default_fields.extend(defaults_resource)
                wrong_types.extend(wrong_types_resource)

                self.resources[resource_instance_name] = new_resource_item

            else:
                print(f"Skipping invalid resource entry: {res_config}")

        # add dynamic property, so that it is not included in asdict()
        # ideally, we should overwrite the __init__ method, but it is not so important property
        if len(default_fields) > 0:
            self._display_message = (
                f"Default values used for missing YAML fields: {default_fields}"
            )
            self._wrong_types = f"Errors during deserialization: {wrong_types}"
        else:
            self._display_message = ""
            self._wrong_types = ""

    @property
    def display_message(self):
        # taking precaution here because the property was not explicitly defined in the __init__ method
        if hasattr(self, "_display_message"):
            return self._display_message
        return ""

    @property
    def error_message(self):
        # taking precaution here because the property was not explicitly defined in the __init__ method
        if hasattr(self, "_wrong_types"):
            return self._wrong_types
        return ""

    def set_data_from_ui(self, dialog):

        # bind
        self.server.bind.host = dialog.lineEditHost.text()
        self.server.bind.port = dialog.spinBoxPort.value()

        # gzip
        self.server.gzip = dialog.checkBoxGzip.isChecked()

        # pretty print
        self.server.pretty_print = dialog.checkBoxPretty.isChecked()

        # admin
        self.server.admin = dialog.checkBoxAdmin.isChecked()

        # cors
        self.server.cors = dialog.checkBoxCors.isChecked()

        # templates
        self.server.templates.path = dialog.lineEditTemplatesPath.text()
        self.server.templates.static = dialog.lineEditTemplatesStatic.text()

        # map
        self.server.map.url = dialog.lineEditMapUrl.text()
        self.server.map.attribution = dialog.lineEditAttribution.text()

        # url
        self.server.url = dialog.lineEditUrl.text()

        # language
        self.server.languages = []
        for i in range(dialog.listWidgetLang.count()):
            item = dialog.listWidgetLang.item(i)
            if item.isSelected():
                self.server.languages.append(item.text())

        # limits
        self.server.limits.default_items = dialog.spinBoxDefault.value()
        self.server.limits.max_items = dialog.spinBoxMax.value()

        self.server.limits.on_exceed = dialog.comboBoxExceed.currentText()

        # logging
        self.logging.level = dialog.comboBoxLog.currentText()
        self.logging.logfile = dialog.lineEditLogfile.text()
        self.logging.logformat = dialog.lineEditLogformat.text()
        self.logging.dateformat = dialog.lineEditDateformat.text()

        # metadata identification
        self.metadata.identification.title = self._unpack_locales_values_list_to_dict(
            dialog.listWidgetMetadataIdTitle
        )
        self.metadata.identification.description = (
            self._unpack_locales_values_list_to_dict(
                dialog.listWidgetMetadataIdDescription
            )
        )
        self.metadata.identification.keywords = (
            self._unpack_locales_values_list_to_dict(
                dialog.listWidgetMetadataIdKeywords
            )
        )

        self.metadata.identification.keywords_type = (
            dialog.lineEditMetadataIdKeywordsType.text()
        )
        self.metadata.identification.terms_of_service = (
            dialog.lineEditMetadataIdTerms.text()
        )
        self.metadata.identification.url = dialog.lineEditMetadataIdUrl.text()

        # metadata license
        self.metadata.license.name = dialog.lineEditMetadataLicenseName.text()
        self.metadata.license.url = dialog.lineEditMetadataLicenseUrl.text()

        # metadata provider
        self.metadata.provider.name = dialog.lineEditMetadataProviderName.text()
        self.metadata.provider.url = dialog.lineEditMetadataProviderUrl.text()

        # metadata contact
        self.metadata.contact.name = dialog.lineEditMetadataContactName.text()
        self.metadata.contact.position = dialog.lineEditMetadataContactPosition.text()
        self.metadata.contact.address = dialog.lineEditMetadataContactAddress.text()
        self.metadata.contact.city = dialog.lineEditMetadataContactCity.text()
        self.metadata.contact.stateorprovince = (
            dialog.lineEditMetadataContactState.text()
        )
        self.metadata.contact.postalcode = dialog.lineEditMetadataContactPostal.text()
        self.metadata.contact.country = dialog.lineEditMetadataContactCountry.text()
        self.metadata.contact.phone = dialog.lineEditMetadataContactPhone.text()
        self.metadata.contact.fax = dialog.lineEditMetadataContactFax.text()
        self.metadata.contact.email = dialog.lineEditMetadataContactEmail.text()
        self.metadata.contact.url = dialog.lineEditMetadataContactUrl.text()
        self.metadata.contact.hours = dialog.lineEditMetadataContactHours.text()
        self.metadata.contact.instructions = (
            dialog.lineEditMetadataContactInstructions.text()
        )
        self.metadata.contact.role = dialog.lineEditMetadataContactRole.text()

    def set_ui_from_data(self, dialog):

        # bind
        dialog.lineEditHost.setText(self.server.bind.host)
        dialog.spinBoxPort.setValue(self.server.bind.port)

        # gzip
        dialog.checkBoxGzip.setChecked(self.server.gzip)

        # mimetype
        self._set_combo_box_value_from_data(
            combo_box=dialog.comboBoxMime,
            value=self.server.mimetype,
        )

        # encoding
        self._set_combo_box_value_from_data(
            combo_box=dialog.comboBoxEncoding,
            value=self.server.encoding,
        )

        # pretty print
        dialog.checkBoxPretty.setChecked(self.server.pretty_print)

        # admin
        dialog.checkBoxAdmin.setChecked(self.server.admin)

        # cors
        dialog.checkBoxCors.setChecked(self.server.cors)

        # templates
        dialog.lineEditTemplatesPath.setText(self.server.templates.path)
        dialog.lineEditTemplatesStatic.setText(self.server.templates.static)

        # map
        dialog.lineEditMapUrl.setText(self.server.map.url)
        dialog.lineEditAttribution.setText(self.server.map.attribution)

        dialog.lineEditUrl.setText(self.server.url)

        # language
        for i in range(dialog.listWidgetLang.count()):
            item = dialog.listWidgetLang.item(i)
            if item.text() in self.server.languages:
                item.setSelected(True)
            else:
                item.setSelected(False)

        # limits
        dialog.spinBoxDefault.setValue(self.server.limits.default_items)
        dialog.spinBoxMax.setValue(self.server.limits.max_items)

        self._set_combo_box_value_from_data(
            combo_box=dialog.comboBoxExceed,
            value=self.server.limits.on_exceed,
        )

        # logging
        self._set_combo_box_value_from_data(
            combo_box=dialog.comboBoxLog,
            value=self.logging.level,
        )

        dialog.lineEditLogfile.setText(self.logging.logfile)
        dialog.lineEditLogformat.setText(self.logging.logformat)
        dialog.lineEditDateformat.setText(self.logging.dateformat)

        # metadata identification

        # DATA WITH LOCALES
        # incoming type: possible list of strings or dictionary
        # limitation: even if YAML had just a list of strings, it will be interpreted here as "en" locale by default

        # title
        self._pack_locales_data_into_list(
            self.metadata.identification.title,
            dialog.listWidgetMetadataIdTitle,
        )

        # description
        self._pack_locales_data_into_list(
            self.metadata.identification.description,
            dialog.listWidgetMetadataIdDescription,
        )

        # keywords
        self._pack_locales_data_into_list(
            self.metadata.identification.keywords, dialog.listWidgetMetadataIdKeywords
        )

        dialog.lineEditMetadataIdKeywordsType.setText(
            self.metadata.identification.keywords_type
        )
        dialog.lineEditMetadataIdTerms.setText(
            self.metadata.identification.terms_of_service
        )
        dialog.lineEditMetadataIdUrl.setText(self.metadata.identification.url)

        # metadata license
        dialog.lineEditMetadataLicenseName.setText(self.metadata.license.name)
        dialog.lineEditMetadataLicenseUrl.setText(self.metadata.license.url)

        # metadata provider
        dialog.lineEditMetadataProviderName.setText(self.metadata.provider.name)
        dialog.lineEditMetadataProviderUrl.setText(self.metadata.provider.url)

        # metadata contact
        dialog.lineEditMetadataContactName.setText(self.metadata.contact.name)
        dialog.lineEditMetadataContactPosition.setText(self.metadata.contact.position)
        dialog.lineEditMetadataContactAddress.setText(self.metadata.contact.address)
        dialog.lineEditMetadataContactCity.setText(self.metadata.contact.city)
        dialog.lineEditMetadataContactState.setText(
            self.metadata.contact.stateorprovince
        )
        dialog.lineEditMetadataContactPostal.setText(self.metadata.contact.postalcode)
        dialog.lineEditMetadataContactCountry.setText(self.metadata.contact.country)
        dialog.lineEditMetadataContactPhone.setText(self.metadata.contact.phone)
        dialog.lineEditMetadataContactFax.setText(self.metadata.contact.fax)
        dialog.lineEditMetadataContactEmail.setText(self.metadata.contact.email)
        dialog.lineEditMetadataContactUrl.setText(self.metadata.contact.url)
        dialog.lineEditMetadataContactHours.setText(self.metadata.contact.hours)
        dialog.lineEditMetadataContactInstructions.setText(
            self.metadata.contact.instructions
        )
        dialog.lineEditMetadataContactRole.setText(self.metadata.contact.role)

        # collections
        dialog.model.setStringList([k for k, _ in self.resources.items()])

        dialog.proxy.setSourceModel(dialog.model)
        dialog.listViewCollection.setModel(dialog.proxy)

    def _set_combo_box_value_from_data(self, *, combo_box, value):
        """Set the combo box value based on the available choice and provided value."""

        for i in range(combo_box.count()):
            if combo_box.itemText(i) == value:
                combo_box.setCurrentIndex(i)
                return

        # If the value is not found, set to the first item or clear it
        if combo_box.count() > 0:
            combo_box.setCurrentIndex(0)
        else:
            combo_box.clear()

    def _unpack_locales_values_list_to_dict(self, list_widget):
        # unpack string values with locales

        all_locales_dict = {}
        for i in range(list_widget.count()):
            full_line_text = list_widget.item(i).text()
            locale = full_line_text.split(": ")[0]
            value = full_line_text.split(": ")[1]

            if locale not in all_locales_dict:
                all_locales_dict[locale] = []
            all_locales_dict[locale].append(value)

        return all_locales_dict

    def _pack_locales_data_into_list(self, data, list_widget):
        list_widget.clear()
        for key in data:
            if isinstance(data, dict):
                local_key_content = data[key]
                if isinstance(local_key_content, str):
                    value = f"{key}: {local_key_content}"
                    list_widget.addItem(value)
                else:  # list
                    for local_key in local_key_content:
                        value = f"{key}: {local_key}"
                        list_widget.addItem(value)
            else:  # list of strings
                value = f"en: {key}"
                list_widget.addItem(value)
