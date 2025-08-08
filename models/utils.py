from dataclasses import is_dataclass, fields, MISSING
from enum import Enum
from types import UnionType
from typing import Any, get_origin, get_args, Union, get_type_hints

from .top_level.utils import InlineList, get_enum_value_from_string


def update_dataclass_from_dict(
    instance, new_dict, prop_name: str = ""
) -> tuple[list, list, list]:
    hints = get_type_hints(type(instance))
    missing_fields = []
    wrong_types = []
    all_missing_props = []

    # loop through the instance properties
    for fld in fields(instance):
        field_name = fld.name

        # try overwrite instance property with new dictionary value
        if field_name in new_dict:
            new_value = new_dict[field_name]
            current_value = getattr(instance, field_name)
            expected_type = hints[field_name]

            # If field is a dataclass and new_value is a dict, recurse
            # This behavior works when 'current_value' is an already instantiated dataclass
            # with all set properties - we just need to overwrite the values

            # case where default value in None, but another class might be expected
            if current_value is None and type(expected_type) is UnionType:
                args = get_args(expected_type)
                valid_type = next((t for t in args if t is not type(None)), None)
                if is_dataclass(valid_type) and isinstance(new_value, dict):
                    current_value = valid_type()
                    setattr(instance, field_name, current_value)

            if is_dataclass(current_value) and isinstance(new_value, dict):
                new_missing_fields, new_wrong_types, new_missing_props = (
                    update_dataclass_from_dict(
                        current_value, new_value, f"{prop_name}.{field_name}"
                    )
                )
                missing_fields.extend(new_missing_fields)
                wrong_types.extend(new_wrong_types)
                all_missing_props.extend(new_missing_props)
            else:
                if _is_instance_of_type(new_value, expected_type):

                    # Exception: remap list to internally used InlineList (needed later for YAML formatting)
                    if expected_type is InlineList:
                        if isinstance(new_value, str):
                            new_value = new_value.split(",")

                        new_value = InlineList(new_value)

                    # Exception: remap str to Enum
                    elif isinstance(expected_type, type) and issubclass(
                        expected_type, Enum
                    ):
                        new_value = get_enum_value_from_string(expected_type, new_value)

                    # Exception with 'expected_type' 'list[some dataclass]'
                    # In this case, 'current_value' will be a 'default'=None (for optional fields) or 'default_factory'=[] (for mandatory fields)
                    # We need to cast every element in the list to the correct class before assigning
                    # if we just assign new_value as is, it will be a 'list[dict]'

                    elif isinstance(new_value, list):
                        new_value, more_wrong_types = (
                            _cast_list_elements_to_expected_types(
                                new_value, expected_type, f"{prop_name}.{field_name}"
                            )
                        )
                        wrong_types.extend(more_wrong_types)

                    setattr(instance, field_name, new_value)
                else:
                    wrong_types.append(f"{prop_name}.{field_name}")
                    all_missing_props.append(f"{prop_name}.{field_name}")
        else:  # field is missing from the object

            # don't report optional fields as missing
            # for optional fields, 'default' is explicitly set to 'None'
            if fld.default is not MISSING and fld.default is None:
                pass
                # print(f"MISSING: {prop_name}.{field_name}")
            else:
                missing_fields.append(f"{prop_name}.{field_name}")
                all_missing_props.append(f"{prop_name}.{field_name}")

    return missing_fields, wrong_types, all_missing_props


def _cast_element_to_type(value: Any, expected_type, prop_name: str):
    """Function intended to cast non-iterable values, or dict (to dataclasses)."""

    # if there are alternative options for the expected type: recurse
    if type(expected_type) is UnionType:
        args = get_args(expected_type)
        for inner_type in args:
            if _is_instance_of_type(value, inner_type):
                return _cast_element_to_type(value, inner_type, prop_name)

    elif is_dataclass(expected_type):
        class_instance = expected_type()
        update_dataclass_from_dict(
            class_instance,
            value,
            prop_name,
        )
        return class_instance

    else:
        if _is_instance_of_type(value, expected_type):
            return value

    raise ValueError("Element type not matched")


def _cast_list_elements_to_expected_types(
    new_value: list, expected_type, prop_name: str
):
    """Cast all elements in the list to one of the expected types."""
    casted_values = []
    wrong_types = []

    # check for the expected inner arguments types
    args = get_args(expected_type)

    if type(expected_type) is UnionType and args:
        # e.g. 'list | dict'
        for possible_type in args:
            if _is_instance_of_type(new_value, possible_type):
                casted_values, more_wrong_types = _cast_list_elements_to_expected_types(
                    new_value, possible_type, prop_name
                )
                wrong_types.extend(more_wrong_types)

    elif type(expected_type) is not UnionType and args and len(new_value) > 0:
        # e.g. '<ListTemplate>' or (ProviderPostgresql | ProviderMvtProxy | ProviderWmsFacade,)

        for val in new_value:

            value_casted = False
            for inner_type in args:
                try:
                    casted_element = _cast_element_to_type(val, inner_type, prop_name)
                    casted_values.append(casted_element)
                    value_casted = True
                    break
                except ValueError:
                    pass

            if not value_casted:
                if isinstance(val, dict) and len(val) > 0:
                    wrong_types.append(f"{prop_name}.{val[0]}")
                else:
                    wrong_types.append(f"{prop_name}")

    else:
        # if there are no arguments, just assign the value as is
        casted_values.extend(new_value)

    return casted_values, wrong_types


def _is_instance_of_type(value, expected_type) -> bool:
    """Basic type checker supporting Optional (Union[..., NoneType]) and direct types."""
    origin = get_origin(expected_type)
    args = get_args(expected_type)

    # Handle Union (including Optional, str | dict, etc.)
    if origin is Union or type(expected_type) is UnionType:
        # Recursively check each allowed type in the union
        return any(_is_instance_of_type(value, arg) for arg in args)

    # Generic containers like list[X], dict[K, V]
    if origin in (list, tuple, set):
        if not isinstance(value, origin):
            return False

        # check for the inner arguments types
        if args and len(value) > 0:
            for val in value:

                value_matched = False
                for inner_type in args:
                    if _is_instance_of_type(val, inner_type):
                        value_matched = True
                        continue
                if not value_matched:
                    return False

            # if loop successfully ended and all values matched expected types
            return True

        return True

    if origin is dict:
        if not isinstance(value, dict):
            return False
        if args and len(args) == 2:
            key_type, val_type = args
            return all(
                _is_instance_of_type(k, key_type) and _is_instance_of_type(v, val_type)
                for k, v in value.items()
            )
        return True

    # Exception for InlineList: just check if the value is a list
    if expected_type is InlineList:
        if isinstance(value, list):
            return True
        return False

    # Exception for Records (Enums): check if value is a member of the Enum
    if issubclass(expected_type, Enum):
        if value in [member.value for member in expected_type]:
            return True
        return False

    # Exception for when 'expected_type' is a custom dataclass and 'value' is dict
    if isinstance(value, dict) and is_dataclass(expected_type):
        return can_cast_to_dataclass(value, expected_type)

    # Fallback for normal types
    return isinstance(value, expected_type)


def can_cast_to_dataclass(data: dict, cls: type) -> bool:

    type_hints = get_type_hints(cls)
    for field in fields(cls):
        field_name = field.name
        field_type = type_hints.get(field_name)

        if field_name not in data:
            if field.default is not MISSING:  # field has default
                continue  # field is ok, go to next

            return False  # field and defaults are missing

        value = data[field_name]

        # Check type
        if not _is_instance_of_type(value, field_type):
            return False

    return True
