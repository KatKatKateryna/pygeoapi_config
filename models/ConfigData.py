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
        defaults = []
        defaults.extend(
            update_dataclass_from_dict(self.server, server_config, "server")
        )
        defaults.extend(
            update_dataclass_from_dict(self.logging, logging_config, "logging")
        )
        defaults.extend(
            update_dataclass_from_dict(self.metadata, metadata_config, "metadata")
        )

        self.resources = {}
        for res_config in resources_dict_list:
            if isinstance(res_config, dict):
                resource_instance_name = next(iter(res_config))
                resource_data = res_config[resource_instance_name]

                # Create a new ResourceConfigTemplate instance and update with available values
                new_resource_item = ResourceConfigTemplate(
                    instance_name=resource_instance_name
                )
                defaults.extend(
                    update_dataclass_from_dict(
                        new_resource_item,
                        resource_data,
                        f"resources: {resource_instance_name}",
                    )
                )
                self.resources[resource_instance_name] = new_resource_item
            else:
                print(f"Skipping invalid resource entry: {res_config}")

        # add dynamic property, so that it is not included in asdict()
        # ideally, we should overwrite the __init__ method, but it is not so important property
        if len(defaults) > 0:
            self._display_message = (
                f"Default values used for missing YAML fields: {defaults}"
            )
        else:
            self._display_message = ""

    @property
    def display_message(self):
        # taking precaution here because the property was not explicitly defined in the __init__ method
        if hasattr(self, "_display_message"):
            return self._display_message
        return ""
