from dataclasses import dataclass, field


@dataclass(kw_only=True)
class BindConfig:
    host: str = field(default="0.0.0.0")
    port: int = field(default=5000)


@dataclass(kw_only=True)
class LimitsConfig:
    default_items: int = field(default=20)
    max_items: int = field(default=50)
    on_exceed: str = field(default="throttle")  # TODO: is this a mandatory field?


@dataclass(kw_only=True)
class MapConfig:
    url: str = field(default="https://tile.openstreetmap.org/{z}/{x}/{y}.png")
    attribution: str = field(
        default='&copy; <a href="https://openstreetmap.org/copyright">OpenStreetMap contributors</a>'
    )


@dataclass(kw_only=True)
class TemplatesConfig:
    # Not currently used
    path: str = field(default="/path/to/jinja2/templates/folder")
    static: str = field(default="/path/to/static/folder")


@dataclass(kw_only=True)
class ApiRulesConfig:
    # Not currently used
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
    cors: bool = field(default=True)
    pretty_print: bool = field(default=True)
    limits: LimitsConfig = field(default_factory=lambda: LimitsConfig())
    map: MapConfig = field(default_factory=lambda: MapConfig())
    admin: bool = field(default=False)
    # Not currently used
    templates: TemplatesConfig = field(default_factory=lambda: TemplatesConfig())

    # optional fields:
    # Not currently used
    api_rules: ApiRulesConfig | None = None
