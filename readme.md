![Tests](https://github.com/desultory/zenlib/actions/workflows/unit_tests.yml/badge.svg)
![Black](https://img.shields.io/badge/code%20style-black-000000.svg)


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

### ClassLogger

Like @loggify but meant to be used as a base class

### log_call

Decorator for methods, logs calls and args. Log level adjustable by changing `log_level`.

### ColorLognameFormatter

A `logging.Formatter` which colors the loglevel portion.

## Util

Helpful utility functions/decorators.

## main_funcs

A collection of functions used when starting a script.

### get_kwargs_from_args

Processes argparser args and returns a kwargs dict.

Adds a logger if passed, can apply over a base_kwargs dict.

### init_logger

Creates a logger using the passed name

### init_argparser

Creates an argparser with the passed program name/descrption.

Adds arguments for basic things such as debug levels, log files, log options

> The log options are used with `process_args` and a supplied logger.

### process_args

Takes a passed argparser and does basic argument parsing. Mostly used to handle log options for the passed logger.

### get_args_n_kwargs

Takes a package name, description, and optional arguments.

Returns the argparser.args and logger as a tuple.

Additional argparser arguments can be passed in the format:

```
ARGS = [
    {'flags': ['-p', '--port'], 'dest': 'listen_port', 'type': int, 'nargs': '?', 'help': 'Port to listen on.'},
    {'flags': ['-a', '--address'], 'dest': 'listen_ip', 'type': str, 'nargs': '?', 'help': 'Address to listen on.'},
    {'flags': ['config_file'], 'type': str, 'nargs': '?', 'help': 'Config file to use.'}]
```

> The flags are unpackes as args for argparser.add_argument while the rest of the keys are unpacked into the kwargs.

### get_kwargs

Wraps `get_args_n_kwargs` and just returns the kwargs dict

### dump_args_for_autocomplete

Prints all cmdline flags and help strings for shell autocomplete scripts to read.

The format is `flag<space>helpstring<\n>`

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
