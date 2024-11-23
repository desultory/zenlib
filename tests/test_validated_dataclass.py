from unittest import TestCase, main

from zenlib.types import validatedDataclass


@validatedDataclass
class testDataClass:
    a: int = None
    b: str = None


class TestValidatedDataclass(TestCase):
    def test_validated_dataclass(self):
        c = testDataClass()
        c.a = 1
        c.b = "test"
        self.assertTrue(hasattr(c, "logger"))

    def test_bad_type(self):
        c = testDataClass()
        with self.assertRaises(TypeError):
            c.a = "test"


if __name__ == "__main__":
    main()
