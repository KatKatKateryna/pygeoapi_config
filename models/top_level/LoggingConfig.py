from dataclasses import dataclass, field


@dataclass(kw_only=True)
class LoggingConfig:
    """Placeholder class for Logging configuration data."""

    # fields with default values:
    level: str = field(default="ERROR")
    logfile: str = field(default="")
