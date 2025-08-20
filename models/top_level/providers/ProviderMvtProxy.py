from dataclasses import dataclass, field

from .records import ProviderTypes
from ..providers import ProviderTemplate
from ..utils import is_valid_string


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

    def assign_ui_dict_to_provider_data(self, values: dict):
        pass

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
        if not isinstance(self.options.zoom.min, int):
            all_invalid_fields.append("options.zoom.min")
        if not isinstance(self.options.zoom.max, int):
            all_invalid_fields.append("options.zoom.max")
        if len(self.options.schemes) == 0:
            all_invalid_fields.append("options.schemes")

        return all_invalid_fields
