from unittest import TestCase, main

from zenlib.logging import loggify


class TestLogging(TestCase):
    def test_loggify(self):
        """Test that loggify can add a logger to an object"""
        loggified_dict = loggify(dict)()
        self.assertTrue(hasattr(loggified_dict, "logger"))


if __name__ == "__main__":
    main()
