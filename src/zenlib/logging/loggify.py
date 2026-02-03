__author__ = "desultory"
__version__ = "3.0.1"

from zenlib.util.merge_class import merge_class
from zenlib.logging.loggermixin import LoggerMixIn


def loggify(cls):
    class ClassLogger(cls, LoggerMixIn):
        def __init__(self, *args, **kwargs):
            self.init_logger(args, kwargs)
            super().__init__(*args, **kwargs)

    merge_class(cls, ClassLogger, ignored_attributes=["__setattr__"])
    return ClassLogger
