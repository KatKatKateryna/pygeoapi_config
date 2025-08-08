from enum import Enum

STRING_SEPARATOR = " | "


class InlineList(list):
    """Class wrapper to indicate that the list should be written as one line in YAML.
    Used for 'bbox' property."""

    pass


def is_valid_string(text):
    if len(str(text)) >= 1:
        return True
    return False


def get_enum_value_from_string(enum_type: Enum, text: str):
    if isinstance(enum_type, type) and issubclass(enum_type, Enum):
        for member in enum_type:
            if text == member.value:
                return member
    raise AttributeError(f"Unexpected attribute type '{text}'", name="text")
