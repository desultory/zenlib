__author__ = "desultory"
__version__ = "0.2.0"


from functools import wraps


def walk_dict(d, walk_key, raise_exception=True):
    """ Walks a dict using a dict structured as the path to the key. """
    for key, subkey in walk_key.items():
        if isinstance(subkey, dict):
            return walk_dict(d[key], subkey, raise_exception=raise_exception)
        if key not in d and not raise_exception:
            return
        if subkey not in d[key] and not raise_exception:
            return
        return d[key][subkey]


def check_dict(key, validate_dict=None, value=None, value_arg=None, unset=False, raise_exception=False, log_level=10, return_val=False, return_arg=None, message=None):
    """
    Adds a check for a dict key to a function.
    If the dict is nto passed, uses the first argument of the function (often self).
    If a value is specified, checks that the value of the key matches the value.
    """
    def decorator(func):
        @wraps(func)
        def validation_wrapper(*args, **kwargs):
            if hasattr(args[0], "__dict__"):
                validate_dict = args[0]

            if hasattr(args[0], "logger"):
                args[0].logger.debug("[%s] Checking dict key: %s" % (func.__name__, key))
                if isinstance(validate_dict, dict):
                    args[0].logger.debug("[%s] Dict:\n%s" % (func.__name__, validate_dict))
                else:
                    args[0].logger.debug("[%s] Dict: %s" % (func.__name__, validate_dict))

            if not validate_dict:
                raise ValueError("validate_dict must be specified.")

            def dispatch_msg(msg):
                msg = msg if not message else f"[{func.__name__}] {message}"
                if raise_exception:
                    raise ValueError(msg)
                elif getattr(args[0], 'logger', False):
                    args[0].logger.log(log_level, msg)
                else:
                    print(msg)
                return args[return_arg] if return_arg else return_val

            if isinstance(key, str):
                if key not in validate_dict:
                    if not unset:
                        return dispatch_msg("[%s] Unable to find key: %s." % (func.__name__, key))
                    else:
                        dict_val = None
                else:
                    if unset:
                        return dispatch_msg("[%s] Key is set when it should be unset: %s." % (func.__name__, key))
                    else:
                        dict_val = validate_dict[key]
            elif isinstance(key, dict):
                if dict_val := walk_dict(validate_dict, key, raise_exception=raise_exception):
                    if unset:
                        return dispatch_msg("[%s] Key is set when it should be unset: %s." % (func.__name__, dict_val))
                elif not unset:
                    raise ValueError("Unable to find key: %s." % key)

            check_val = args[value_arg] if value_arg is not None else value
            if check_val is not None and dict_val != check_val:
                return dispatch_msg("[%s] Key: %s has value: %s, but expected: %s." % (func.__name__, key, dict_val, value))

            if hasattr(args[0], "logger"):
                args[0].logger.debug("[%s] Validation successful for key: %s." % (func.__name__, key))

            return func(*args, **kwargs)
        return validation_wrapper
    return decorator


