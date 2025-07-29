from dataclasses import dataclass, field
from enum import Enum


# records
class OnExceed(Enum):
    THROTTLE = "throttle"
    ERROR = "error"


# data classes
@dataclass(kw_only=True)
class BindConfig:
    host: str = field(default="0.0.0.0")
    port: int = field(default=5000)


@dataclass(kw_only=True)
class LimitsConfig:
    default_items: int = field(default=20)
    max_items: int = field(default=50)
    on_exceed: OnExceed = field(default_factory=lambda: OnExceed.THROTTLE)


@dataclass(kw_only=True)
class MapConfig:
    url: str = field(default="https://tile.openstreetmap.org/{z}/{x}/{y}.png")
    attribution: str = field(
        default='&copy; <a href="https://openstreetmap.org/copyright">OpenStreetMap contributors</a>'
    )


@dataclass(kw_only=True)
class TemplatesConfig:
    path: str = field(default="")
    static: str = field(default="")


@dataclass(kw_only=True)
class ApiRulesConfig:
    # Not currently used in the UI
    api_version: str = field(default="1.2.3")
    strict_slashes: bool = field(default=True)
    url_prefix: str = field(default="v{api_major}")
    version_header: str = field(default="X-API-Version")


@dataclass(kw_only=True)
class ServerConfig:
    """Placeholder class for Server configuration data."""

    bind: BindConfig = field(default_factory=lambda: BindConfig())
    url: str = field(default="http://localhost:5000")
    mimetype: str = field(default="application/json; charset=UTF-8")
    encoding: str = field(default="utf-8")
    gzip: bool = field(default=False)
    languages: list = field(default_factory=lambda: ["en-US"])  # to format with " - "
    cors: bool = field(default=False)
    pretty_print: bool = field(default=False)
    limits: LimitsConfig = field(default_factory=lambda: LimitsConfig())
    map: MapConfig = field(default_factory=lambda: MapConfig())
    admin: bool = field(default=False)
    templates: TemplatesConfig = field(default_factory=lambda: TemplatesConfig())

    # optional fields:
    # TODO: Not currently used in the UI
    # api_rules: ApiRulesConfig | None = None

    def get_invalid_properties(self):
        """Checks the values of mandatory fields: bind (host), url, languages."""
        all_invalid_fields = []

        if len(self.bind.host) < 7:
            all_invalid_fields.append("server.bind.host")
        if len(self.url) < 7:
            all_invalid_fields.append("server.url")
        if len(self.languages) == 0:
            all_invalid_fields.append("server.languages")

        return all_invalid_fields
