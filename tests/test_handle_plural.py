from unittest import TestCase, main

from zenlib.util import handle_plural


class TestHandlePlural(TestCase):
    @handle_plural
    def _test_plural_ints(self, arg_a, iterated):
        if isinstance(iterated, int):
            self._test_data += iterated
        return iterated

    @handle_plural
    def _test_plural_ints_with_kwarg(self, arg_a, iterated, test_kwarg='asdf'):
        self.assertEqual(test_kwarg, 'asdf')
        if isinstance(iterated, int):
            self._test_data += iterated
        return iterated

    @handle_plural
    def _test_plural_setting_kwarg(self, arg_a, iterated, test_kwarg='asdf'):
        self.assertEqual(test_kwarg, 'test')
        if isinstance(iterated, int):
            self._test_data += iterated
        return iterated

    def test_list(self):
        self._test_data = 0
        test_list = [1, 2, 3, 4]
        extra_arg = 'a'
        self.assertEqual(self._test_plural_ints(extra_arg, test_list), None)
        self.assertEqual(self._test_data, sum(test_list))
        self._test_data = 0
        self.assertEqual(self._test_plural_ints_with_kwarg(extra_arg, test_list), None)
        self.assertEqual(self._test_data, sum(test_list))

    def test_set(self):
        self._test_data = 0
        test_set = {1, 2, 3, 4}
        extra_arg = 'a'
        self.assertEqual(self._test_plural_ints(extra_arg, test_set), None)
        self.assertEqual(self._test_data, sum(test_set))
        self._test_data = 0
        self.assertEqual(self._test_plural_ints_with_kwarg(extra_arg, test_set), None)
        self.assertEqual(self._test_data, sum(test_set))

    def test_setting_kwarg(self):
        self._test_data = 0
        test_list = [1, 2, 3, 4]
        extra_arg = 'a'
        self.assertEqual(self._test_plural_setting_kwarg(extra_arg, test_list, test_kwarg='test'), None)
        self.assertEqual(self._test_data, sum(test_list))

    def test_single(self):  # non-iterables should allow returns
        self._test_data = 0
        test_arg = 1
        extra_arg = 'a'
        self.assertEqual(self._test_plural_ints(extra_arg, test_arg), test_arg)

    def test_string(self):
        self._test_data = 0
        test_arg = 'abcd'
        extra_arg = 'z'
        self.assertEqual(self._test_plural_ints(extra_arg, test_arg), test_arg)

    def test_dict_keys(self):
        self._test_data = 0
        test_arg = {'a': 1, 'b': 2, 'c': 3}
        self.assertEqual(self._test_plural_ints(test_arg), None)
        self.assertEqual(self._test_data, sum(test_arg.values()))

    @handle_plural
    def _test_plural_dict(self, key, value):
        self._test_data[key] = value

    def test_dict_unrolling(self):
        self._test_data = {}
        test_arg = {'a': 1, 'b': 2, 'c': 3}
        self._test_plural_dict(test_arg)
        self.assertEqual(self._test_data, test_arg)


if __name__ == '__main__':
    main()

