__author__ = "desultory"
__version__ = "1.0.0"


def update_init(decorator):
    """
    Updates the init function of a class, puts the decorated function at the end of the init.
    Useful for function decorators that edit a class instance.
    """
    def decorator_wrapper(cls):
        original_init = cls.__init__

        def new_init(self, *args, **kwargs):
            original_init(self, *args, **kwargs)
            decorator(self)

        cls.__init__ = new_init
        return cls
    return decorator_wrapper
