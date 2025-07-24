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
    Only 2 levels of properties have an assigned type,
    the deeper nested properties (as well as optional properties) are defined as generic dictionaries.
    """

    server: ServerConfig = field(default_factory=lambda: ServerConfig())
    logging: LoggingConfig = field(default_factory=lambda: LoggingConfig())
    metadata: MetadataConfig = field(default_factory=lambda: MetadataConfig())
    resources: list[ResourceConfigTemplate] = field(default_factory=lambda: [])

    def set_data_from_yaml(self, dict_content: dict):
        """Parse YAML file content and overwride .config_data properties where available."""

        # Read the content of the YAML file for each of the top level properties
        server_config = dict_content.get("server", {})
        logging_config = dict_content.get("logging", {})
        metadata_config = dict_content.get("metadata", {})
        resources_config = dict_content.get("resources", [])
        resources_dict_list = [{k: v} for k, v in resources_config.items()]

        # Update the dataclass properties with the new values
        update_dataclass_from_dict(self.server, server_config)
        update_dataclass_from_dict(self.logging, logging_config)
        update_dataclass_from_dict(self.metadata, metadata_config)

        self.resources.clear()
        for res_config in resources_dict_list:
            if isinstance(res_config, dict):
                resource_instance_name = next(iter(res_config))
                resource_data = res_config[resource_instance_name]

                # Create a new ResourceConfigTemplate instance and update with available values
                new_resource_item = ResourceConfigTemplate(
                    instance_name=resource_instance_name
                )
                update_dataclass_from_dict(new_resource_item, resource_data)
                self.resources.append(new_resource_item)
            else:
                print(f"Skipping invalid resource entry: {res_config}")
