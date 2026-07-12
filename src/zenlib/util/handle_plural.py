__author__ = "desultory"
__version__ = "2.2.1"

from collections.abc import KeysView, ValuesView


def handle_plural(function, log_level=5):
    """
    Wraps functions to take a list/dict and iterate over it.
    The last passed argument should be the iterable.
    Logs using the logger attribute if it exists.
    """

    def wrapper(self, *args, **kwargs):
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
            log(f"Expanding list: {focus_arg}")
            for item in focus_arg:
                function(self, *(other_args + (item,)), **kwargs)
        elif isinstance(focus_arg, set):
            log(f"Expanding set: {focus_arg}")
            for item in focus_arg:
                function(self, *(other_args + (item,)), **kwargs)
        elif isinstance(focus_arg, ValuesView):
            log(f"Expanding dict values: {focus_arg}")
            for value in focus_arg:
                function(self, *(other_args + (value,)), **kwargs)
        elif isinstance(focus_arg, KeysView):
            log(f"Expanding dict keys: {focus_arg}")
            for key in focus_arg:
                function(self, *(other_args + (key,)), **kwargs)
        elif isinstance(focus_arg, dict):
            log(f"Expanding dict: {focus_arg}")
            for key, value in focus_arg.items():
                function(
                    self,
                    *(
                        other_args
                        + (
                            key,
                            value,
                        )
                    ),
                    **kwargs,
                )
        else:
            log(f"Arguments were not expanded: {args}", log_level - 5)
            return function(self, *args, **kwargs)

    return wrapper
