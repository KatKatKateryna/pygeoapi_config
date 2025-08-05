class InlineList(list):
    """Class wrapper to indicate that the list should be written as one line in YAML.
    Used for 'bbox' property."""

    pass


def is_valid_string(text):
    if len(str(text)) >= 1:
        return True
    return False
