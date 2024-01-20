from zenlib.logging import ColorLognameFormatter
from logging import Formatter


def process_args(argparser, logger=None):
    args = argparser.parse_args()
    if args.version:
        package = argparser.prog
        from importlib.metadata import version
        print(f"{package} {version(package)}")
        exit(0)

    if logger:
        if args.log_level is not None:
            log_level = int(args.log_level)
        elif args.verbose:
            log_level = 5
        elif args.debug:
            log_level = 10
        else:
            log_level = 20
        logger.setLevel(log_level)

        format_str = '%(asctime)s | ' if args.log_time else ''
        if log_level < 20:
            format_str += '%(levelname)s | %(name)-42s | %(message)s'
        else:
            format_str += '%(levelname)s | %(message)s'
        formatter = ColorLognameFormatter(format_str) if not args.no_log_color else Formatter(format_str)

        # Add the formatter to the first handler, or add a new handler
        for handler in logger.handlers:
            handler.setFormatter(formatter)
            break
        else:
            from logging import StreamHandler, FileHandler
            handler = StreamHandler() if args.log_file is None else FileHandler(args.log_file)
            handler.setFormatter(formatter)
            logger.addHandler(handler)

    return args
