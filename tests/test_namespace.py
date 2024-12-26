from os import environ
from unittest import TestCase, main, skipIf



from zenlib.util import nsexec


class TestPassedException(Exception):
    pass


def test_exception():
    raise TestPassedException("This is a test exception")

def test_add_func(a, b):
    return a + b

def test_uid_gid():
    import os
    return os.getuid(), os.getgid()

class TestNamespace(TestCase):
    @skipIf(environ.get("CI") == "true", "Skipping test_namespace.py in CI")
    def test_user_namespace_exceptions(self):
        with self.assertRaises(TestPassedException):
            nsexec(test_exception)

    @skipIf(environ.get("CI") == "true", "Skipping test_namespace.py in CI")
    def test_user_namespace_func(self):
        self.assertEqual(nsexec(test_add_func, 1, 2), 3)

    @skipIf(environ.get("CI") == "true", "Skipping test_namespace.py in CI")
    def test_user_namespace_uid_gid(self):
        self.assertEqual(nsexec(test_uid_gid), (0, 0))


if __name__ == "__main__":
    main()
