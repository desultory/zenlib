__author__ = "desultory"
__version__ = "3.0.0"

from .loggermixin import LoggerMixIn


class ClassLogger(LoggerMixIn):
    def __init__(self, *args, **kwargs):
        self.init_logger(args, kwargs)

        if super().__class__.__class__ is not type:
            super().__init__(*args, **kwargs)
