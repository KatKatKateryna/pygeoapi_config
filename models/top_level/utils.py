from enum import Enum
import requests
from urllib.parse import urlparse

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


def bbox_from_list(raw_bbox_list: list):

    # this loop is to not add empty decimals unnecessarily
    list_bbox_val = []
    for part in raw_bbox_list:
        if isinstance(part, str):  # if the list is read from UI widgets
            part = part.strip()
            if "." in part:
                list_bbox_val.append(float(part))
            else:
                list_bbox_val.append(int(part))
        else:  # if the list is already taken from actual data (int or float)
            list_bbox_val.append(part)

    if len(list_bbox_val) != 4 and len(list_bbox_val) != 6:
        raise ValueError(
            f"Wrong number of values: {len(list_bbox_val)}. Expected: 4 or 6"
        )

    return InlineList(list_bbox_val)


def is_url_responsive(url: str) -> bool:

    parsed_url = urlparse(url)
    if not all([parsed_url.scheme, parsed_url.netloc]):
        return False, "Invalid URL"

    try:
        # Detect OGC ExceptionReport (invalid request)
        response = requests.get(url, allow_redirects=True, timeout=5)
        if response.status_code != 200:
            return False, f"HTTP response status code: {response.status_code}"
        else:
            text = response.text
            if "ExceptionReport" in text or "ExceptionText" in text:
                return False, "Invalid CRS URL"
            return True, "Valid CRS URL"

    except requests.ConnectionError:
        # No internet or server unreachable
        return False, "No internet connection or cannot reach server."

    except requests.Timeout:
        return False, "Request timed out."

    except requests.RequestException:
        return False, "Something went wrong with the request :("
