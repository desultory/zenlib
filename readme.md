# Zenlib

Personal functions, classes, and decorators used in some of my projects


## Logging

### @loggify

This decorator can be added to any class to initialize it with a logger, and add extra logging functionality to that class

### ColorLognameFormatter

A `logging.Formatter` which colors the loglevel portion.

## Threading

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

### @handle_plural

This decorator is designed to be added to functions, automatically expands pased dicts/lists into the function it wraps.

> This function does not return values for most operations, it is designed to be used within a class where the wrapped function sets class attributes.

### NoDupFlatList

Essentially a dumb set, but is a list so is ordered

### pretty_print

A function designed to print complex data structures in a nice manner

### replace_file_line

Replaces a line in a file

`def replace_file_line(file_path, old_line, new_line):`

### update_init

Used by `@add_thread`, appends the passed function to the init of a class.



