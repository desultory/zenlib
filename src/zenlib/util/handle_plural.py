__author__ = "desultory"
__version__ = "2.1.0"

from collections.abc import KeysView, ValuesView


def handle_plural(function, log_level=10):
    """
    Wraps functions to take a list/dict and iterate over it.
    The last passed argument should be the iterable.
    Logs using the logger attribute if it exists.
    """
    def wrapper(self, *args):
        def log(msg, level=log_level):
            if hasattr(self, "logger"):
                self.logger.log(level, msg)

        if len(args) == 1:
            focus_arg = args[0]
            other_args = tuple()
        else:
            focus_arg = args[-1]
            other_args = args[:-1]

        if isinstance(focus_arg, list) and not isinstance(focus_arg, str):
            log("Expanding list: %s" % focus_arg)
            for item in focus_arg:
                function(self, *(other_args + (item,)))
        elif isinstance(focus_arg, ValuesView):
            log("Expanding dict values: %s" % focus_arg)
            for value in focus_arg:
                function(self, *(other_args + (value,)))
        elif isinstance(focus_arg, KeysView):
            log("Expanding dict keys: %s" % focus_arg)
            for key in focus_arg:
                function(self, *(other_args + (key,)))
        elif isinstance(focus_arg, dict):
            log("Expanding dict: %s" % focus_arg)
            for key, value in focus_arg.items():
                function(self, *(other_args + (key, value,)))
        else:
            log(f"Arguments were not expanded: {args}", log_level - 5)
            return function(self, *args)
    return wrapper
