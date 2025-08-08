from dataclasses import dataclass, field

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
        if not is_valid_string(self.data.search_path):
            all_invalid_fields.append("data.search_path")

        return all_invalid_fields
