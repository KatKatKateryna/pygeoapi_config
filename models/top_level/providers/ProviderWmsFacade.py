from dataclasses import dataclass, field

from .records import ProviderTypes
from ..providers import ProviderTemplate
from ..utils import is_valid_string


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

    def get_invalid_properties(self):
        """Checks the values of mandatory fields."""
        all_invalid_fields = []

        if not isinstance(self.type, ProviderTypes):
            all_invalid_fields.append("type")
        if not is_valid_string(self.name):
            all_invalid_fields.append("name")
        if not is_valid_string(self.crs):
            all_invalid_fields.append("crs")
        if not is_valid_string(self.data):
            all_invalid_fields.append("data")
        if not is_valid_string(self.format.name):
            all_invalid_fields.append("format.name")
        if not is_valid_string(self.format.mimetype):
            all_invalid_fields.append("format.mimetype")
        if not is_valid_string(self.options.layer):
            all_invalid_fields.append("options.layer")
        if not is_valid_string(self.options.style):
            all_invalid_fields.append("options.style")
        if not is_valid_string(self.options.version):
            all_invalid_fields.append("options.version")

        return all_invalid_fields
