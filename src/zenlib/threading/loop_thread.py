__author__ = "desultory"
__version__ = "1.0.0"


def loop_thread(function):
    """
    Wrapper for a method already wrapped with add_thread.
    Causes the method to loop until the _running_{name} event is cleared.
    """
    def loop_wrapper(self, *args, **kwargs):
        while getattr(self, f"_running_{function.__name__}").is_set():
            function(self, *args, **kwargs)
        self.logger.info("Thread received stop signal: %s" % function.__name__)
    return loop_wrapper
