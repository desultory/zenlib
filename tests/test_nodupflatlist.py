from unittest import TestCase, main

from zenlib.types import NoDupFlatList


class TestNoDupFlatList(TestCase):
    def test_util_import(self):
        from zenlib.util import NoDupFlatList as NDFL
        self.assertEqual(NoDupFlatList, NDFL)

    def test_dedup1(self):
        test_list = NoDupFlatList(no_warn=True)
        test_list += 1
        test_list.append(2)
        test_list.append(1)
        test_list.append(3)
        test_list += 2
        self.assertEqual(test_list, [1, 2, 3])

    def test_dedup2(self):
        test_list = NoDupFlatList(no_warn=True)
        test_list.append(3)
        test_list += 1
        test_list.append(2)
        test_list.append(1)
        test_list += 3
        test_list.append(2)
        self.assertEqual(test_list, [3, 1, 2])

    def test_flattening(self):
        test_list = NoDupFlatList(no_warn=True)
        test_list.append([1, 2, 3])
        test_list += [4, 5, 6]
        self.assertEqual(test_list, [1, 2, 3, 4, 5, 6])

    def test_deep_flattening(self):
        test_list = NoDupFlatList(no_warn=True)
        test_list.append([1, 2, 3, [4, 5, 6]])
        test_list += [7, 8, 9]
        self.assertEqual(test_list, [1, 2, 3, 4, 5, 6, 7, 8, 9])

    def test_flatening_and_dedup(self):
        test_list = NoDupFlatList(no_warn=True)
        test_list.append([1, 2, 3, [4, 5, 6]])
        test_list += [7, 8, 9]
        test_list.append([1, 2, 3, [4, 5, 6]])
        test_list += [1, [2, 3], 4, [7, [8, 9]], 6]
        self.assertEqual(test_list, [1, 2, 3, 4, 5, 6, 7, 8, 9])


if __name__ == "__main__":
    main()
