__author__ = 'desultory'
__version__ = '0.1.0'

from threading import Thread
from zenlib.logging import loggify
from inspect import signature


@loggify
class ZenThread(Thread):
    """ A thread that stores the exception and return value of the function it runs. """
    def __init__(self, owner=None, *args, **kwargs):
        self._getattr_log_ignore += ['_target', '_delete', '_bootstrap', '_bootstrap_inner',
                                     '_set_ident', '_set_tstate_lock', '_set_native_id']
        super().__init__(*args, **kwargs)
        self.owner = owner
        self.exception = None
        self.return_value = None

    def run(self):
        """
        Runs the thread and stores the exception and return value.
        Adds the owner to the args if the function has a self parameter.
        """
        try:
            self.logger.info("Starting thread: %s", self.name)
            args = self._args
            try:
                if signature(self._target).parameters.get('self'):
                    if not self.owner:
                        raise ValueError("Thread target has self parameter but no owner was provided: %s" % self._target.__name__)
                    args = (self.owner,) + self._args
            except ValueError:
                pass

            self.logger.debug("Thread args: %s", args)
            self.logger.debug("Thread kwargs: %s", self._kwargs)

            self.return_value = self._target(*args, **self._kwargs)

        except Exception as e:
            self.exception = e
            self.logger.error("[%s] Thread args: %s" % (self._target.__name__, self._args))
            self.logger.error("[%s] Thread kwargs: %s" % (self._target.__name__, self._kwargs))
            self.logger.exception(e)
        finally:
            del self._target, self._args, self._kwargs

