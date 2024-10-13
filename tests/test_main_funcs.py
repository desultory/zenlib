from argparse import ArgumentParser, Namespace
from logging import Logger
from unittest import TestCase, expectedFailure, main

from zenlib.util import get_args_n_logger, get_kwargs, get_kwargs_from_args, init_argparser, init_logger
from zenlib.util.main_funcs import dump_args_for_autocomplete, get_base_args

DEFAULT_ARGS = ["debug", "trace", "log_time", "no_log_color"]


def get_test_args():
    return [{"flags": ["arg1"], "action": "store", "nargs": "?"}, {"flags": ["arg2"], "action": "store", "nargs": "?"}]


class TestMainFuncs(TestCase):
    def test_init_logger(self):
        self.assertIsInstance(init_logger(), Logger)

    def test_init_argparser(self):
        self.assertIsInstance(init_argparser(), ArgumentParser)

    def test_named_init_argparser(self):
        parser = init_argparser("test", "test description")
        self.assertEqual(parser.prog, "test")
        self.assertEqual(parser.description, "test description")

    def _check_for_test_args(self, args):
        self.assertIsInstance(args, Namespace)
        if hasattr(args, "arg1"):
            self.assertEqual(args.arg1, "discover")
        if hasattr(args, "arg2"):
            self.assertEqual(args.arg2, "tests")

    def test_get_args_n_logger(self):
        args, logger = get_args_n_logger("zenlib_test", "test description", get_test_args())
        self.assertIsInstance(logger, Logger)
        self._check_for_test_args(args)

    def test_get_args_n_logger_no_default(self):
        args, logger = get_args_n_logger("zenlib_test", "test description", get_test_args(), drop_default=True)
        self.assertIsInstance(logger, Logger)

        for arg in DEFAULT_ARGS:
            self.assertFalse(hasattr(args, arg))

    def test_get_kwargs_from_args(self):
        args, logger = get_args_n_logger("zenlib_test", "test description", get_test_args())
        self._check_for_test_args(args)
        kwargs = get_kwargs_from_args(args, logger)
        self.assertIsInstance(kwargs, dict)
        self.assertEqual(kwargs["logger"], logger)

    def test_not_drop_base(self):
        args, logger = get_args_n_logger("zenlib_test", "test description", get_test_args())
        self._check_for_test_args(args)
        kwargs = get_kwargs_from_args(args, logger, drop_base=False)
        self.assertIsInstance(kwargs, dict)
        self.assertEqual(kwargs["logger"], logger)
        for arg in DEFAULT_ARGS:
            self.assertTrue(arg in kwargs)

    def test_get_kwargs(self):
        kwargs = get_kwargs("zenlib_test", "test description", get_test_args())
        self.assertIsInstance(kwargs, dict)
        self.assertTrue("logger" in kwargs)

    @expectedFailure  # This exits so should fail
    def test_dump_args_for_autocomplete(self):
        dump_args_for_autocomplete(get_test_args())

    def test_dump_args_for_autocomplete_no_exit(self):
        self.assertEqual(dump_args_for_autocomplete(get_test_args(), test=True), "")
        self.assertEqual(
            dump_args_for_autocomplete(get_base_args(), test=True),
            "-d enable debug mode (level 10)\n--debug enable debug mode (level 10)\n-dd enable trace debug mode (level 5)\n--trace enable trace debug mode (level 5)\n-v print the version and exit\n--version print the version and exit\n--log-time enable log timestamps\n--no-log-color disable log color\n",
        )


if __name__ == "__main__":
    main()
