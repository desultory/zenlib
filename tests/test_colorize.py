from unittest import TestCase, main

from zenlib.util import colorize


class TestColorize(TestCase):
    def test_red(self):
        self.assertEqual(colorize("test", "red"), "\033[31mtest\033[0m")
        self.assertEqual(colorize("test2", "RED", bold=True), "\033[31;1mtest2\033[0m")
        self.assertEqual(colorize("test3", "ReD", bright=True), "\033[91mtest3\033[0m")
        self.assertEqual(colorize("test4", "REd", bold=True, bright=True), "\033[91;1mtest4\033[0m")

    def test_green(self):
        self.assertEqual(colorize("test", "green"), "\033[32mtest\033[0m")
        self.assertEqual(colorize("test2", "GREEN", bold=True), "\033[32;1mtest2\033[0m")
        self.assertEqual(colorize("test3", "GrEeN", bright=True), "\033[92mtest3\033[0m")
        self.assertEqual(colorize("test4", "GREeN", bold=True, bright=True), "\033[92;1mtest4\033[0m")

    def test_yellow(self):
        self.assertEqual(colorize("test", "yellow"), "\033[33mtest\033[0m")
        self.assertEqual(colorize("test2", "YELLOW", bold=True), "\033[33;1mtest2\033[0m")
        self.assertEqual(colorize("test3", "YeLLoW", bright=True), "\033[93mtest3\033[0m")
        self.assertEqual(colorize("test4", "YELLOw", bold=True, bright=True), "\033[93;1mtest4\033[0m")

    def test_blue(self):
        self.assertEqual(colorize("test", "blue"), "\033[34mtest\033[0m")
        self.assertEqual(colorize("test2", "BLUE", bold=True), "\033[34;1mtest2\033[0m")
        self.assertEqual(colorize("test3", "BlUE", bright=True), "\033[94mtest3\033[0m")
        self.assertEqual(colorize("test4", "BLUe", bold=True, bright=True), "\033[94;1mtest4\033[0m")

    def test_magenta(self):
        self.assertEqual(colorize("test", "magenta"), "\033[35mtest\033[0m")
        self.assertEqual(colorize("test2", "MAGENTA", bold=True), "\033[35;1mtest2\033[0m")
        self.assertEqual(colorize("test3", "MaGeNTa", bright=True), "\033[95mtest3\033[0m")
        self.assertEqual(colorize("test4", "MAGeNTa", bold=True, bright=True), "\033[95;1mtest4\033[0m")

    def test_cyan(self):
        self.assertEqual(colorize("test", "cyan"), "\033[36mtest\033[0m")
        self.assertEqual(colorize("test2", "CYAN", bold=True), "\033[36;1mtest2\033[0m")
        self.assertEqual(colorize("test3", "CyAN", bright=True), "\033[96mtest3\033[0m")
        self.assertEqual(colorize("test4", "CYAn", bold=True, bright=True), "\033[96;1mtest4\033[0m")

    def test_white(self):
        self.assertEqual(colorize("test", "white"), "\033[37mtest\033[0m")
        self.assertEqual(colorize("test2", "WHITE", bold=True), "\033[37;1mtest2\033[0m")
        self.assertEqual(colorize("test3", "WhITE", bright=True), "\033[97mtest3\033[0m")
        self.assertEqual(colorize("test4", bold=True, bright=True), "\033[97;1mtest4\033[0m")


    def test_invalid_color(self):
        with self.assertRaises(ValueError):
            colorize("test", "invalid_color")


if __name__ == "__main__":
    main()
