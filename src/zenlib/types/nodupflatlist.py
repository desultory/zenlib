__author__ = "desultory"
__version__ = "1.1.0"


from zenlib.logging import ClassLogger
from zenlib.util import handle_plural


class NoDupFlatList(ClassLogger, list):
    """List that automatically filters duplicate elements when appended and concatenated."""

    def __init__(self, no_warn=False, *args, **kwargs):
        if log_bump := kwargs.pop("log_bump", 0):
            kwargs["_log_bump"] = log_bump
        super().__init__(*args, **kwargs)
        self.no_warn = no_warn

    @handle_plural
    def append(self, item):
        from collections.abc import Iterable

        if isinstance(item, Iterable) and not isinstance(item, str):
            self.logger.debug("Adding list items: %s" % item)
            self.append(item)
        elif item not in self:
            self.logger.debug("Adding list item: %s" % item)
            super().append(item)
        elif not self.no_warn:
            self.logger.warning("List item already exists: %s" % item)

    def __iadd__(self, item):
        self.append(item)
        return self
