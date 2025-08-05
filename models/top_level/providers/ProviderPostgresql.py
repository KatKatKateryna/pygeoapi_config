from dataclasses import dataclass, field

from .records import ProviderTypes
from ..providers import ProviderTemplate
from ..utils import InlineList


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
    geom_field = ""
