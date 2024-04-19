__author__ = "desultory"
__version__ = "2.0.0"

from .zenthread import ZenThread
from threading import Event
from zenlib.util import update_init


def add_thread(name, target, description=None):
    """
    Adds a thread to a class instance.
    The target is the function that the thread will run.
    The description is passed to the thread as the name.
    Creates a dictionary of threads in the class instance called threads.
    The key is the name of the thread.
    The value is the thread object.
    """
    def decorator(cls):
        def create_thread(self):
            """
            This method reads the target from the decorator.
            It is added to the class as f'create_{name}_thread'.
            """
            # If the tharget has a dot in it, it is a path to a function
            if "." in target:
                target_parts = target.split(".")
                target_attr = self
                for part in target_parts:
                    target_attr = getattr(target_attr, part)
            else:
                target_attr = getattr(self, target)

            self.threads[name] = ZenThread(target=target_attr, name=description,
                                           owner=self, logger=self.logger)

        def start_thread(self):
            thread = self.threads[name]
            if thread._is_stopped:
                self.logger.info("Re-creating thread")
                getattr(self, f"create_{name}_thread")()
                thread = self.threads[name]

            if thread._started.is_set() and not thread._is_stopped:
                self.logger.warning("Thread is already started: %s" % name)
            else:
                getattr(self, f"_running_{name}").set()
                thread.start()
            return thread

        def stop_thread(self, force=False):
            thread = self.threads[name]
            dont_join = False
            if not thread._started.is_set() or thread._is_stopped:
                self.logger.warning("Thread is not active: %s" % name)
                dont_join = True

            if hasattr(self, f"_running_{name}"):
                self.logger.debug("Clearing running event for thread: %s" % name)
                getattr(self, f"_running_{name}").clear()

            if hasattr(self, f"stop_{name}_thread_actions"):
                self.logger.info("Calling: %s" % f"stop_{name}_thread_actions")
                getattr(self, f"stop_{name}_thread_actions")()

            if hasattr(self, f"_{name}_timer"):
                self.logger.info("Stopping the timer for thread: %s" % name)
                getattr(self, f"_{name}_timer").cancel()

            if force:
                self.logger.info("Stopping thread: %s" % name)
                thread.stop()

            if not dont_join:
                self.logger.info("Waiting on thread to end: %s" % name)
                thread.join()

        setattr(cls, f"create_{name}_thread", create_thread)
        setattr(cls, f"start_{name}_thread", start_thread)
        setattr(cls, f"stop_{name}_thread", stop_thread)
        setattr(cls, f"_running_{name}", Event())
        cls.threads = {}

        # Update the __init__ method of the class
        return update_init(create_thread)(cls)
    return decorator
