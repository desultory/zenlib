__author__ = "desultory"
__version__ = "2.1.2"

from .utils import add_handler_if_not_exists, log_init, log_setattr

from logging import Logger, getLogger


class ClassLogger:
    def __init__(self, *args, **kwargs):
        # Get the parent logger from the root if one was not passed
        parent_logger = kwargs.pop('logger') if isinstance(kwargs.get('logger'), Logger) else getLogger()
        # Get a child logger from the parent logger, set self.logger
        self.logger = parent_logger.getChild(self.__class__.__name__)
        # Bump the log level if _log_bump is passed
        self.logger.setLevel(self.logger.parent.level + kwargs.pop('_log_bump', 0))

        # Add a colored stream handler if one does not exist
        add_handler_if_not_exists(self.logger)

        # Log class init if _log_init is passed
        log_init(self, args, kwargs)


        if kwargs.pop('_log_setattr', False):
            # add setattr logging
            setattr(self, "__setattr__", log_setattr)

        if super().__class__.__class__ is not type:
            super().__init__(*args, **kwargs)
