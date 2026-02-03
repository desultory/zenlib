from importlib.metadata import PackageNotFoundError, version
from logging import Logger, StreamHandler
from sys import modules

from zenlib.logging.colorlognameformatter import ColorLognameFormatter


def _logger_has_handler(logger):
    """Checks if a logger or its parents has a handler already"""
    while logger:
        if logger.handlers:
            return True
        logger = logger.parent
    return False


def add_handler_if_not_exists(logger):
    """Adds a ColorLognameFormatter handler to the logger if it doesn't have a handler already
    Coloring is diabled by the _ZENLIB_COLOR_TEXT variable in the colorize function
    """
    if _logger_has_handler(logger):
        return
    stream_handler = StreamHandler()
    formatter = ColorLognameFormatter(fmt="%(levelname)s | %(name)-42s | %(message)s")
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)
    logger.info("Added default handler to logger: %s", logger)


def log_init(self, args, kwargs):
    """If _log_init is in the kwargs and set to True, logs init args, kwargs, class name, and version"""
    class_name = self.__class__.__name__
    logger = self.logger
    if not kwargs.pop("_log_init", False):
        return logger.log(5, "Init logging disabled for class: %s", class_name)

    logger.info("Initializing class: %s", class_name)

    if args:
        logger.debug("[%s] Init args: %s" % (class_name, args))
    if kwargs:
        logger.debug("[%s] Init kwargs: %s" % (class_name, kwargs))

    package_name = self.__module__.split(".")[0]
    try:
        logger.info("[%s] Package version: %s" % (package_name, version(package_name)))
    except (NameError, PackageNotFoundError) as ex:
        if ex.msg != "No package metadata was found for builtins":
            logger.debug("[%s] Package version not found for: %s" % (class_name, package_name))

    if module_version := getattr(modules.get(self.__module__), "__version__", None):
        logger.info("[%s] Module version: %s" % (self.__module__, module_version))

    if class_version := getattr(self, "__version__", None):
        logger.info("[%s] Class version: %s" % (class_name, class_version))


def handle_additional_logging(self, kwargs):
    """Sets __setattr__ to log_setattr if _log_setattr is in the kwargs and set to True"""
    if kwargs.pop("_log_setattr", False):
        setattr(self, "__setattr__", log_setattr)


def log_setattr(self, name, value):
    """Logs when an attribute is set"""
    super().__setattr__(name, value)
    # check if the logger is defined
    if not isinstance(self.logger, Logger):
        raise ValueError("Logger is not defined")

    # Log containers or strings with newlines on a new line
    if isinstance(value, list) or isinstance(value, dict) or isinstance(value, str) and "\n" in value:
        self.logger.log(5, "Setattr '%s' to:\n%s" % (name, getattr(self, name)))
    else:
        self.logger.log(5, "Setattr '%s' to: %s" % (name, getattr(self, name)))
