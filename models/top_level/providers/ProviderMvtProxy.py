from dataclasses import dataclass, field

from .records import ProviderTypes
from ..providers import ProviderTemplate


@dataclass(kw_only=True)
class MvtProxyZoom:
    min: int = 0
    max: int = 15


@dataclass(kw_only=True)
class MvtProxyOptions:
    zoom: MvtProxyZoom = field(default_factory=lambda: MvtProxyZoom())
    schemes: list = field(default_factory=lambda: [])


@dataclass(kw_only=True)
class MvtProxyFormat:
    name: str = ""
    mimetype: str = ""


# All Provider subclasses need to have default values even for mandatory fields,
# so that the empty instance can be created and filled with values later
@dataclass(kw_only=True)
class ProviderMvtProxy(ProviderTemplate):

    # overwriting default values of the parent class
    type: ProviderTypes = ProviderTypes.TILE
    name: str = "MVT-proxy"
    data: str = ""

    # provider-specific attributes
    options: MvtProxyOptions = field(default_factory=lambda: MvtProxyOptions())
    format: MvtProxyFormat = field(default_factory=lambda: MvtProxyFormat())
