# Zenlib

Personal functions, classes, and decorators used in some of my projects

## Logging

### @loggify

This decorator can be added to any class to initialize it with a logger, and add extra logging functionality to that class.

The following additional kwargs are handled in __init__:

* `logger` (Logger) Used as the parent logger, if not set, uses the root logger.
* `_log_init` (bool) Can be passed to loggified classes, to enable or disable additional initialization logging.
* `_log_bump` (int) Changes the log level for added loggers.

Loggified classes will also log use of \_\_setattr\_\_,  and \_\_getitem\_\_.

### log_call

Decorator for methods, logs calls and args. Log level adjustable by chaning `log_level`.

### ColorLognameFormatter

A `logging.Formatter` which colors the loglevel portion.

## Threading

### ZenThread

An extension of the builtin thread that sets results to self.return_value and exceptions to self.exception.

Supports re-starting and looping with the self.loop event.

### @threaded

Runs the wrapped function in a thread when called.

Adds the thread to `_threads` within the object.

If an exception is raised, it will be added to `self._threads` in the form `(thread, exception_queue)`.

### @thread_wrapped('threadname')

Meant to be used with `@add_thread`, the argument is the threadname that function is associated with.

### @add_thread('threadname', 'target_function', 'description')

`@add_thread` decorates a class, and adds `create_{threadname}_thread`, `start_` and `stop_` functions which are used to handle thread management of a `thread_wrapped` function.

Once added, a thread will be added to `self.threads[threadname]`.

## Util

Helpful utility functions/decorators.

## @handle_plural

This decorator is designed to be added to functions, automatically expands pased dicts/lists into the function it wraps.

> This function does not return values for most operations, it is designed to be used within a class where the wrapped function sets class attributes.

## NoDupFlatList

Essentially a dumb set, but is a list so is ordered

## pretty_print

A function designed to print complex data structures in a nice manner

## replace_file_line

Replaces a line in a file

`def replace_file_line(file_path, old_line, new_line):`

## update_init

Used by `@add_thread`, appends the passed function to the init of a class.

## walk_dict

Takes two dicts as args, walks the first dict using the structure of the second dict.
If `fail_safe` is set, returns none when keys can't be found.

## check_dict

This decorator can be added to a function to check for the presence or lack of a dict item.

> By default, it will print an error message, but will use self.logger if it exists in the class whose method is decorated.
> This logger will be created automatically if the clsss is wrapped with @loggify.

The first arg (`key`) is required. The `validate_dict` arg is initially unset, and allows the dict which is being checked to be changed.

If `key` is a dict, the structure will be used to walk the `validate_dict`.

> The decorator will read args[0] at runtime, and if this is a dict, it will use that if `validate_dict` is not set.
> Functionally, this reads `self` and allows this decorator to be used to check for dict items within a class with a  `__dict__`

* `value_arg` Defines the value to compare found keys against.
* `contains` Is a boolean that enables checking for the `value_arg` as the name of a key in `validate_dict`.
* `unset` Is a boolean used to make validation pass if the `key` is not found.
* `raise_exception` Causes a ValueError to be rasied instead of printing an error message.
* `log_level` (10) Defines the log level to send the message to.
* `return_val` (False) Defines the default return value to use when validation fails.
* `return_arg` Return this argument (by number) when validation fails.
* `message` Set the vailidation failure message.

Additional arguments exist to set a value to compare found keys against
