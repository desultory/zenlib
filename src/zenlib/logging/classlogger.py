__author__ = "desultory"
__version__ = "2.0.0"

from .colorlognameformatter import ColorLognameFormatter

from logging import Logger, getLogger, StreamHandler
from sys import modules


def _has_handler(logger):
    while logger:
        if logger.handlers:
            return True
        logger = logger.parent
    return False


class ClassLogger:
    def __init__(self, logger=None, _log_bump=0, *args, **kwargs):
        # Get the parent logger from the root if one was not passed
        parent_logger = logger if isinstance(logger, Logger) else getLogger()
        # Get a child logger from the parent logger, set self.logger
        self.logger = parent_logger.getChild(self.__class__.__name__)
        # Bump the log level if _log_bump is passed
        self.logger.setLevel(self.logger.parent.level + _log_bump)

        # Add a colored stream handler if one does not exist
        if not _has_handler(self.logger):
            color_stream_handler = StreamHandler()
            color_stream_handler.setFormatter(ColorLognameFormatter(fmt='%(levelname)s | %(name)-42s | %(message)s'))
            self.logger.addHandler(color_stream_handler)
            self.logger.info("Adding default handler: %s" % self.logger)

        # Log class init if _log_init is passed
        if kwargs.pop('_log_init', True) is True:
            self.logger.info("Intializing class: %s" % self.__class__.__name__)
            self.logger.debug("Log level: %s" % self.logger.level)

            if args:
                self.logger.debug("Args: %s" % repr(args))
            if kwargs:
                self.logger.debug("Kwargs: %s" % repr(kwargs))
            if module_version := getattr(modules[self.__module__], '__version__', None):
                self.logger.info("Module version: %s" % module_version)
        else:
            self.logger.log(5, "Init debug logging disabled for: %s" % self.__class__.__name__)

        if super().__class__.__class__ is not type:
            super().__init__(*args, **kwargs)

    def __setattr__(self, name, value):
        """ Add logging to setattr. """
        super().__setattr__(name, value)

        # Check if the logger is defined
        if not hasattr(self, 'logger') or not isinstance(self.logger, Logger):
            return

        elif isinstance(value, list) or isinstance(value, dict) or isinstance(value, str) and "\n" in value:
            self.logger.log(5, "Setattr '%s' to:\n%s" % (name, value))
        else:
            self.logger.log(5, "Setattr '%s' to: %s" % (name, value))

    def __setitem__(self, name, value):
        """ Add logging to dict setitem. """
        if hasattr(super(), '__setitem__'):
            super().__setitem__(name, value)
            self.logger.log(5, "Setitem '%s' to: %s" % (name, value))
