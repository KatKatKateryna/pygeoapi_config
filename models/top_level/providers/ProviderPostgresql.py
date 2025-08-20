from dataclasses import dataclass, field

from ...utils import update_dataclass_from_dict
from .records import ProviderTypes
from ..providers import ProviderTemplate
from ..utils import InlineList, is_valid_string


@dataclass(kw_only=True)
class PostgresqlData:
    host: str = ""
    port: str = ""
    dbname: str = ""
    user: str = ""
    password: str = ""
    search_path: InlineList = field(default_factory=lambda: InlineList([]))


# All Provider subclasses need to have default values even for mandatory fields,
# so that the empty instance can be created and filled with values later
@dataclass(kw_only=True)
class ProviderPostgresql(ProviderTemplate):

    # overwriting default values of the parent class
    type: ProviderTypes = ProviderTypes.FEATURE
    name: str = "PostgreSQL"
    data: PostgresqlData = field(default_factory=lambda: PostgresqlData())

    # provider-specific attributes
    id_field: str = ""
    table: str = ""
    geom_field: str = ""

    def assign_ui_dict_to_provider_data(self, values: dict):

        # adjust structure to match the class structure
        values["data"] = {}
        for k, v in values.items():
            if k in ["host", "port", "dbname", "user", "password", "search_path"]:
                values["data"][k] = v
            # custom change
        values["data"]["search_path"] = values["search_path"].split(",")

        update_dataclass_from_dict(self, values, "ProviderPostgresql")

    def get_invalid_properties(self):
        """Checks the values of mandatory fields."""
        all_invalid_fields = []

        if not isinstance(self.type, ProviderTypes):
            all_invalid_fields.append("type")
        if not is_valid_string(self.name):
            all_invalid_fields.append("name")
        if not is_valid_string(self.crs):
            all_invalid_fields.append("crs")

        if not is_valid_string(self.data.host):
            all_invalid_fields.append("data.host")
        if not is_valid_string(self.data.port):
            all_invalid_fields.append("data.port")
        if not is_valid_string(self.data.dbname):
            all_invalid_fields.append("data.dbname")
        if not is_valid_string(self.data.user):
            all_invalid_fields.append("data.user")
        if not is_valid_string(self.data.password):
            all_invalid_fields.append("data.password")
        if len(self.data.search_path) == 0:
            all_invalid_fields.append("data.search_path")

        if not is_valid_string(self.id_field):
            all_invalid_fields.append("id_field")
        if not is_valid_string(self.table):
            all_invalid_fields.append("table")
        if not is_valid_string(self.geom_field):
            all_invalid_fields.append("geom_field")

        return all_invalid_fields
