from dataclasses import dataclass
from typing import get_type_hints


def validatedDataclass(cls):
    from zenlib.logging import loggify
    from zenlib.util import merge_class

    cls = loggify(dataclass(cls))

    class ValidatedDataclass(cls):
        def __setattr__(self, attribute, value):
            value = self._validate_attribute(attribute, value)
            super().__setattr__(attribute, value)

        def _validate_attribute(self, attribute, value):
            """Ensures the attribute is the correct type"""
            if attribute == "logger":
                return value
            if value is None:
                return

            expected_type = get_type_hints(self.__class__)[attribute]
            if not isinstance(value, expected_type):
                try:
                    value = expected_type(value)
                except ValueError:
                    raise TypeError(f"[{attribute}] Type mismatch: '{expected_type}' != {type(value)}")
            return value

    merge_class(cls, ValidatedDataclass, ignored_attributes=["__setattr__"])
    return ValidatedDataclass
