from zenlib.util import init_logger, init_argparser, process_args, get_kwargs_from_args


def get_args_n_logger(package, description: str, arguments=[], get_kwargs=False):
    """
    Takes a description, and list of arguments, and returns the parsed args and logger.
    """
    argparser = init_argparser(prog=package, description=description)
    logger = init_logger(package)

    for arg in arguments:
        dest = arg.pop('flags')
        argparser.add_argument(*dest, **arg)

    args = process_args(argparser, logger=logger)

    if get_kwargs:
        args = get_kwargs_from_args(args, logger=logger)

    return args, logger
