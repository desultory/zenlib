__author__ = "desultory"
__version__ = "1.2.0"

from zenlib.logging import ColorLognameFormatter

from logging import Logger, getLogger, StreamHandler
from sys import modules


def loggify(cls):
    """
    Decorator for classes to add a logging object and log basic tasks
    """
    class ClassWrapper(cls):
        def __init__(self, *args, **kwargs):
            parent_logger = kwargs.pop('logger') if isinstance(kwargs.get('logger'), Logger) else getLogger()
            self.logger = parent_logger.getChild(self.__class__.__name__)
            self.logger.setLevel(self.logger.parent.level + kwargs.pop('_log_bump', 0))

            def has_handler(logger):
                parent = logger
                while parent:
                    if parent.handlers:
                        return True
                    parent = parent.parent
                return False

            if not has_handler(self.logger):
                color_stream_handler = StreamHandler()
                color_stream_handler.setFormatter(ColorLognameFormatter(fmt='%(levelname)s | %(name)-42s | %(message)s'))
                self.logger.addHandler(color_stream_handler)
                self.logger.info("Adding default handler: %s" % self.logger)

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

        def __getattribute__(self, name):
            """
            Override for function use logging.
            Does not log functions starting with _ to debug level
            """
            attr = super().__getattribute__(name)
            # Ignore builtins
            if callable(attr) and not name.startswith('__') and name not in ['get', 'set', 'items', 'keys', 'values']:
                def wrapper(*args, **kwargs):
                    if not name.startswith('_'):
                        self.logger.debug("Calling function: %s" % name)
                    self.logger.log(5, "[%s] Calling function with args: %s, kwargs: %s" % (name, args, kwargs))
                    result = attr(*args, **kwargs)
                    self.logger.log(5, "[%s] Finished with result: %s" % (name, result))
                    return result
                return wrapper
            else:
                return attr

        def __setattr__(self, name, value):
            # First set the attribute using the parent class
            super().__setattr__(name, value)

            # Check if the logger is defined
            if not isinstance(self.logger, Logger):
                raise ValueError("The logger is not defined")

            if isinstance(value, list) or isinstance(value, dict) or isinstance(value, str) and "\n" in value:
                self.logger.log(5, "Setattr '%s' to:\n%s" % (name, getattr(self, name)))
            else:
                self.logger.log(5, "Setattr '%s' to: %s" % (name, getattr(self, name)))

        def __setitem__(self, name, value):
            """
            Override for dicts,
            return an error if the parent class doesn't have __setitem__
            """
            if hasattr(super(), '__setitem__'):
                super().__setitem__(name, value)
                self.logger.log(5, "Setitem '%s' to: %s" % (name, value))
            else:
                raise NotImplementedError("The parent class does not have __setitem__")

    ClassWrapper.__name__ = cls.__name__
    ClassWrapper.__module__ = cls.__module__
    ClassWrapper.__qualname__ = cls.__qualname__

    return ClassWrapper
