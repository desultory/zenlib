__author__ = "desultory"
__version__ = "1.0.0"

from functools import wraps


def log_call(log_level=10):
    """ Decorator for logging function calls to self.logger. """
    def decorator(func):
        @wraps(func)
        def log_wrapper(self, *args, **kwargs):
            self.logger.log(log_level, "[%s] Calling function with args: %s, kwargs: %s" % (func.__name__, args, kwargs))
            result = func(self, *args, **kwargs)
            self.logger.log(log_level, "[%s] Finished with result: %s" % (func.__name__, result))
            return result
        return log_wrapper
    return decorator
