from dataclasses import is_dataclass, fields, MISSING
from enum import Enum
from types import UnionType
from typing import get_origin, get_args, Union, get_type_hints

from .top_level.utils import InlineList


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
                    # TODO: exception with expected type e.g list[ProviderPostgres]

                    # exception: remap list to internally used InlineList (needed later for YAML formatting)
                    if expected_type is InlineList:
                        new_value = InlineList(new_value)

                    setattr(instance, field_name, new_value)
                else:
                    wrong_types.append(
                        f"Skipped '{prop_name}.{field_name}': expected {expected_type}, got {type(new_value)}"
                    )
                    all_missing_props.append(f"{prop_name}.{field_name}")
        else:  # field is missing from the object

            # don't report optional fields as missing
            # for optional fields, 'default' is explicitly set to 'None'
            if fld.default is not MISSING and fld.default is None:
                print(f"MISSING: {prop_name}.{field_name}")
            else:
                missing_fields.append(f"{prop_name}.{field_name}")
                all_missing_props.append(f"{prop_name}.{field_name}")

    return missing_fields, wrong_types, all_missing_props


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
            if (
                field.default is not MISSING and field.default is None
            ):  # field has default None
                continue  # field is ok, go to next
            if field.default is not field.default_factory:  # field has default
                continue  # field is ok, go to next
            if field.default_factory is not None:  # field has default factory
                continue  # field is ok, go to next
            return False  # field and defaults are missing

        value = data[field_name]

        # Check type
        if not _is_instance_of_type(value, field_type):
            return False

    return True
