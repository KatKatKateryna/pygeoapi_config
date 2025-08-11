from dataclasses import dataclass, field, fields, is_dataclass
from enum import Enum

from .utils import update_dataclass_from_dict
from .top_level import (
    ServerConfig,
    LoggingConfig,
    MetadataConfig,
    ResourceConfigTemplate,
)
from .top_level.utils import InlineList
from .top_level.providers import ProviderPostgresql
from .top_level.providers.records import ProviderTypes


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
        all_missing_props = []

        defaults_server, wrong_types_server, all_missing_props_server = (
            update_dataclass_from_dict(self.server, server_config, "server")
        )

        defaults_logging, wrong_types_logging, all_missing_props_logging = (
            update_dataclass_from_dict(self.logging, logging_config, "logging")
        )

        defaults_metadata, wrong_types_metadata, all_missing_props_metadata = (
            update_dataclass_from_dict(self.metadata, metadata_config, "metadata")
        )

        default_fields.extend(defaults_server)
        default_fields.extend(defaults_logging)
        default_fields.extend(defaults_metadata)
        wrong_types.extend(wrong_types_server)
        wrong_types.extend(wrong_types_logging)
        wrong_types.extend(wrong_types_metadata)
        all_missing_props.extend(all_missing_props_server)
        all_missing_props.extend(all_missing_props_logging)
        all_missing_props.extend(all_missing_props_metadata)

        self.resources = {}
        for res_config in resources_dict_list:
            if isinstance(res_config, dict):
                resource_instance_name = next(iter(res_config))
                resource_data = res_config[resource_instance_name]

                # Create a new ResourceConfigTemplate instance and update with available values
                new_resource_item = ResourceConfigTemplate(
                    instance_name=resource_instance_name
                )
                defaults_resource, wrong_types_resource, all_missing_props_resource = (
                    update_dataclass_from_dict(
                        new_resource_item,
                        resource_data,
                        f"resources.{resource_instance_name}",
                    )
                )
                default_fields.extend(defaults_resource)
                wrong_types.extend(wrong_types_resource)
                all_missing_props.extend(all_missing_props_resource)

                self.resources[resource_instance_name] = new_resource_item

            else:
                wrong_types.append(
                    [f"Skipping invalid resource entry: {str(res_config)[:40]}"]
                )
                all_missing_props.append(str(res_config)[:40])

        # add dynamic property, so that it is not included in asdict()
        # ideally, we should overwrite the __init__ method, but it is not so important property
        self._defaults_used = default_fields
        self._wrong_types = wrong_types
        self._all_missing_props = all_missing_props

    @property
    def defaults_message(self):
        # taking precaution here because the property was not explicitly defined in the __init__ method
        if hasattr(self, "_defaults_used"):
            return self._defaults_used
        return []

    @property
    def error_message(self):
        # taking precaution here because the property was not explicitly defined in the __init__ method
        if hasattr(self, "_wrong_types"):
            return self._wrong_types
        return []

    @property
    def all_missing_props(self):
        # taking precaution here because the property was not explicitly defined in the __init__ method
        if hasattr(self, "_all_missing_props"):
            return self._all_missing_props
        return []

    def asdict_enum_safe(self, obj):
        """Overwriting dataclass 'asdict' fuction to replace Enums with strings."""
        if is_dataclass(obj):
            result = {}
            for f in fields(obj):
                value = getattr(obj, f.name)
                if value is not None:
                    result[f.name] = self.asdict_enum_safe(value)
            return result
        elif isinstance(obj, Enum):
            return obj.value
        elif isinstance(obj, InlineList):
            return obj
        elif isinstance(obj, list):
            return [self.asdict_enum_safe(v) for v in obj]
        elif isinstance(obj, dict):
            return {
                self.asdict_enum_safe(k): self.asdict_enum_safe(v)
                for k, v in obj.items()
            }
        else:
            return obj

    def add_new_resource(self) -> str:
        """Add a placeholder resource."""
        new_name = "new_resource"
        self.resources[new_name] = ResourceConfigTemplate(instance_name=new_name)
        return new_name

    def delete_resource(self, dialog):
        self.resources.pop(dialog.current_res_name)

    def set_new_provider_data(
        self, values: dict, res_name: str, provider_type: ProviderTypes
    ):
        """Adds a provider data to the resource. Called on Save click from New Providere window."""

        if provider_type == ProviderTypes.FEATURE:
            new_provider = ProviderPostgresql()
            self.resources[res_name].providers.append(new_provider)

            # adjust structure to match the class structure
            values["data"] = {}
            for k, v in values.items():
                if k in ["host", "port", "dbname", "user", "password", "search_path"]:
                    values["data"][k] = v
                # custom change
            values["data"]["search_path"] = values["search_path"].split(",")

            update_dataclass_from_dict(new_provider, values, "ProviderPostgresql")

            # if incomplete data, remove Provider from ConfigData and show Warning
            invalid_props = new_provider.get_invalid_properties()
            if len(invalid_props) > 0:
                self.resources[res_name].providers.pop(-1)
                return invalid_props

        elif provider_type == ProviderTypes.MAP:
            pass

        elif provider_type == ProviderTypes.TILE:
            pass

        # set value to the provider widget
        return []
