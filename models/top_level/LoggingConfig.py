from dataclasses import dataclass, field


@dataclass(kw_only=True)
class RotationConfig:
    mode: str | None = None
    when: str | None = None
    interval: int | None = None
    max_bytes: int | None = None
    backup_count: int | None = None


@dataclass(kw_only=True)
class LoggingConfig:
    """Placeholder class for Logging configuration data."""

    # fields with default values:
    level: str = field(default="ERROR")
    logfile: str = field(default="")

    # optional fields:
    logformat: str | None = None
    dateformat: str | None = None
    rotation: RotationConfig | None = None
