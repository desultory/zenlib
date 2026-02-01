from unittest import TestCase, main

from zenlib.types.validated_dataclass import validatedDataclass


@validatedDataclass
class testDataClass:
    a: int = 0
    b: str = ""


@validatedDataclass
class anotherDataClass:
    x: float = 0.0
    y: str = "default"


class TestValidatedDataclass(TestCase):
    def test_validated_dataclass(self):
        c = testDataClass()
        c.a = 1
        c.b = "test"
        self.assertTrue(hasattr(c, "logger"))

    def test_default_values(self):
        d = anotherDataClass()
        self.assertEqual(d.x, 0.0)
        self.assertEqual(d.y, "default")
        d.x = 3.14
        d.y = "hello"
        self.assertEqual(d.x, 3.14)
        self.assertEqual(d.y, "hello")

    def test_bad_type(self):
        c = testDataClass()
        d = anotherDataClass()

        with self.assertRaises(TypeError):
            c.a = "test"

        with self.assertRaises(TypeError):
            d.x = "not a float"


if __name__ == "__main__":
    main()
