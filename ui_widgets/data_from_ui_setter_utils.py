from ..models.top_level.utils import STRING_SEPARATOR, InlineList


def bbox_from_string(raw_bbox_str):

    # this loop is to not add empty decimals unnecessarily
    list_bbox_val = []
    for part in raw_bbox_str.split(","):
        part = part.strip()
        if "." in part:
            list_bbox_val.append(float(part))
        else:
            list_bbox_val.append(int(part))

    if len(list_bbox_val) != 4 and len(list_bbox_val) != 6:
        raise ValueError(
            f"Wrong number of values: {len(list_bbox_val)}. Expected: 4 or 6"
        )

    return InlineList(list_bbox_val)


def unpack_locales_values_list_to_dict(list_widget, allow_list: bool):
    # unpack string values with locales

    all_locales_dict = {}
    for i in range(list_widget.count()):
        full_line_text = list_widget.item(i).text()
        locale = full_line_text.split(": ", 1)[0]
        value = full_line_text.split(": ", 1)[1]

        if allow_list:  # for multiple entries per language
            if locale not in all_locales_dict:
                all_locales_dict[locale] = []
            all_locales_dict[locale].append(value)
        else:
            all_locales_dict[locale] = value

    return all_locales_dict


def unpack_listwidget_values_to_sublists(
    list_widget, expected_members: int | None = None
):
    # unpack string values with locales

    all_sublists = []
    for i in range(list_widget.count()):
        full_line_text = list_widget.item(i).text()
        values = full_line_text.split(STRING_SEPARATOR)

        if expected_members and len(values) != expected_members:
            raise ValueError(
                f"Not enough values to unpack in {list_widget}: {len(all_sublists)}. Expected: {expected_members}"
            )
        all_sublists.append(values)

    return all_sublists
