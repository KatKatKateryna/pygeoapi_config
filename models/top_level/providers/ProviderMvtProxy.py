from dataclasses import dataclass, field

from .records import ProviderTypes
from ..providers import ProviderTemplate
from ..utils import is_valid_string
from ...utils import update_dataclass_from_dict


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

    def assign_ui_dict_to_provider_data(self, values: dict[str, str | list | int]):

        # adjust structure to match the class structure
        values["options"] = {}
        values["options"]["zoom"] = {}
        values["format"] = {}

        # custom change
        values["options"]["zoom"]["min"] = values["options.zoom.min"]
        values["options"]["zoom"]["max"] = values["options.zoom.max"]
        values["options"]["schemes"] = values["options.schemes"]  # already list

        values["format"]["name"] = values["format.name"]
        values["format"]["mimetype"] = values["format.mimetype"]

        update_dataclass_from_dict(self, values, "ProviderMvtProxy")

        # Exception: if Zoom values are empty (e.g. missing in the UI), they will not overwrite the class attributes
        # This happens because if new value is abcent, there is nothing we can replace a default 'int' with. Manual overwrite:
        if values["options.zoom.min"] is None:
            self.options.zoom.min = None
        if values["options.zoom.max"] is None:
            self.options.zoom.max = None

    def pack_data_to_list(self):
        return [
            self.type.value,
            self.name,
            self.crs,
            self.data,
            self.options.zoom.min,
            self.options.zoom.max,
            self.options.schemes,
            self.format.name,
            self.format.mimetype,
        ]

    def assign_value_list_to_provider_data(self, values: list):
        if len(values) != 9:
            raise ValueError(
                f"Unexpected number of value to unpack: {len(values)}. Expected: 9"
            )

        self.name = values[1]
        self.crs = values[2]
        self.data = values[3]
        self.options.zoom.min = int(values[4])
        self.options.zoom.max = int(values[5])
        self.options.schemes = (
            values[6].split(",") if is_valid_string(values[6]) else []
        )
        self.format.name = values[7]
        self.format.mimetype = values[8]

    def get_invalid_properties(self):
        """Checks the values of mandatory fields."""
        all_invalid_fields = []

        if not isinstance(self.type, ProviderTypes):
            all_invalid_fields.append("type")
        if not is_valid_string(self.name):
            all_invalid_fields.append("name")
        if not self.crs or not is_valid_string(self.crs):
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
