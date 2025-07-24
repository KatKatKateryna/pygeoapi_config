from dataclasses import dataclass, field
from enum import Enum


@dataclass(kw_only=True)
class RotationConfig:
    # Not currently used
    mode: str | None = None
    when: str | None = None
    interval: int | None = None
    max_bytes: int | None = None
    backup_count: int | None = None


class LoggingLevel(Enum):
    # Not currently used
    DEBUG = "DEBUG"
    INFO = "INFO"
    ERROR = "ERROR"
    WARNING = "WARNING"


@dataclass(kw_only=True)
class LoggingConfig:
    """Placeholder class for Logging configuration data."""

    # fields with default values:
    level: str = field(default="ERROR")
    logfile: str = field(default="")

    # optional fields:
    # Not currently used
    logformat: str | None = None
    dateformat: str | None = None
    rotation: RotationConfig | None = None
