from platform import system
from sys import version_info

if version_info < (3, 12) or system() != "Linux":
    nsexec, get_id_map = None, None
else:
    from zenlib.namespace.namespace import get_id_map
    from zenlib.namespace.nsexec import nsexec

__all__ = [
    "nsexec",
    "get_id_map",
]
