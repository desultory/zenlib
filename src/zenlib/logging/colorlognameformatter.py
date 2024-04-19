__author__ = "desultory"
__version__ = "2.0.0"


from logging import Formatter


class ColorLognameFormatter(Formatter):
    """
    ColorLognameFormatter Class
    Add the handler to the stdout handler using:
    stdout_handler = logging.StreamHandler()
    stdout_handler.setFormatter(ColorLognameFormatter())
    """

    # Define the color codes
    _reset_str = '\x1b[0m'
    _grey_str = '\x1b[37m'
    _blue_str = '\x1b[34m'
    _yllw_str = '\x1b[33m'
    _sred_str = '\x1b[31m'
    _bred_str = '\x1b[31;1m'
    _magenta_str = '\x1b[35m'
    # Format into a dict
    _color_levelname = {'DEBUG': _grey_str,
                        'INFO': _blue_str,
                        'WARNING': _yllw_str,
                        'ERROR': _sred_str,
                        'CRITICAL': _bred_str}

    def __init__(self, fmt='%(levelname)s | %(message)s', *args, **kwargs):
        super().__init__(fmt, *args, **kwargs)
        self._level_str_len = max([len(name) for name in self._color_levelname])

    def color_levelname(self, levelname):
        """ Adds color to a levelname string """
        color = self._color_levelname.get(levelname, self._magenta_str)
        return f"{color}{levelname}{self._reset_str}".ljust(self._level_str_len + len(color) + len(self._reset_str), ' ')

    def format(self, record):
        # When calling format, replace the levelname with a colored version
        # Note: the string size is greatly increased because of the color codes
        old_levelname = record.levelname
        record.levelname = self.color_levelname(record.levelname)
        format_str = super().format(record)
        record.levelname = old_levelname
        return format_str
