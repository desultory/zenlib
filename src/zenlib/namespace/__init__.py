from os import environ
if not environ.get("CI"):
    from .nsexec import nsexec
    from .namespace import get_id_map
else:
    nsexec, get_id_map = None, None

__all__ = [
    "nsexec",
    "get_id_map",
]
