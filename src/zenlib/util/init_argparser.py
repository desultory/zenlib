from argparse import ArgumentParser


def init_argparser(prog=None, description=None):
    argparser = ArgumentParser(prog=prog, description=description)
    argparser.add_argument('-d', '--debug', action='store_true', help='Debug mode.')
    argparser.add_argument('-dd', '--verbose', action='store_true', help='Verbose debug mode.')
    argparser.add_argument('-v', '--version', action='store_true', help='Print the version and exit.')

    return argparser

