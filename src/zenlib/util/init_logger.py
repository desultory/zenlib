
from logging import getLogger, StreamHandler
from zenlib.logging import ColorLognameFormatter


def init_logger(name=None, args=None):
    name = name or __name__
    logger = getLogger(name)
    handler = StreamHandler()
    formatter = ColorLognameFormatter()
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

