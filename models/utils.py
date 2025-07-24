from dataclasses import is_dataclass, fields
from typing import get_origin, get_args, Union, get_type_hints

from .top_level.utils import InlineList


def update_dataclass_from_dict(instance, new_dict):
    hints = get_type_hints(type(instance))

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
                update_dataclass_from_dict(current_value, new_value)
            else:
                if _is_instance_of_type(new_value, expected_type):

                    # exception: remap list to internally used InlineList (needed later for YAML formatting)
                    if expected_type is InlineList:
                        new_value = InlineList(new_value)

                    setattr(instance, field_name, new_value)
                else:
                    print(
                        f"Skipped {field_name}: expected {expected_type}, got {type(new_value)}"
                    )


def _is_instance_of_type(value, expected_type) -> bool:
    """Basic type checker supporting Optional (Union[..., NoneType]) and direct types."""
    origin = get_origin(expected_type)
    args = get_args(expected_type)

    # Handle Union (including Optional, str | dict, etc.)
    if origin is Union:
        # Recursively check each allowed type in the union
        return any(_is_instance_of_type(value, arg) for arg in args)

    # Generic containers like list[X], dict[K, V]
    if origin in (list, tuple, set):
        if not isinstance(value, origin):
            return False
        # if args:
        #    inner_type = args[0]
        #    return all(_is_instance_of_type(item, inner_type) for item in value)
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

    # Exception for InlineList
    if expected_type is InlineList:
        if isinstance(value, list):
            return True
        return False

    # TODO: Exceptions for Records(Enums)

    # Fallback for normal types
    return isinstance(value, expected_type)
