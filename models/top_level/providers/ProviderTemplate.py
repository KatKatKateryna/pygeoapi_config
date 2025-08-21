from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any
from .records import ProviderTypes


# this class doesn't need to be initialized on its own, only the subclasses
# All Provider subclasses need to have default values even for mandatory fields,
# so that the empty instance can be created and filled with values later
@dataclass(kw_only=True)
class ProviderTemplate(ABC):
    """Class to represent a Provider configuration template."""

    type: ProviderTypes
    name: str
    data: Any

    # optional, but with assumed default value:
    crs: str = field(default="http://www.opengis.net/def/crs/OGC/1.3/CRS84")

    # optional
    storage_crs: str | None = None

    @staticmethod
    def init_provider_from_type(provider_type: ProviderTypes):
        """Return empty instance of the subclass, based on the requested type.
        Imports are inside the method to avoid circular imports from subclasses."""
        from . import ProviderPostgresql, ProviderWmsFacade, ProviderMvtProxy

        if provider_type == ProviderTypes.FEATURE:
            return ProviderPostgresql()

        elif provider_type == ProviderTypes.MAP:
            return ProviderWmsFacade()

        elif provider_type == ProviderTypes.TILE:
            return ProviderMvtProxy()

    @abstractmethod
    def assign_ui_dict_to_provider_data(self, values: dict[str, str]):
        """Takes the dictionary of values specific to provider type, and assigns them to the class instance."""
        pass

    @abstractmethod
    def assign_value_list_to_provider_data(self):
        """Takes a list of values specific to provider type, and assigns them to the class instance."""
        pass

    @abstractmethod
    def pack_data_to_list(self) -> list:
        """Returns a list with all instance properties in a specific order."""
        pass
