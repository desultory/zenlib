from dataclasses import dataclass
from typing import ForwardRef, Union, get_args, get_origin, get_type_hints


class ValidatedDataclass:
    def __setattr__(self, attribute, value):
        value = self._validate_attribute(attribute, value)
        super().__setattr__(attribute, value)

    def _validate_attribute(self, attribute, value):
        """Ensures the attribute is the correct type"""
        if attribute == "logger":
            return value
        if value is None:
            return

        expected_type = self.__class__.__annotations__.get(attribute)
        if not expected_type:
            return value  # No type hint, so we can't validate it
        if get_origin(expected_type) is Union and isinstance(get_args(expected_type)[0], ForwardRef):
            expected_type = get_type_hints(self.__class__)[attribute]

        if not isinstance(value, expected_type):
            try:
                value = expected_type(value)
            except ValueError:
                raise TypeError(f"[{attribute}] Type mismatch: '{expected_type}' != {type(value)}")
        return value


def validatedDataclass(cls):
    from zenlib.logging import loggify

    annotations = {}
    for base in cls.__mro__:
        annotations.update(getattr(base, "__annotations__", {}))

    cls_dict = dict(cls.__dict__)
    cls_dict["__annotations__"] = annotations

    vdc = loggify(dataclass(type(cls.__name__, (ValidatedDataclass, cls), cls_dict)))

    return vdc
