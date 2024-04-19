__author__ = "desultory"
__version__ = "1.0.0"


def walk_dict(d, walk_key, fail_safe=True):
    """ Walks a dict using a dict structured as the path to the key. """
    for key, subkey in walk_key.items():
        if isinstance(subkey, dict):
            return walk_dict(d[key], subkey, fail_safe=fail_safe)
        if key not in d and fail_safe:
            return
        if subkey not in d[key] and fail_safe:
            return
        return d[key][subkey]

