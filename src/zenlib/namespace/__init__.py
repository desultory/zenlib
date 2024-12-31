from os import environ
from platform import system
from sys import version_info

if environ.get("CI", "false").lower() == "true" or version_info < (3, 12) or system() != "Linux":
    nsexec, get_id_map = None, None
else:
    from .namespace import get_id_map
    from .nsexec import nsexec

__all__ = [
    "nsexec",
    "get_id_map",
]
