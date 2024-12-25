from unittest import TestCase, expectedFailure, main

from zenlib.util import nsexec


def test_exception():
    raise Exception("This is a test exception")


def test_add_func(a, b):
    return a + b


class TestNamespace(TestCase):
    @expectedFailure
    def test_user_namespace_exceptions(self):
        nsexec(test_exception)

    def test_user_namespace_func(self):
        self.assertEqual(nsexec(test_add_func, 1, 2), 3)


if __name__ == "__main__":
    main()
