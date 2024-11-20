from unittest import TestCase, main

from zenlib.logging import loggify


class TestLogging(TestCase):
    def test_loggify(self):
        """Test that loggify can add a logger to an object"""
        loggified_dict = loggify(dict)()
        self.assertTrue(hasattr(loggified_dict, "logger"))

    def test_log_init(self):
        """Tests that _log_init as an arg for a loggified class functions"""
        loggified_dict = loggify(dict)(_log_init=True)
        self.assertTrue(hasattr(loggified_dict, "logger"))


if __name__ == "__main__":
    main()
