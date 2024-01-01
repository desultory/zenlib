__author__ = "desultory"
__version__ = "1.0.0"


from zenlib.logging import loggify
from .handle_plural import handle_plural


@loggify
class NoDupFlatList(list):
    """ List that automatically filters duplicate elements when appended and concatenated. """
    def __init__(self, no_warn=False, log_bump=0, *args, **kwargs):
        self.no_warn = no_warn
        self.logger.setLevel(self.logger.parent.level + log_bump)

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
