def _logger_has_handler(logger):
    """ Checks if a logger or its parents has a handler already """
    while logger:
        if logger.handlers:
            return True
        logger = logger.parent
    return False


def add_handler_if_not_exists(logger):
    """ Adds a ColorLognameFormatter handler to the logger if it doesn't have a handler already"""
    if _logger_has_handler(logger):
        return
    from .colorlognameformatter import ColorLognameFormatter
    from logging import StreamHandler
    color_stream_handler = StreamHandler()
    color_stream_handler.setFormatter(ColorLognameFormatter(fmt='%(levelname)s | %(name)-42s | %(message)s'))
    logger.addHandler(color_stream_handler)
    logger.info("Added default handler to logger: %s", logger)

def log_init(self, args, kwargs, cls=None):
    """ If _log_init is in the kwargs and set to True, logs init args, kwargs, class name, and version"""
    class_name = cls.__name__ if cls else self.__class__.__name__
    logger = self.logger
    if not kwargs.pop("_log_init", False):
        return logger.debug("Init logging disabled for class: %s", class_name)

    logger.info("Initializing class: %s", class_name)

    if args:
        logger.debug("[%s] Init args: %s" % (class_name,  args))
    if kwargs:
        logger.debug("[%s] Init kwargs: %s" % (class_name, kwargs))

    from sys import modules
    if module_version := getattr(modules.get(cls.__module__), '__version__', None):
        logger.info("[%s] Module version: %s" % (class_name,module_version))

    if class_version := getattr(cls, '__version__', None):
        logger.info("[%s] Class version: %s" % (class_name, class_version))
