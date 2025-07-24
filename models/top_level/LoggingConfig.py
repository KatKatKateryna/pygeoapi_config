from dataclasses import dataclass, field
from enum import Enum


# records
class LoggingLevel(Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    ERROR = "ERROR"
    WARNING = "WARNING"


# data classes
@dataclass(kw_only=True)
class RotationConfig:
    # Not currently used in the UI
    mode: str | None = None
    when: str | None = None
    interval: int | None = None
    max_bytes: int | None = None
    backup_count: int | None = None


@dataclass(kw_only=True)
class LoggingConfig:
    """Placeholder class for Logging configuration data."""

    # fields with default values:
    level: LoggingLevel = field(default_factory=lambda: LoggingLevel.ERROR)
    logfile: str = field(default="")

    # optional fields:
    logformat: str | None = None
    dateformat: str | None = None
    # TODO: Not currently used in the UI
    rotation: RotationConfig | None = None
