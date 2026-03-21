__author__ = "desultory"
__version__ = "1.3.0"

from collections.abc import Iterable
from typing import Self, TypeVar

from zenlib.logging.classlogger import ClassLogger
from zenlib.util.handle_plural import handle_plural

T = TypeVar("T")


class NoDupFlatList(ClassLogger, list[T]):
    """List that automatically filters duplicate elements when appended and concatenated."""

    def __init__(self, no_warn: bool = False, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.no_warn: bool = no_warn

    @handle_plural
    def append(self, item: T | Iterable[T]) -> None:
        """Adds an item or items to the list, avoiding duplicates.
        If the item is an iterable (but not a string), each element is added individually. (recursive)
        """
        if isinstance(item, Iterable) and not isinstance(item, str):
            self.logger.debug("Adding list items: %s" % item)
            self.append(item)
        elif item not in self:
            self.logger.debug("Adding list item: %s" % item)
            super().append(item)
        elif not self.no_warn:
            self.logger.warning("List item already exists: %s" % item)

    # Ignore type checking for __iadd__ method, we think we know what we're doing
    def __iadd__(self, item: Iterable[T]) -> Self:  # type: ignore[misc,override]
        """Implements the += operator to add items from an iterable, avoiding duplicates.
        Passes any input to the append method.

        The handle_plural decorator will expand any input while adding
        """
        self.append(item)
        return self

    def copy(self) -> "NoDupFlatList[T]":
        """Returns a copy of the NoDupFlatList."""
        new_obj = type(self)(no_warn=self.no_warn, logger=self.logger)
        new_obj.extend(self)
        return new_obj
