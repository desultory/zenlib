
"""
Get kwargs from argparser args
"""


def get_kwargs_from_args(args, logger=None, base_kwargs={}):
    """
    Get kwargs from argparser args
    """
    kwargs = base_kwargs.copy()
    if logger is not None:
        kwargs['logger'] = logger

    for arg in vars(args):
        value = getattr(args, arg)
        if value is None or value is False:
            continue

        kwargs[arg] = value
    return kwargs


