__author__ = "desultory"
__version__ = "1.0.0"


def thread_wrapped(thread_name):
    """
    Wrap a class function to be used with add_thread
    """
    def decorator(function):
        def wrapper(self, *args, **kwargs):
            self.logger.info("Starting the processing loop for thread: %s" % thread_name)
            while not getattr(self, f"_stop_processing_{thread_name}").is_set():
                function(self, *args, **kwargs)
            self.logger.info("The processing loop has ended for thread: %s" % thread_name)
        return wrapper
    return decorator
