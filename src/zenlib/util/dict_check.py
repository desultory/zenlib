__author__ = "desultory"
__version__ = "2.0.0"

from functools import wraps
from typing import Any, Callable, Concatenate, ParamSpec, Protocol, TypeVar

from zenlib.typing.haslogger import HasLogger

P = ParamSpec("P")
R = TypeVar("R")


class LoggerDict(HasLogger, Protocol):
    def __contains__(self, key: str) -> bool: ...
    def get(self, key: str, default: Any = None) -> Any: ...


SelfT = TypeVar("SelfT", bound=LoggerDict)


def return_check(self: HasLogger, message: str, raise_exception: bool, log_level: int, return_val=None) -> str:
    if raise_exception:
        raise ValueError(message)
    self.logger.log(log_level, message)
    return return_val


def contains(
    key: str,
    message: str | None = None,
    is_set: bool = True,
    raise_exception: bool = False,
    log_level: int = 10,
    debug_level: int = 5,
) -> Callable[[Callable[Concatenate[SelfT, P], R]], Callable[Concatenate[SelfT, P], R | None]]:
    """
    Ensure that the key exists in the dictionary. (self/first arg)

    Returns the message/exception if the key is not found.

    If raise_exception is true, raises an exception if the key is missing/undefined.
    If is_set is True, then the key must have a value. (disable to just check the key is defined)

    debug_level is used for successes
    log_level is used for failures (when exceptions are not raised)
    """

    def _dict_contains(func: Callable[Concatenate[SelfT, P], R]) -> Callable[Concatenate[SelfT, P], R | None]:
        @wraps(func)
        def _contains(self: SelfT, *args: P.args, **kwargs: P.kwargs):
            msg = f"[{func.__name__}] {message}" if message else ""
            value = self.get(key)
            if key not in self:
                return return_check(
                    self, msg or f"[{func.__name__}] Unable to find key: {key}.", raise_exception, log_level
                )
            if is_set and (not value or repr(value) == "PosixPath('.')"):
                return return_check(
                    self, msg or f"[{func.__name__}] Key is not set: {key}.", raise_exception, log_level
                )
            self.logger.log(debug_level, f"[{func.__name__}] Contains check passed for: {key}")
            return func(self, *args, **kwargs)

        return _contains

    return _dict_contains


def unset(
    key: str, message: str | None = None, raise_exception: bool = False, log_level: int = 10, debug_level: int = 5
) -> Callable[[Callable[Concatenate[SelfT, P], R]], Callable[Concatenate[SelfT, P], R | None]]:
    """
    Ensure that the key does not exist in the dictionary. (self/first arg)

    Returns the message/exception if the key is found

    If it exists, make sure it is not set (not an empty/default value)

    if raise_exception is true, raises an exception if the key is defined.

    debug_level is used for successes
    log_level is used for failures (when exceptions are not raised)
    """

    def _dict_unset(func: Callable[Concatenate[SelfT, P], R]) -> Callable[Concatenate[SelfT, P], R | None]:
        @wraps(func)
        def _unset(self: SelfT, *args: P.args, **kwargs: P.kwargs):
            msg = f"[{func.__name__}] {message}" if message else ""
            value = self.get(key)
            if key in self and (repr(value) != "PosixPath('.')" and value):
                return return_check(
                    self,
                    msg or f"[{func.__name__}] Key '{key}' is set: {repr(value)}",
                    raise_exception,
                    log_level,
                )
            self.logger.log(debug_level, f"[{func.__name__}] Unset check passed for: {key}; {repr(value)}")
            return func(self, *args, **kwargs)

        return _unset

    return _dict_unset
