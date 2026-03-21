"""
Toml file reader helper

uses tomllib.load to read the file and return the data as a dict

has an "allow_missing" arg to return an empty dict if the file is missing

if there are parser erorrs, shows the line with the issue and the error message
turns it into a formatted ValueError instead of a TOMLDecodeError, with the line number and column number highlighted in red, and the error message in yellow
"""

from pathlib import Path
from tomllib import TOMLDecodeError, load
from typing import Union

from zenlib.util.colorize import colorize as c_


def parse_line_number_from_error(e: TOMLDecodeError) -> int:
    # Try to extract line number from the error message
    try:
        return int(str(e).split("(")[1][:-1].split(",")[0].split()[-1])
    except (IndexError, ValueError):
        pass
    return -1


def parse_column_number_from_error(e: TOMLDecodeError) -> int:
    # Try to extract column number from the error message
    try:
        return int(str(e).split("(")[1][:-1].split(",")[1].split()[-1])
    except (IndexError, ValueError):
        pass
    return -1


def parse_toml(file_path: Union[Path, str], allow_missing: bool = False) -> dict:
    try:
        with open(file_path, "rb") as f:
            data = load(f)
            return data
    except FileNotFoundError:
        if allow_missing:
            return {}
        else:
            raise
    except TOMLDecodeError as e:
        line_number = getattr(e, "lineno", parse_line_number_from_error(e))
        column_number = getattr(e, "colno", parse_column_number_from_error(e))
        msg = getattr(e, "msg", str(e))
        error_msg = c_(f"[Line {c_(line_number, 'red')} column {c_(column_number, 'red')}] {c_(msg, 'yellow')}")
        with open(file_path, "r") as f:
            lines = f.readlines()
            error_line = lines[line_number - 1].rstrip() if line_number <= len(lines) else "Line number out of range"

        indicator_line = " " * (column_number - 1) + "^"

        error_msg += f"\n{error_line}\n{indicator_line}"
        raise ValueError(error_msg) from e
