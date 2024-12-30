from dataclasses import dataclass


def validatedDataclass(cls):
    from zenlib.logging import loggify
    from zenlib.util import merge_class


    cls = loggify(dataclass(cls))
    base_annotations = {}
    for base in cls.__mro__:
        base_annotations.update(getattr(base, "__annotations__", {}))

    cls.__annotations__.update(base_annotations)

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

            expected_type = self.__class__.__annotations__.get(attribute)
            if not expected_type:
                return value  # No type hint, so we can't validate it
            if not isinstance(value, expected_type):
                try:
                    value = expected_type(value)
                except ValueError:
                    raise TypeError(f"[{attribute}] Type mismatch: '{expected_type}' != {type(value)}")
            return value

    merge_class(cls, ValidatedDataclass, ignored_attributes=["__setattr__"])
    return ValidatedDataclass
