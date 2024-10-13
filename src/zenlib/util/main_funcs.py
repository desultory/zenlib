"""
Functions to help with the main()
"""

__version__ = "1.2.1"
__author__ = "desultory"


def get_base_args():
    return [
        {"flags": ["-d", "--debug"], "action": "store_true", "help": "enable debug mode (level 10)"},
        {"flags": ["-dd", "--trace"], "action": "store_true", "help": "enable trace debug mode (level 5)"},
        {"flags": ["-v", "--version"], "action": "store_true", "help": "print the version and exit"},
        {"flags": ["--log-file"], "type": str, "help": "set the path to the log file"},
        {"flags": ["--log-level"], "type": str, "help": "set the log level"},
        {"flags": ["--log-time"], "action": "store_true", "help": "enable log timestamps"},
        {"flags": ["--no-log-color"], "action": "store_true", "help": "disable log color"},
    ]


def init_logger(name=None):
    """Initialize the logger with a name"""
    from logging import getLogger

    name = name or __name__
    return getLogger(name)


def init_argparser(prog=None, description=None):
    """Initialize an argparser with common options."""
    from argparse import ArgumentParser

    argparser = ArgumentParser(prog=prog, description=description)
    return argparser


def get_kwargs_from_args(args, logger=None, base_kwargs={}, drop_base=True):
    """Get kwargs from argparser args.
    Drop base doesn't add init_argparser args."""
    kwargs = base_kwargs.copy()
    if logger is not None:
        kwargs["logger"] = logger

    for arg in vars(args):
        if drop_base and arg in ["debug", "trace", "version", "log_file", "log_level", "log_time", "no_log_color"]:
            continue
        value = getattr(args, arg)

        if value is None:
            continue

        kwargs[arg] = value
    return kwargs


def process_args(argparser, logger=None):
    """Process argparser args, optionally configuring a logger."""
    from logging import Formatter

    from zenlib.logging import ColorLognameFormatter

    args = argparser.parse_args()
    if args.version and argparser.prog != "zenlib_test":
        package = argparser.prog
        from importlib.metadata import version

        print(f"{package} {version(package)}")
        exit(0)

    if logger:
        if args.log_level is not None:
            log_level = int(args.log_level)
        elif args.trace:
            log_level = 5
        elif args.debug:
            log_level = 10
        else:
            log_level = 20
        logger.setLevel(log_level)

        format_str = "%(asctime)s | " if args.log_time else ""
        if log_level < 20:
            format_str += "%(levelname)s | %(name)-42s | %(message)s"
        else:
            format_str += "%(levelname)s | %(message)s"
        formatter = ColorLognameFormatter(format_str) if not args.no_log_color else Formatter(format_str)

        # Add the formatter to the first handler, or add a new handler
        for handler in logger.handlers:
            handler.setFormatter(formatter)
            break
        else:
            from logging import FileHandler, StreamHandler

            handler = StreamHandler() if args.log_file is None else FileHandler(args.log_file)
            handler.setFormatter(formatter)
            logger.addHandler(handler)

    return args


def dump_args_for_autocomplete(args, test=False):
    """Dump args for autocomplete"""
    out_str = ""
    for arg in args:
        if arg.get("action") not in ["store_true", "store_false"]:
            continue
        for flag in arg["flags"]:
            out_str += f"{flag} {arg.get('help')}\n"
    if test:
        return out_str
    print(out_str)
    exit(0)


def get_args_n_logger(package, description: str, arguments=[], drop_default=False):
    """Takes a package name and description
    If arguments are passed, they are added to argparser.
    Returns the parsed args and logger.
    """
    arguments = get_base_args() + arguments
    from sys import argv

    if "--dump_args" in argv:
        dump_args_for_autocomplete(arguments)

    from argparse import Namespace

    argparser = init_argparser(prog=package, description=description)
    logger = init_logger(package)

    for arg in arguments:
        dest = arg.pop("flags")
        if drop_default:
            arg["default"] = None
        argparser.add_argument(*dest, **arg)

    args = process_args(argparser, logger=logger)

    if drop_default:
        args = Namespace(**{name: value for name, value in vars(args).items() if value != argparser.get_default(name)})

    return args, logger


def get_kwargs(package, description: str, arguments=[], base_kwargs={}, drop_default=False, drop_base=True):
    """Like get_args_n_logger, but only returns kwargs"""
    args, logger = get_args_n_logger(package, description, arguments, drop_default=drop_default)
    return get_kwargs_from_args(args, logger=logger, base_kwargs=base_kwargs, drop_base=drop_base)
