from dataclasses import dataclass, field
from enum import Enum
from urllib.parse import urlparse


# records
class MetadataKeywordTypeEnum(Enum):
    DISCIPLINE = "discipline"
    TEMPORAL = "temporal"
    PLACE = "place"
    THEME = "theme"
    STRATUM = "stratum"


class MetadataRoleEnum(Enum):
    AUTHOR = "author"
    COAUTHOR = "coAuthor"
    COLLABORATOR = "collaborator"
    CONTRIBUTOR = "contributor"
    CUSTODIAN = "custodian"
    DISTRIBUTOR = "distributor"
    EDITOR = "editor"
    FUNDER = "funder"
    MEDIATOR = "mediator"
    ORIGINATOR = "originator"
    OWNER = "owner"
    POINTOFCONTACT = "pointOfContact"
    PRINCIPALINVESTIGATOR = "principalInvestigator"
    PROCESSOR = "processor"
    PUBLISHER = "publisher"
    RESOURCEPROVIDER = "resourceProvider"
    RIGHTSHOLDER = "rightsHolder"
    SPONSOR = "sponsor"
    STAKEHOLDER = "stakeholder"
    USER = "user"


# data classes
@dataclass(kw_only=True)
class IdentificationConfig:
    title: str | dict = field(default_factory=lambda: "")
    description: str | dict = field(default_factory=lambda: "")
    keywords: list | dict = field(default_factory=lambda: [])
    keywords_type: MetadataKeywordTypeEnum = field(
        default_factory=lambda: MetadataKeywordTypeEnum.THEME
    )
    terms_of_service: str = field(
        default="https://creativecommons.org/licenses/by/4.0/"
    )
    url: str = field(default="https://example.org")


@dataclass(kw_only=True)
class LicenseConfig:
    name: str = field(default="CC-BY 4.0 license")
    url: str = field(default="https://creativecommons.org/licenses/by/4.0/")


@dataclass(kw_only=True)
class ProviderConfig:
    name: str = field(default="Organization Name")
    url: str = field(default="https://pygeoapi.io")


@dataclass(kw_only=True)
class ContactConfig:
    name: str = field(default="Lastname, Firstname")
    position: str = field(default="Position Title")
    address: str = field(default="Mailing Address")
    city: str = field(default="City")
    stateorprovince: str = field(default="Administrative Area")
    postalcode: str = field(default="Zip or Postal Code")
    country: str = field(default="Country")
    phone: str = field(default="+xx-xxx-xxx-xxxx")
    fax: str = field(default="+xx-xxx-xxx-xxxx")
    email: str = field(default="you@example.org")
    url: str = field(default="Contact URL")
    hours: str = field(default="Mo-Fr 08:00-17:00")
    instructions: str = field(default="During hours of service. Off on weekends.")
    role: MetadataRoleEnum = field(
        default_factory=lambda: MetadataRoleEnum.POINTOFCONTACT
    )


@dataclass(kw_only=True)
class MetadataConfig:
    """Placeholder class for Metadata configuration data."""

    identification: IdentificationConfig = field(
        default_factory=lambda: IdentificationConfig()
    )
    license: LicenseConfig = field(default_factory=lambda: LicenseConfig())
    provider: ProviderConfig = field(default_factory=lambda: ProviderConfig())
    contact: ContactConfig = field(default_factory=lambda: ContactConfig())

    def get_invalid_properties(self):
        """Checks the values of mandatory fields: identification (title, description, keywords)."""
        all_invalid_fields = []

        if len(self.identification.title) == 0:
            all_invalid_fields.append("metadata.identification.title")
        if len(self.identification.description) == 0:
            all_invalid_fields.append("metadata.identification.description")
        if len(self.identification.keywords) == 0:
            all_invalid_fields.append("metadata.identification.keywords")
        if len(self.license.name) == 0:
            all_invalid_fields.append("metadata.license.name")
        if len(self.provider.name) == 0:
            all_invalid_fields.append("metadata.provider.name")
        if len(self.contact.name) == 0:
            all_invalid_fields.append("metadata.contact.name")

        parsed_url = urlparse(self.identification.url)
        if not all([parsed_url.scheme, parsed_url.netloc]):
            all_invalid_fields.append("metadata.identification.url")

        return all_invalid_fields
