import json


class YamlConfig:
    """Placeholder class for Config file data."""

    server: dict
    logging: dict
    metadata: dict
    resources: list

    def __init__(self):
        """Initialize the class with default values."""

        # SERVER
        server = {}
        server["bind"] = {"host": "0.0.0.0", "port": 5000}
        server["url"] = "http://localhost:5000"
        server["mimetype"] = "application/json; charset=UTF-8"
        server["encoding"] = "utf-8"
        server["gzip"] = False
        server["languages"] = ["en-US"]
        server["cors"] = True  # TODO: is this a mandatory field?
        server["pretty_print"] = True
        server["limits"] = {
            "default_items": 20,
            "max_items": 50,
            "on_exceed": "throttle",  # TODO: is this a mandatory field?
        }
        server["map"] = {
            "url": "https://tile.openstreetmap.org/{z}/{x}/{y}.png",
            "attribution": '&copy; <a href="https://openstreetmap.org/copyright">OpenStreetMap contributors</a>',
        }
        server["admin"] = False

        # LOGGING
        logging = {}
        logging["level"] = "ERROR"
        logging["logfile"] = ""

        # METADATA
        metadata = {}
        metadata["identification"] = {
            "title": [{"en": ""}],
            "description": [{"en": ""}],
            "keywords": [{"en": []}],
            "keywords_type": "theme",
            "terms_of_service": "https://creativecommons.org/licenses/by/4.0/",
            "url": "https://example.org",
        }
        metadata["license"] = {
            "name": "CC-BY 4.0 license",
            "url": "https://creativecommons.org/licenses/by/4.0/",
        }
        metadata["provider"] = {
            "name": "Organization Name",
            "url": "https://pygeoapi.io",
        }
        metadata["contact"] = {
            "name": "Lastname, Firstname",
            "position": "Position Title",
            "address": "Mailing Address",
            "city": "City",
            "stateorprovince": "Administrative Area",
            "postalcode": "Zip or Postal Code",
            "country": "Country",
            "phone": "+xx-xxx-xxx-xxxx",
            "fax": "+xx-xxx-xxx-xxxx",
            "email": "you@example.org",
            "url": "Contact URL",
            "hours": "Mo-Fr 08:00-17:00",
            "instructions": "During hours of service. Off on weekends.",
            "role": "pointOfContact",
        }

        # RESOURCES
        resources = []

        self.server = server
        self.logging = logging
        self.metadata = metadata
        self.resources = resources

    @property
    def as_dict(self):
        """Return a dictionary representation of a class instance."""
        return {
            "server": self.server,
            "logging": self.logging,
            "metadata": self.metadata,
            "resources": self.resources,
        }

    @property
    def as_string(self):
        """Return a string representation of a class instance."""
        return json.dumps(self.as_dict)

    def __repr__(self):
        return self.as_string
