__author__ = "desultory"
__version__ = "1.0.0"


def merge_class(base_class, new_class, ignored_attributes=None):
    """Merges base attributes back into a new class, ignoring ignored_attributes
    Intended to be used when decorating classes, so the new class has attributes such as:
        __doc__
        __module__
        __annotations__
        __module__
        __name__
        __qualname__
    """
    ignored_base = ["__dict__", "__init__"]
    ignored_attributes = ignored_attributes or []
    base_attributes = [a for a in base_class.__dict__ if a.startswith("__") and a.endswith("__") and a not in ignored_base]
    base_attributes += ["__name__", "__qualname__", "__module__"]
    for attr in base_attributes:
        if attr in ignored_attributes:
            continue
        base_value = getattr(base_class, attr)
        new_value = getattr(new_class, attr, None)
        if attr in ["__init_subclass__", "__subclasshook__"]:
            bv = base_value() if callable(base_value) else base_value
            nv = new_value() if callable(new_value) else new_value
            if bv == nv:
                continue

        if base_value != new_value:
            setattr(new_class, attr, base_value)
