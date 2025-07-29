from dataclasses import dataclass, field
from enum import Enum

from .utils import InlineList


# records
class ResourceTypes(Enum):
    COLLECTION = "collection"
    STAC = "stac-collection"


class ProviderTypes(Enum):
    FEATURE = "feature"
    MAP = "map"
    TILE = "tile"


# data classes
@dataclass(kw_only=True)
class ProviderTemplate:
    """Class to represent a Provider configuration template."""

    type: ProviderTypes
    name: str
    data: str

    # optional fields:
    id_field: str | None = None
    title_field: str | None = None
    geometry: dict | None = None
    options: dict | None = None
    format: dict | None = None


@dataclass(kw_only=True)
class LinkTemplate:
    """Class to represent a Link configuration template."""

    type: str
    rel: str
    title: str
    href: str
    hreflang: str


@dataclass(kw_only=True)
class SpatialConfig:
    bbox: InlineList = field(default_factory=lambda: InlineList([-180, -90, 180, 90]))
    crs: str = field(default="http://www.opengis.net/def/crs/OGC/1.3/CRS84")


@dataclass(kw_only=True)
class ExtentsConfig:
    """Class to represent Extents configuration template."""

    # fields with default values:
    spatial: dict = field(default_factory=lambda: SpatialConfig())

    # optional fields:
    temporal: dict | None = None


@dataclass(kw_only=True)
class ResourceConfigTemplate:
    """Class to represent a Resource configuration template."""

    # fields with default values:
    type: ResourceTypes = field(default_factory=lambda: ResourceTypes.COLLECTION)
    title: str | dict = field(default="")
    description: str | dict = field(default="")
    keywords: list | dict = field(default_factory=lambda: [])
    links: list[LinkTemplate] = field(default_factory=lambda: [])
    extents: ExtentsConfig = field(default_factory=lambda: ExtentsConfig())
    providers: list[ProviderTemplate] = field(default_factory=lambda: [])

    # Overwriding __init__ method to pass 'instance_name' as an input but not make it an instance property
    # This will allow to have a clean 'asdict(class)' output without 'instance_name' in it
    def __init__(
        self,
        *,
        instance_name: str,
        type: str = "collection",
        title: str = "",
        description: str = "",
        keywords: dict = None,
        links: list[LinkTemplate] = None,
        extents: ExtentsConfig = None,
        providers: list[ProviderTemplate] = None
    ):
        self._instance_name = instance_name
        self.type = type
        self.title = title
        self.description = description

        # using full class name here instead of type(self), because "type" is used here as a property name
        if keywords is None:
            keywords = ResourceConfigTemplate.__dataclass_fields__[
                "keywords"
            ].default_factory()
        if links is None:
            links = ResourceConfigTemplate.__dataclass_fields__[
                "links"
            ].default_factory()
        if extents is None:
            extents = ResourceConfigTemplate.__dataclass_fields__[
                "extents"
            ].default_factory()
        if providers is None:
            providers = ResourceConfigTemplate.__dataclass_fields__[
                "providers"
            ].default_factory()

        self.keywords = keywords
        self.links = links
        self.extents = extents
        self.providers = providers

    @property
    def instance_name(self):
        return self._instance_name
