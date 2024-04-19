__author__ = "desultory"
__version__ = "2.0.0"

from collections.abc import KeysView, ValuesView


def handle_plural(function):
    """
    Wraps functions to take a list/dict and iterate over it
    the last argument should be iterable
    """
    def wrapper(self, *args):
        if len(args) == 1:
            focus_arg = args[0]
            other_args = tuple()
        else:
            focus_arg = args[-1]
            other_args = args[:-1]

        if isinstance(focus_arg, list) and not isinstance(focus_arg, str):
            self.logger.debug("Expanding list: %s" % focus_arg)
            for item in focus_arg:
                function(self, *(other_args + (item,)))
        elif isinstance(focus_arg, ValuesView):
            self.logger.debug("Expanding dict values: %s" % focus_arg)
            for value in focus_arg:
                function(self, *(other_args + (value,)))
        elif isinstance(focus_arg, KeysView):
            self.logger.debug("Expanding dict keys: %s" % focus_arg)
            for key in focus_arg:
                function(self, *(other_args + (key,)))
        elif isinstance(focus_arg, dict):
            self.logger.debug("Expanding dict: %s" % focus_arg)
            for key, value in focus_arg.items():
                function(self, *(other_args + (key, value,)))
        else:
            self.logger.log(5, "Arguments were not expanded: %s" % args)
            return function(self, *args)
    return wrapper
