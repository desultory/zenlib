from unittest import TestCase, main

from zenlib.util import pretty_print


class TestPrettyPrint(TestCase):
    def test_pretty_print_str(self):
        self.assertEqual(pretty_print("hello"), "hello\n")

    def test_pretty_print_int(self):
        self.assertEqual(pretty_print(42), "42\n")

    def test_pretty_print_tuple(self):
        self.assertEqual(pretty_print((1, 2, 3)), "+ 1\n+ 2\n+ 3\n")

    def test_pretty_print_list(self):
        self.assertEqual(pretty_print([1, 2, 3]), "- 1\n- 2\n- 3\n")

    def test_pretty_print_set(self):
        self.assertEqual(pretty_print({1, 2, 3}), "+ 1\n+ 2\n+ 3\n")

    def test_pretty_print_dict(self):
        self.assertEqual(pretty_print({1: 2, 3: 4}), "1: 2\n3: 4\n")

    def test_pretty_print_nested_dict(self):
        self.assertEqual(pretty_print({1: {"a": "asdf"}, 4: {"b": "1234"}}), "1:\n  a: asdf\n4:\n  b: 1234\n")

    def test_pretty_print_nested_list(self):
        self.assertEqual(pretty_print([1, [2, 3], 4]), "- 1\n- 2\n- 3\n- 4\n")

    def test_pretty_print_nested_list_in_dict(self):
        self.assertEqual(pretty_print({1: [2, 3], 4: [5, 6]}), "1:\n  - 2\n  - 3\n4:\n  - 5\n  - 6\n")

    def test_pretty_print_indent(self):
        self.assertEqual(pretty_print([1, [2, 3], 4], indent=2), "  - 1\n  - 2\n  - 3\n  - 4\n")


if __name__ == "__main__":
    main()
