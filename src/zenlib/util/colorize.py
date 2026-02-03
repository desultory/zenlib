__version__ = "0.4.0"


from dataclasses import dataclass
from enum import Enum

import zenlib

ANSI_START = "\x1b["


class Formatters(Enum):
    BOLD = 1
    DIM = 2
    ITALIC = 3
    UNDERLINE = 4
    BLINK = 5
    FAST_BLINK = 6
    REVERSE = 7
    HIDDEN = 8
    STRIKETHROUGH = 9


class Colors(Enum):
    RED = 31
    GREEN = 32
    YELLOW = 33
    BLUE = 34
    MAGENTA = 35
    CYAN = 36
    WHITE = 37


@dataclass
class ANSICode:
    code: int
    bright: bool = False
    background: bool = False
    bold: bool = False
    dim: bool = False
    italic: bool = False
    underline: bool = False
    blink: bool = False
    fast_blink: bool = False
    reverse: bool = False
    hidden: bool = False
    strikethrough: bool = False

    @property
    def formatters(self):
        return [str(formatter.value) for formatter in Formatters if getattr(self, formatter.name.lower())]

    def __str__(self):
        color_code = self.code
        color_code += 60 if self.bright else 0
        color_code += 10 if self.background else 0
        if formatters := self.formatters:
            color_code = f"{color_code};{';'.join(formatters)}"
        return f"{ANSI_START}{color_code}m"


def colorize(text: str, color="white", *args, **kwargs) -> str:
    if not zenlib._ZENLIB_COLOR_TEXT:
        return text

    try:
        color_code = Colors[color.upper()].value
    except (KeyError, AttributeError):
        try:
            color_code = int(color)
        except ValueError:
            raise ValueError(f"Invalid color: {color}")
        color_code = int(color)

    return f"{ANSICode(color_code, *args, **kwargs)}{text}{ANSICode(0)}"
