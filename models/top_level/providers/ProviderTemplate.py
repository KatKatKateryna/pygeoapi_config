from dataclasses import dataclass, field
from typing import Any
from .records import ProviderTypes


# this class doesn't need to be initialized on its own, only the subclasses
# All Provider subclasses need to have default values even for mandatory fields,
# so that the empty instance can be created and filled with values later
@dataclass(kw_only=True)
class ProviderTemplate:
    """Class to represent a Provider configuration template."""

    type: ProviderTypes
    name: str
    data: Any

    # optional, but with assumed default value:
    crs: str = field(default="http://www.opengis.net/def/crs/OGC/1.3/CRS84")
