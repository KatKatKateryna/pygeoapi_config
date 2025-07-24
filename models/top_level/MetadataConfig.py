from dataclasses import dataclass, field


# data classes
@dataclass(kw_only=True)
class IdentificationConfig:
    title: str | dict = field(default_factory=lambda: "")
    description: str | dict = field(default_factory=lambda: "")
    keywords: list | dict = field(default_factory=lambda: [])
    keywords_type: str = field(default="theme")
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
    role: str = field(default="pointOfContact")


@dataclass(kw_only=True)
class MetadataConfig:
    """Placeholder class for Metadata configuration data."""

    identification: IdentificationConfig = field(
        default_factory=lambda: IdentificationConfig()
    )
    license: LicenseConfig = field(default_factory=lambda: LicenseConfig())
    provider: ProviderConfig = field(default_factory=lambda: ProviderConfig())
    contact: ContactConfig = field(default_factory=lambda: ContactConfig())
