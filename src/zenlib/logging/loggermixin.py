__author__ = "desultory"
__version__ = "1.3.0"

from logging import Logger, getLogger

from .utils import add_handler_if_not_exists, handle_additional_logging, log_init


class LoggerMixIn:
    """ A mixin class that provides logging functionality to classes that inherit from it.
    The logger kwarg can be passed, which will be used as the parent logger.
    if _log_init is set to True, the logger will log the class initialization.
    if _log_level is set, the logger's level will be set to that value.
    If _log_bump is set, the logger's level will be bumped by that amount.
    Othweise, the log level is not set, and the logger will use the parent's level.
    """

    def init_logger(self, args, kwargs):
        # Get the parent logger from the root if one was not passed
        parent_logger = kwargs.pop("logger") if isinstance(kwargs.get("logger"), Logger) else getLogger()
        # Get a child logger from the parent logger, set self.logger
        self.logger = parent_logger.getChild(self.__class__.__name__)

        if log_level := kwargs.pop("_log_level", None):
            # Set the logger's level if _log_level is passed
            self.logger.setLevel(log_level)
        elif log_bump := kwargs.pop("_log_bump", None):
            self.logger.setLevel(self.logger.parent.level + log_bump)

        # Add a colored stream handler if one does not exist
        add_handler_if_not_exists(self.logger)

        # Log class init if _log_init is passed
        log_init(self, args, kwargs)

        # Add logging to _log_setattr if set
        handle_additional_logging(self, kwargs)
