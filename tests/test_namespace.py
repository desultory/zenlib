from unittest import TestCase, main

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
    def test_user_namespace_exceptions(self):
        with self.assertRaises(TestPassedException):
            nsexec(test_exception)

    def test_user_namespace_func(self):
        self.assertEqual(nsexec(test_add_func, 1, 2), 3)

    def test_user_namespace_uid_gid(self):
        self.assertEqual(nsexec(test_uid_gid), (0, 0))

    def test_user_namespace_alt_uid_gid(self):
        self.assertEqual(nsexec(test_uid_gid, uid=9999, gid=9999), (9999, 9999))


if __name__ == "__main__":
    main()
