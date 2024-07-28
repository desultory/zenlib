__author__ = "desultory"
__version__ = "1.2.1"

from functools import wraps


def return_check(self, message, raise_exception, log_level, return_val=None):
    if raise_exception:
        raise ValueError(message)
    self.logger.log(log_level, message)
    return return_val


def contains(key, message=None, is_set=True, raise_exception=False, log_level=10, debug_level=5):
    """
    Ensure that the key exists in the dictionary.
    Returns the message/exception if the key is not found.
    If is_set is True, then the key must have a value.
    """
    def _dict_contains(func):
        @wraps(func)
        def _contains(*args, **kwargs):
            self = args[0]
            msg = f"[{func.__name__}] {message}" if message else None
            value = self.get(key)
            if key not in self:
                return return_check(self, msg or "[%s] Unable to find key: %s." % (func.__name__, key), raise_exception, log_level)
            if is_set and not (value or repr(value) == "PosixPath('.')"):
                return return_check(self, msg or "[%s] Key is not set: %s." % (func.__name__, key), raise_exception, log_level)
            self.logger.log(debug_level, "[%s] Contains check passed for: %s" % (func.__name__, key))
            return func(*args, **kwargs)
        return _contains
    return _dict_contains


def unset(key, message=None, raise_exception=False, log_level=10, debug_level=5):
    """
    Ensure that the key does not exist in the dictionary.
    If it exists, make sure it is not set.
    """
    def _dict_unset(func):
        @wraps(func)
        def _unset(*args, **kwargs):
            self = args[0]
            msg = f"[{func.__name__}] {message}" if message else None
            value = self.get(key)
            if key in self and (repr(value) != "PosixPath('.')" and value):
                return return_check(self, msg or "[%s] Key '%s' is set: %s." % (func.__name__, key, repr(value)), raise_exception, log_level)
            self.logger.log(debug_level, "[%s] Unset check passed for: %s; %s" % (func.__name__, key, repr(value)))
            return func(*args, **kwargs)
        return _unset
    return _dict_unset
