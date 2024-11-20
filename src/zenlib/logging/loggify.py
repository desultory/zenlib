__author__ = "desultory"
__version__ = "2.4.0"

from .utils import add_handler_if_not_exists, log_init, log_setattr

from logging import Logger, getLogger


def loggify(cls):
    class ClassLogger(cls):
        def __init__(self, *args, **kwargs):
            # Get the parent logger from the root if one was not passed
            parent_logger = kwargs.pop('logger') if isinstance(kwargs.get('logger'), Logger) else getLogger()
            # Get a child logger from the parent logger, set self.logger
            self.logger = parent_logger.getChild(cls.__name__)
            # Bump the log level if _log_bump is passed
            self.logger.setLevel(self.logger.parent.level + kwargs.pop('_log_bump', 0))

            # Add a colored stream handler if one does not exist
            add_handler_if_not_exists(self.logger)

            # Log class init if _log_init is passed
            log_init(self, args, kwargs, cls)

            # Add setattr logging
            setattr(self, "__setattr__", log_setattr)

            super().__init__(*args, **kwargs)

    ClassLogger.__name__ = cls.__name__
    ClassLogger.__module__ = cls.__module__
    ClassLogger.__doc__ = cls.__doc__
    ClassLogger.__qualname__ = cls.__qualname__
    return ClassLogger
