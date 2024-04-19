__author__ = 'desultory'
__version__ = '1.0.0'

from threading import Thread, Event
from zenlib.logging import ClassLogger


class ZenThread(ClassLogger, Thread):
    """ A thread that stores the exception and return value of the function it runs. """
    def __init__(self, looping=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.exception = None
        self.return_value = None
        self.loop = Event()
        self._looping = looping

    def start(self):
        """ Starts the thread, sets the loop event if self._looping is True. """
        if self._looping:
            self.loop.set()
        self.logger.info("Starting thread: %s", self.name)
        super().start()

    def run(self):
        """
        Runs the thread and stores the exception and return value.
        Clears the started flag when finished, does not delete the target.
        """
        if not self._started.is_set():
            raise RuntimeError("Cannot run thread that has not been started: %s", self.name)

        try:
            while True:
                self.return_value = self._target(*self._args, **self._kwargs)
                if not self.loop.is_set():
                    break
        except Exception as e:
            self.exception = e
            self.logger.error("[%s] Thread args: %s" % (self._target.__name__, self._args))
            self.logger.error("[%s] Thread kwargs: %s" % (self._target.__name__, self._kwargs))
            self.logger.exception(e)
        self.logger.info("Thread finished: %s", self.name)
        self._started.clear()

