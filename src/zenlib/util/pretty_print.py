__author__ = "Desultory"
__version__ = "1.0.0"


def pretty_print(input_data, indent=0, prefix="", print_out=False):
    """
    Formats a complex data structure into a formatted string
    """
    out = ""
    if isinstance(input_data, dict):
        for key, value in input_data.items():
            if not isinstance(value, str) and (hasattr(value, '__getitem__') or hasattr(value, '__iter__')) and not isinstance(value, type):
                out += " " * indent + "%s:\n" % key
                out += pretty_print(value, indent + 2)
            else:
                out += " " * indent + f"{prefix}{key}: {value}\n"
    elif isinstance(input_data, list):
        for item in input_data:
            out += pretty_print(item, indent, prefix='- ')
    elif isinstance(input_data, tuple):
        for item in input_data:
            out += pretty_print(item, indent, prefix='+ ')
    elif hasattr(input_data, 'name') and hasattr(input_data, 'value'):
        # If the value is not iterable, it is a single value
        if not hasattr(input_data.value, '__getitem__') or isinstance(input_data.value, str):
            out += " " * indent + f"{prefix}{input_data.name}: {input_data.value}\n"
        else:
            out += " " * indent + f"{prefix}{input_data.name}:\n{pretty_print(input_data.value, indent=indent + 2, prefix='= ')}"
    elif isinstance(input_data, type):
        out += " " * indent + f"{prefix}<{input_data.__name__}>\n"
    elif not isinstance(input_data, str) and (hasattr(input_data, '__getitem__') or hasattr(input_data, '__iter__')):
        for key in input_data:
            out += pretty_print(key, indent, prefix='+ ')
    else:
        out = " " * indent + f"{prefix}{input_data}\n"

    if print_out:
        print(out)

    return out
