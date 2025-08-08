from dataclasses import dataclass, field
from enum import Enum
from urllib.parse import urlparse

from .utils import is_valid_string


# records
class ServerOnExceedEnum(Enum):
    THROTTLE = "throttle"
    ERROR = "error"


# data classes
@dataclass(kw_only=True)
class ServerBindConfig:
    host: str = field(default="0.0.0.0")
    port: int = field(default=5000)


@dataclass(kw_only=True)
class ServerLimitsConfig:
    default_items: int = field(default=20)
    max_items: int = field(default=50)
    on_exceed: ServerOnExceedEnum = field(
        default_factory=lambda: ServerOnExceedEnum.THROTTLE
    )


@dataclass(kw_only=True)
class ServerMapConfig:
    url: str = field(default="https://tile.openstreetmap.org/{z}/{x}/{y}.png")
    attribution: str = field(
        default='&copy; <a href="https://openstreetmap.org/copyright">OpenStreetMap contributors</a>'
    )


@dataclass(kw_only=True)
class ServerTemplatesConfig:
    path: str = field(default="")
    static: str = field(default="")


@dataclass(kw_only=True)
class ServerApiRulesConfig:
    # Not currently used in the UI
    api_version: str = field(default="1.2.3")
    strict_slashes: bool = field(default=True)
    url_prefix: str = field(default="v{api_major}")
    version_header: str = field(default="X-API-Version")


@dataclass(kw_only=True)
class ServerConfig:
    """Placeholder class for Server configuration data."""

    bind: ServerBindConfig = field(default_factory=lambda: ServerBindConfig())
    url: str = field(default="http://localhost:5000")
    mimetype: str = field(default="application/json; charset=UTF-8")
    encoding: str = field(default="utf-8")
    map: ServerMapConfig = field(default_factory=lambda: ServerMapConfig())

    # optional fields:
    gzip: bool = field(default=False)
    languages: list = field(default_factory=lambda: ["en-US"])  # to format with " - "
    cors: bool = field(default=False)
    pretty_print: bool = field(default=False)
    limits: ServerLimitsConfig = field(default_factory=lambda: ServerLimitsConfig())
    admin: bool = field(default=False)
    templates: ServerTemplatesConfig | None = None

    # Not currently used in the UI
    # api_rules: ServerApiRulesConfig | None = None

    def get_invalid_properties(self):
        """Checks the values of mandatory fields: bind (host), url, languages."""
        all_invalid_fields = []

        if not is_valid_string(self.bind.host):
            all_invalid_fields.append("server.bind.host")
        if not is_valid_string(self.url):
            all_invalid_fields.append("server.url")
        if len(self.languages) == 0:
            all_invalid_fields.append("server.languages")

        return all_invalid_fields
