from unittest import TestCase, main
from collections import UserDict
from pathlib import Path

from zenlib.util import contains, unset
from zenlib.logging import loggify


TEST_DICT = {'a': [1, 2, 3],
             'b': 123,
             'c': '123',
             'd': {'aa': 1, 'bb': 2},
             'e': None,
             'p': Path(),
             'q': Path('test')}


@loggify
class TestDict(UserDict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data = TEST_DICT

    @contains('a')
    def _contains_a(self):
        return True

    @contains('e')
    def _contains_e(self):
        assert False, 'This check should not pass'

    @contains('e', is_set=False)
    def _contains_e_unset(self):
        return True

    @contains('p')
    def _contains_p(self):
        assert False, 'This check should not pass'

    @contains('p', is_set=False)
    def _contains_p_unset(self):
        return True

    @contains('q')
    def _contains_q(self):
        return True

    @contains('z')
    def _contains_z(self):
        assert False, 'This check should not pass'

    @unset('a')
    def _unset_a(self):
        assert False, 'This check should not pass'

    @unset('a', raise_exception=True)
    def _unset_a_exception(self):
        assert False, 'This check should not pass'

    @unset('e')
    def _unset_e(self):
        return True

    @unset('z')
    def _unset_z(self):
        return True


class TestDictCheck(TestCase):
    def test_contains(self):
        test_dict = TestDict()
        self.assertTrue(test_dict._contains_a())
        self.assertFalse(test_dict._contains_e())
        self.assertTrue(test_dict._contains_e_unset())
        self.assertFalse(test_dict._contains_p())
        self.assertTrue(test_dict._contains_p_unset())
        self.assertTrue(test_dict._contains_q())
        self.assertFalse(test_dict._contains_z())

    def test_unset(self):
        test_dict = TestDict()
        self.assertFalse(test_dict._unset_a())
        with self.assertRaises(ValueError):
            test_dict._unset_a_exception()
        self.assertTrue(test_dict._unset_z())
        self.assertTrue(test_dict._unset_e())


if __name__ == '__main__':
    main()

