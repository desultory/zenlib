
from logging import getLogger


def init_logger(name=None, args=None):
    name = name or __name__
    return getLogger(name)

