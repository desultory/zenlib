__author__ = 'desultory'
__version__ = '1.0.0'

from threading import Thread
from queue import Queue


def threaded(function):
    """
    Simply starts a function in a thread
    Adds it to an internal _threads list for handling
    """
    def wrapper(self, *args, **kwargs):
        if not hasattr(self, '_threads'):
            self._threads = list()

        thread_exception = Queue()

        def exception_wrapper(*args, **kwargs):
            try:
                function(*args, **kwargs)
            except Exception as e:
                self.logger.warning("Exception in thread: %s" % function.__name__)
                thread_exception.put(e)
                self.logger.debug(e)

        thread = Thread(target=exception_wrapper, args=(self, *args), kwargs=kwargs, name=function.__name__)
        thread.start()
        self._threads.append((thread, thread_exception))
    return wrapper
