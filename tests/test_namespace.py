from os import environ
from unittest import TestCase, main, skipIf

from zenlib.namespace import nsexec


class TestPassedException(Exception):
    pass


def test_exception():
    raise TestPassedException("This is a test exception")


def test_add_func(a, b):
    return a + b


def test_add_kwargs(a, b, add1=None, add2=None):
    return add1 + add2


def test_uid_gid():
    import os

    return os.getuid(), os.getgid()


def test_cwd():
    from pathlib import Path

    return [p for p in Path("/").rglob("")]


class TestNamespace(TestCase):
    @skipIf(environ.get("CI") == "true", "Skipping test_namespace.py in CI")
    def test_user_namespace_exceptions(self):
        with self.assertRaises(TestPassedException):
            nsexec(test_exception)

    @skipIf(environ.get("CI") == "true", "Skipping test_namespace.py in CI")
    def test_user_namespace_func(self):
        self.assertEqual(nsexec(test_add_func, 1, 2), 3)

    @skipIf(environ.get("CI") == "true", "Skipping test_namespace.py in CI")
    def test_user_namespace_kwargs(self):
        self.assertEqual(nsexec(test_add_kwargs, 1, 2, add1=3, add2=4), 7)

    @skipIf(environ.get("CI") == "true", "Skipping test_namespace.py in CI")
    def test_user_namespace_uid_gid(self):
        self.assertEqual(nsexec(test_uid_gid), (0, 0))

    @skipIf(environ.get("CI") == "true", "Skipping test_namespace.py in CI")
    def test_user_namespace_chroot(self):
        from pathlib import Path
        from tempfile import TemporaryDirectory

        with TemporaryDirectory() as test_dir:  # It should be an empty root tree
            self.assertEqual(nsexec(test_cwd, target_root=test_dir), [Path("/")])


if __name__ == "__main__":
    main()
