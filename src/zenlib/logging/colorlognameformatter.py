__author__ = "desultory"
__version__ = "3.0.0"

from logging import Formatter

from zenlib.util import colorize


class ColorLognameFormatter(Formatter):
    """A logging formatter which colors the levelname of the log message.
    Uses the zenlib.util.colorize function to color the levelname.
    Normal levelnames are padded to the length of the longest levelname."""

    level_colors = {
        "DEBUG": {"color": "white"},
        "INFO": {"color": "blue"},
        "WARNING": {"color": "yellow"},
        "ERROR": {"color": "red", "bold": True},
        "CRITICAL": {"color": "red", "bold": True, "bright": True},
    }

    def __init__(self, fmt="%(levelname)s | %(message)s", *args, **kwargs):
        super().__init__(fmt, *args, **kwargs)
        self.level_str_width = max(len(name) for name in self.level_colors) - 1

    def format(self, record):
        # When calling format, replace the levelname with a colored version
        # Note: the string size is greatly increased because of the color codes
        old_levelname = record.levelname
        color_info = self.level_colors.get(record.levelname, {"color": "white"})
        record.levelname = colorize(record.levelname.ljust(self.level_str_width), **color_info)
        format_str = super().format(record)
        record.levelname = old_levelname
        return format_str
