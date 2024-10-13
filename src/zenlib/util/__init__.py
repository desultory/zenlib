from .handle_plural import handle_plural
from .nodupflatlist import NoDupFlatList
from .pretty_print import pretty_print
from .replace_file_line import replace_file_line
from .dict_check import contains, unset
from .main_funcs import init_logger, process_args, init_argparser, get_args_n_logger, get_kwargs_from_args, get_kwargs

__all__ = ['handle_plural', 'NoDupFlatList', 'pretty_print', 'replace_file_line',
           'init_logger', 'process_args',
           'init_argparser', 'get_args_n_logger', 'get_kwargs_from_args', 'get_kwargs',
           'contains', 'unset']
