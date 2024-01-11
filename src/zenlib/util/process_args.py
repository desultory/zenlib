from zenlib.logging import ColorLognameFormatter


def process_args(argparser, logger=None):
    args = argparser.parse_args()
    if args.version:
        package = argparser.prog
        from importlib.metadata import version
        print(f"{package} {version(package)}")
        exit(0)

    if logger:
        if args.verbose:
            logger.setLevel(5)
            formatter = ColorLognameFormatter('%(levelname)s | %(name)-42s | %(message)s')
        elif args.debug:
            logger.setLevel(10)
            formatter = ColorLognameFormatter('%(levelname)s | %(name)-42s | %(message)s')
        else:
            logger.setLevel(20)
            formatter = ColorLognameFormatter()

        # Add the formatter to the first handler, or add a new handler
        for handler in logger.handlers:
            handler.setFormatter(formatter)
            break
        else:
            from logging import StreamHandler
            handler = StreamHandler()
            handler.setFormatter(formatter)
            logger.addHandler(handler)

    return args
