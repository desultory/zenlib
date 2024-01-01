__author__ = "desultory"
__version__ = "1.2.0"

from .colorlognameformatter import ColorLognameFormatter

from logging import Logger, getLogger, StreamHandler
from sys import modules
from functools import update_wrapper, wraps
from inspect import signature


def loggify(cls):
    def _has_handler(logger):
        while logger:
            if logger.handlers:
                return True
            logger = logger.parent
        return False

    class ClassLogger(cls):
        def __init__(self, *args, **kwargs):
            # Get the parent logger from the root if one was not passed
            parent_logger = kwargs.pop('logger') if isinstance(kwargs.get('logger'), Logger) else getLogger()
            # Get a child logger from the parent logger, set self.logger
            self.logger = parent_logger.getChild(cls.__name__)
            # Bump the log level if _log_bump is passed
            self.logger.setLevel(self.logger.parent.level + kwargs.pop('_log_bump', 0))

            # Add a colored stream handler if one does not exist
            if not _has_handler(self.logger):
                color_stream_handler = StreamHandler()
                color_stream_handler.setFormatter(ColorLognameFormatter(fmt='%(levelname)s | %(name)-42s | %(message)s'))
                self.logger.addHandler(color_stream_handler)
                self.logger.info("Adding default handler: %s" % self.logger)

            # Log class init if _log_init is passed
            if kwargs.pop('_log_init', True) is True:
                self.logger.info("Intializing class: %s" % cls.__name__)
                self.logger.debug("Log level: %s" % self.logger.level)

                if args:
                    self.logger.debug("Args: %s" % repr(args))
                if kwargs:
                    self.logger.debug("Kwargs: %s" % repr(kwargs))
                if module_version := getattr(modules[cls.__module__], '__version__', None):
                    self.logger.info("Module version: %s" % module_version)
                if class_version := getattr(cls, '__version__', None):
                    self.logger.info("Class version: %s" % class_version)
            else:
                self.logger.log(5, "Init debug logging disabled for: %s" % cls.__name__)

            super().__init__(*args, **kwargs)
            update_wrapper(self, cls)

        def __getattribute__(self, name):
            """
            Override for function use logging.
            Does not override functions starting with __
            Does not log functions starting with _ to debug level
            """
            attr = super().__getattribute__(name)
            # Ignore builtins, add additional logging for functions
            if callable(attr) and not name.startswith('__'):
                log_level = 5 if name.startswith('_') else 10

                # Add a wrapper, so the returned function will haev additional logging
                @wraps(attr)
                def call_wrapper(*args, **kwargs):
                    self.logger.log(log_level, "Calling function: %s" % name)
                    self.logger.log(5, "[%s] Calling function with args: %s, kwargs: %s" % (name, args, kwargs))
                    try:
                        result = attr(self, *args, **kwargs) if signature(attr).parameters.get('self') else attr(*args, **kwargs)
                    except ValueError:
                        result = attr(*args, **kwargs)
                    self.logger.log(5, "[%s] Finished with result: %s" % (name, result))
                    return result
                return call_wrapper
            else:
                return attr

        def __setattr__(self, name, value):
            """ Add logging to setattr. """
            super().__setattr__(name, value)

            # Check if the logger is defined
            if not isinstance(self.logger, Logger):
                raise ValueError("The logger is not defined")

            if isinstance(value, list) or isinstance(value, dict) or isinstance(value, str) and "\n" in value:
                self.logger.log(5, "Setattr '%s' to:\n%s" % (name, getattr(self, name)))
            else:
                self.logger.log(5, "Setattr '%s' to: %s" % (name, getattr(self, name)))

        def __setitem__(self, name, value):
            """ Add logging to dict setitem. """
            if hasattr(super(), '__setitem__'):
                super().__setitem__(name, value)
                self.logger.log(5, "Setitem '%s' to: %s" % (name, value))
    return ClassLogger
