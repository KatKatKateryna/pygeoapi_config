from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

from .providers import ProviderPostgresql, ProviderMvtProxy, ProviderWmsFacade
from .utils import InlineList


# records
class ResourceTypes(Enum):
    COLLECTION = "collection"
    STAC = "stac-collection"


class VisibilityTypes(Enum):
    DEFAULT = "default"
    HIDDEN = "hidden"


# data classes
@dataclass(kw_only=True)
class LinkTemplate:
    """Class to represent a Link configuration template."""

    type: str = ""
    rel: str = ""
    href: str = ""

    # optional
    title: str | None = None
    hreflang: str | None = None
    length: int | None = None


@dataclass(kw_only=True)
class SpatialConfig:
    bbox: InlineList = field(default_factory=lambda: InlineList([-180, -90, 180, 90]))

    # optional, but with assumed default value:
    crs: str = field(default="http://www.opengis.net/def/crs/OGC/1.3/CRS84")


@dataclass(kw_only=True)
class TemporalConfig:

    # optional
    begin: str | datetime | None = None
    end: str | datetime | None = None
    trs: str | None = (
        None  # default: 'http://www.opengis.net/def/uom/ISO-8601/0/Gregorian'
    )


@dataclass(kw_only=True)
class ExtentsConfig:
    """Class to represent Extents configuration template."""

    # fields with default values:
    spatial: SpatialConfig = field(default_factory=lambda: SpatialConfig())

    # optional
    temporal: TemporalConfig | None = None


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
    # for providers, the types have to be explicitly listed so they are picked up on deserialization
    providers: list[ProviderPostgresql | ProviderMvtProxy | ProviderWmsFacade] = field(
        default_factory=lambda: []
    )

    # optional
    visibility: VisibilityTypes | None = None
    # limits, linked-data: ignored for now

    # Overwriding __init__ method to pass 'instance_name' as an input but not make it an instance property
    # This will allow to have a clean 'asdict(class)' output without 'instance_name' in it
    def __init__(
        self,
        *,
        instance_name: str,
        type: ResourceTypes = ResourceTypes.COLLECTION,
        title: str = "",
        description: str = "",
        keywords: dict = None,
        links: list[LinkTemplate] = None,
        extents: ExtentsConfig = None,
        providers: list[
            ProviderPostgresql | ProviderMvtProxy | ProviderWmsFacade
        ] = None,
        visibility: VisibilityTypes | None = None
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
        self.visibility = visibility

    @property
    def instance_name(self):
        return self._instance_name
