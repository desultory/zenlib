__author__ = "desultory"
__version__ = "1.0.0"


from logging import Formatter


class ColorLognameFormatter(Formatter):
    """
    ColorLognameFormatter Class
    Add the handler to the stdout handler using:
    stdout_handler = logging.StreamHandler()
    stdout_handler.setFormatter(ColorLognameFormatter())
    """

    _level_str_len = 8
    # Define the color codes
    _reset_str = '\x1b[0m'
    _grey_str = '\x1b[37m'
    _blue_str = '\x1b[34m'
    _yllw_str = '\x1b[33m'
    _sred_str = '\x1b[31m'
    _bred_str = '\x1b[31;1m'
    _magenta_str = '\x1b[35m'
    # Make the basic strings
    _debug_color_str = f"{_grey_str}DEBUG{_reset_str}".ljust(
        _level_str_len + len(_reset_str) + len(_grey_str), ' ')
    _info_color_str = f"{_blue_str}INFO{_reset_str}".ljust(
        _level_str_len + len(_reset_str) + len(_blue_str), ' ')
    _warn_color_str = f"{_yllw_str}WARNING{_reset_str}".ljust(
        _level_str_len + len(_reset_str) + len(_yllw_str), ' ')
    _error_color_str = f"{_sred_str}ERROR{_reset_str}".ljust(
        _level_str_len + len(_reset_str) + len(_sred_str), ' ')
    _crit_color_str = f"{_bred_str}CRITICAL{_reset_str}".ljust(
        _level_str_len + len(_reset_str) + len(_bred_str), ' ')
    # Format into a dict
    _color_levelname = {'DEBUG': _debug_color_str,
                        'INFO': _info_color_str,
                        'WARNING': _warn_color_str,
                        'ERROR': _error_color_str,
                        'CRITICAL': _crit_color_str}

    def __init__(self, fmt='%(levelname)s | %(message)s', *args, **kwargs):
        super().__init__(fmt, *args, **kwargs)

    def format(self, record):
        # When calling format, replace the levelname with a colored version
        # Note: the string size is greatly increased because of the color codes
        old_levelname = record.levelname
        if record.levelname in self._color_levelname:
            record.levelname = self._color_levelname[record.levelname]
        else:
            record.levelname = f"{self._magenta_str}{record.levelname}{self._reset_str}".ljust(
                self._level_str_len + len(self._magenta_str) + len(self._reset_str), ' ')

        format_str = super().format(record)

        try:
            record.levelname = old_levelname
        except NameError:
            pass

        return format_str
