__author__ = "desultory"
__version__ = "1.1.0"


def return_check(self, message, raise_exception, log_level, return_val=None):
    if raise_exception:
        raise ValueError(message)
    self.logger.log(log_level, message)
    return return_val


def contains(key, message=None, is_set=True, raise_exception=False, log_level=10, debug_level=5):
    def _dict_contains(func):
        from functools import wraps

        @wraps(func)
        def _contains(*args, **kwargs):
            self = args[0]
            if key not in self:
                return return_check(self, message or "[%s] Unable to find key: %s." % (self.__class__.__name__, key), raise_exception, log_level)
            if is_set and not self[key]:
                return return_check(self, message or "[%s] Key is not set: %s." % (self.__class__.__name__, key), raise_exception, log_level)
            self.logger.log(debug_level, "[%s] Contains check passed for: %s" % (self.__class__.__name__, key))
            return func(*args, **kwargs)
        return _contains
    return _dict_contains
