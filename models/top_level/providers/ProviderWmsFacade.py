from dataclasses import dataclass, field

from .records import ProviderTypes
from ..providers import ProviderTemplate


@dataclass(kw_only=True)
class WmsFacadeOptions:
    layer: str = ""
    style: str = ""
    version: str = ""


@dataclass(kw_only=True)
class WmsFacadeFormat:
    name: str = ""
    mimetype: str = ""


# All Provider subclasses need to have default values even for mandatory fields,
# so that the empty instance can be created and filled with values later
@dataclass(kw_only=True)
class ProviderWmsFacade(ProviderTemplate):

    # overwriting default values of the parent class
    type: ProviderTypes = ProviderTypes.MAP
    name: str = "WMSFacade"
    data: str = ""

    # provider-specific attributes
    options: WmsFacadeOptions = field(default_factory=lambda: WmsFacadeOptions())
    format: WmsFacadeFormat = field(default_factory=lambda: WmsFacadeFormat())
