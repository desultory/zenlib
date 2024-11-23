from .dict_check import contains, unset
from .handle_plural import handle_plural
from .main_funcs import get_args_n_logger, get_kwargs, get_kwargs_from_args, init_argparser, init_logger, process_args
from .merge_class import merge_class
from .pretty_print import pretty_print
from .replace_file_line import replace_file_line

__all__ = [
    "handle_plural",
    "NoDupFlatList",
    "pretty_print",
    "replace_file_line",
    "init_logger",
    "process_args",
    "init_argparser",
    "get_args_n_logger",
    "get_kwargs_from_args",
    "get_kwargs",
    "contains",
    "unset",
    "merge_class",
]
