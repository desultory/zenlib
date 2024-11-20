from unittest import TestCase, main

from zenlib.logging import loggify, ClassLogger
from logging import Handler, getLogger, Formatter


class TestClass(ClassLogger):
    __version__ = "1.2.3"


class TestHandler(Handler):
    """ Test handler which simply stores emitted records """
    def __init__(self):
        super().__init__()
        self.formatter = Formatter("%(levelname)s: %(message)s")
        self.records = []

    def emit(self, record):
        self.records.append(self.format(record))


class TestLogging(TestCase):
    def test_loggify(self):
        """Test that loggify can add a logger to an object"""
        loggified_dict = loggify(dict)()
        self.assertTrue(hasattr(loggified_dict, "logger"))

    def test_class_logger(self):
        """Tests that ClassLogger can be used to add a logger to a class"""
        test_class = TestClass()
        self.assertTrue(hasattr(test_class, "logger"))

    def test_loggify_log_init(self):
        """Tests that _log_init as an arg for a loggified class functions"""
        test_logger = getLogger("test_logger")
        test_handler = TestHandler()
        test_logger.setLevel(5)
        test_logger.addHandler(test_handler)
        loggified_dict = loggify(dict)(logger=test_logger, _log_init=True)
        self.assertTrue(hasattr(loggified_dict, "logger"))
        self.assertIn("INFO: Initializing class: dict", test_handler.records)
        self.assertIn("DEBUG: [dict] Package version not found for: builtins", test_handler.records)

    def test_class_logger_log_init(self):
        """Tests that _log_init as an arg for a ClassLogger class functions"""
        test_logger = getLogger("test_logger")
        test_handler = TestHandler()
        test_logger.setLevel(5)
        test_logger.addHandler(test_handler)
        test_class = TestClass(logger=test_logger, _log_init=True)
        self.assertTrue(hasattr(test_class, "logger"))
        self.assertIn("INFO: Initializing class: TestClass", test_handler.records)
        self.assertIn("DEBUG: [TestClass] Package version not found for: tests", test_handler.records)
        self.assertIn("INFO: [TestClass] Class version: 1.2.3", test_handler.records)


if __name__ == "__main__":
    main()
