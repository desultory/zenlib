__version__ = "0.2.0"

from enum import Enum

ANSI_START = "\x1b["


class Colors(Enum):
    RED = 31
    GREEN = 32
    YELLOW = 33
    BLUE = 34
    MAGENTA = 35
    CYAN = 36
    WHITE = 37


class ANSICode:
    def __init__(self, code, bright=False, bold=False):
        self.code = code
        self.bright = bright
        self.bold = bold

    def __str__(self):
        color_code = self.code
        color_code += 60 if self.bright else 0
        bold_str = ";1" if self.bold else ""
        return f"{ANSI_START}{color_code}{bold_str}m"


def colorize(text: str, color="white", bright=False, bold=False) -> str:
    try:
        color_code = Colors[color.upper()].value
    except (KeyError, AttributeError):
        try:
            color_code = int(color)
        except ValueError:
            raise ValueError(f"Invalid color: {color}")
        color_code = int(color)

    return f"{ANSICode(color_code, bright, bold)}{text}{ANSICode(0)}"
