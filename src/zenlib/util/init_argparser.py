from argparse import ArgumentParser


def init_argparser(prog=None, description=None):
    argparser = ArgumentParser(prog=prog, description=description)
    argparser.add_argument('-d', '--debug', action='store_true', help='Debug mode.')
    argparser.add_argument('-dd', '--verbose', action='store_true', help='Verbose debug mode.')
    argparser.add_argument('-v', '--version', action='store_true', help='Print the version and exit.')
    argparser.add_argument('--log-file', type=str, help='Log file path.')
    argparser.add_argument('--log-level', type=str, help='Log level.')
    argparser.add_argument('--log-time', action='store_true', help='Log timestamps.')
    argparser.add_argument('--no-log-color', action='store_true', help='Disable log color.')

    return argparser

