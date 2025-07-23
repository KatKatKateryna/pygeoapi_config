from dataclasses import dataclass, field

from .top_level import (
    ServerConfig,
    LoggingConfig,
    MetadataConfig,
    ResourceConfigTemplate,
)


@dataclass(kw_only=True)
class YamlConfig:
    """Placeholder class for Config file data.
    Only 2 levels of properties have an assigned type,
    the deeper nested properties (as well as optional properties) are defined as generic dictionaries.
    """

    server: ServerConfig = field(default_factory=lambda: ServerConfig())
    logging: LoggingConfig = field(default_factory=lambda: LoggingConfig())
    metadata: MetadataConfig = field(default_factory=lambda: MetadataConfig())
    resources: list[ResourceConfigTemplate] = field(default_factory=lambda: [])
