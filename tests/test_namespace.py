from platform import system
from getpass import getuser
from sys import version_info
from unittest import TestCase, main, skipIf

from zenlib.namespace import nsexec


def check_test_compat():
    """Checks if tests are compatible with the current environment"""
    if system() != "Linux":
        return

    if version_info < (3, 12):
        return

    user = getuser()

    with open("/etc/subuid", "r") as f:
        for subuid_line in f:
            if subuid_line.startswith(f"{user}:"):
                break
        else:
            return

    with open("/etc/subgid", "r") as f:
        for subgid_line in f:
            if subgid_line.startswith(f"{user}:"):
                break
        else:
            return


    return True


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

    return [p.resolve() for p in Path("/").rglob("")]


@skipIf(not check_test_compat(), "Skipping test_namespace.py in CI")
class TestNamespace(TestCase):
    def test_user_namespace_exceptions(self):
        with self.assertRaises(TestPassedException):
            nsexec(test_exception)

    def test_user_namespace_func(self):
        self.assertEqual(nsexec(test_add_func, 1, 2), 3)

    def test_user_namespace_kwargs(self):
        self.assertEqual(nsexec(test_add_kwargs, 1, 2, add1=3, add2=4), 7)

    def test_user_namespace_uid_gid(self):
        self.assertEqual(nsexec(test_uid_gid), (0, 0))

    def test_user_namespace_chroot(self):
        from pathlib import Path
        from tempfile import TemporaryDirectory

        with TemporaryDirectory() as test_dir:  # It should be an empty root tree
            self.assertEqual(nsexec(test_cwd, target_root=test_dir), [Path("/")])


if __name__ == "__main__":
    main()
