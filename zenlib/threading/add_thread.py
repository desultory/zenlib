__author__ = "desultory"
__version__ = "1.0.0"

from threading import Thread, Event
from zenlib.utils import update_init


def add_thread(name, target, description=None):
    """
    Adds a thread of a class which targets the target
    Creates a dict that contains the name of the thread as a key, with the thread as a value
    Cteates basic helper functions to manage the thread
    """
    def decorator(cls):
        def create_thread(self):
            if not hasattr(self, 'threads'):
                self.threads = dict()

            if "." in target:
                target_parts = target.split(".")
                target_attr = self
                for part in target_parts:
                    target_attr = getattr(target_attr, part)
            else:
                target_attr = getattr(self, target)

            self.threads[name] = Thread(target=target_attr, name=description)
            self.logger.info("Created thread: %s" % name)

        def start_thread(self):
            thread = self.threads[name]
            setattr(self, f"_stop_processing_{name}", Event())
            if thread._is_stopped:
                self.logger.info("Re-creating thread")
                getattr(self, f"create_{name}_thread")()
                thread = self.threads[name]

            if thread._started.is_set() and not thread._is_stopped:
                self.logger.warning("%s thread is already started" % name)
            else:
                self.logger.info("Starting thread: %s" % name)
                thread.start()
                return True

        def stop_thread(self):
            thread = self.threads[name]
            dont_join = False
            if not thread._started.is_set() or thread._is_stopped:
                self.logger.warning("Thread is not active: %s" % name)
                dont_join = True

            if hasattr(self, f"_stop_processing_{name}"):
                self.logger.debug("Setting stop event for thread: %s" % name)
                getattr(self, f"_stop_processing_{name}").set()

            if hasattr(self, f"stop_{name}_thread_actions"):
                self.logger.debug("Calling: %s" % f"stop_{name}_thread_actions")
                getattr(self, f"stop_{name}_thread_actions")()

            if hasattr(self, f"_{name}_timer"):
                self.logger.info("Stopping the timer for thread: %s" % name)
                getattr(self, f"_{name}_timer").cancel()

            if not dont_join:
                self.logger.info("Waiting on thread to end: %s" % name)
                thread.join()
            return True

        setattr(cls, f"create_{name}_thread", create_thread)
        setattr(cls, f"start_{name}_thread", start_thread)
        setattr(cls, f"stop_{name}_thread", stop_thread)

        return update_init(create_thread)(cls)
    return decorator
