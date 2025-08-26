from ..models.top_level.utils import STRING_SEPARATOR


def unpack_locales_values_list_to_dict(list_widget, allow_list_per_locale: bool):
    # unpack string values with locales

    all_locales_dict = {}
    for i in range(list_widget.count()):
        full_line_text = list_widget.item(i).text()
        locale = full_line_text.split(": ", 1)[0]
        value = full_line_text.split(": ", 1)[1]

        if allow_list_per_locale:  # for multiple entries per language
            if locale not in all_locales_dict:
                all_locales_dict[locale] = []
            all_locales_dict[locale].append(value)
        else:
            all_locales_dict[locale] = value

    return all_locales_dict


def unpack_listwidget_values_to_sublists(
    list_widget, expected_members: int | None = None
) -> list[list]:

    all_sublists = []
    for i in range(list_widget.count()):

        # using count to access data entries of 'list_widget' via .item(i)
        full_line_text = list_widget.item(i).text()
        values = full_line_text.split(STRING_SEPARATOR)

        if expected_members and len(values) != expected_members:
            raise ValueError(
                f"Not enough values to unpack in {list_widget}: {len(all_sublists)}. Expected: {expected_members}"
            )
        all_sublists.append(values)

    return all_sublists
