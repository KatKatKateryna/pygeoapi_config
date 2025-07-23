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
class ServerConfig:
    """Placeholder class for Server configuration data."""

    bind: BindConfig = field(default_factory=lambda: BindConfig())
    url: str = field(default="http://localhost:5000")
    mimetype: str = field(default="application/json; charset=UTF-8")
    encoding: str = field(default="utf-8")
    gzip: bool = field(default=False)
    languages: list = field(default_factory=lambda: ["en-US"])  # to format with " - "
    cors: bool = field(
        default=True
    )  # TODO: seems to be a mandatory field, but commented out here: https://github.com/geopython/pygeoapi/blob/master/pygeoapi-config.yml
    pretty_print: bool = field(default=True)
    limits: LimitsConfig = field(default_factory=lambda: LimitsConfig())
    map: MapConfig = field(default_factory=lambda: MapConfig())
    admin: bool = field(default=False)
