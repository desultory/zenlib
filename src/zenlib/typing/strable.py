"""
typing type for something that is "str" able
"""

from typing import Protocol

class Strable(Protocol):
    """
    Protocol for something that is "str" able
    """

    def __str__(self) -> str:
        """
        Return a string representation of the object.
        """
        ...
