from importlib.metadata import PackageNotFoundError, version
from logging import Logger, StreamHandler
from sys import modules

from zenlib.logging.colorlognameformatter import ColorLognameFormatter


def _logger_has_handler(logger: Logger | None) -> bool:
    """Checks if a logger or its parents has a handler already"""
    while logger:
        if logger.handlers:
            return True
        logger = logger.parent
    return False


def add_handler_if_not_exists(logger: Logger) -> None:
    """Adds a ColorLognameFormatter handler to the logger if it doesn't have a handler already
    Coloring is disabled by the _ZENLIB_COLOR_TEXT variable in the colorize function
    """
    if _logger_has_handler(logger):
        return
    stream_handler = StreamHandler()
    formatter = ColorLognameFormatter(fmt="%(levelname)s | %(name)-42s | %(message)s")
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)
    logger.info(f"Added default handler to logger: {logger}")


def log_init(self, args, kwargs) -> None:
    """If _log_init is in the kwargs and set to True, logs init args, kwargs, class name, and version"""
    class_name = self.__class__.__name__
    logger = self.logger
    if not kwargs.pop("_log_init", False):
        return logger.log(5, f"Init logging disabled for class: {class_name}")

    logger.info(f"Initializing class: {class_name}")

    if args:
        logger.debug(f"[{class_name}] Init args: {args}")
    if kwargs:
        logger.debug(f"[{class_name}] Init kwargs: {kwargs}")

    package_name = self.__module__.split(".")[0]
    try:
        logger.info(f"[{package_name}] Package version: {version(package_name)}")
    except (NameError, PackageNotFoundError) as ex:
        if str(ex) == "No package metadata was found for builtins":
            package_name = "builtins"
        logger.debug(f"[{class_name}] Package version not found for: {package_name}")

    if module_version := getattr(modules.get(self.__module__), "__version__", None):
        logger.info(f"[{self.__module__}] Module version: {module_version}")

    if class_version := getattr(self, "__version__", None):
        logger.info(f"[{class_name}] Class version: {class_version}")
