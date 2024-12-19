__author__ = "desultory"
__version__ = "3.0.0"

from ..util import merge_class
from .loggermixin import LoggerMixIn


def loggify(cls):
    class ClassLogger(cls, LoggerMixIn):
        def __init__(self, *args, **kwargs):
            self.init_logger(args, kwargs)
            super().__init__(*args, **kwargs)

    merge_class(cls, ClassLogger, ignored_attributes=["__setattr__"])
    return ClassLogger
