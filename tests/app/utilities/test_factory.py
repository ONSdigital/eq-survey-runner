import unittest

from app.utilities.factory import Factory


class TestClassA(object):
    pass


class TestClassB(object):
    pass


class TestFactory(unittest.TestCase):

    def test_register(self):
        factory = Factory()
        factory.register("test", TestClassA)

        self.assertIsInstance(factory.create("test"), TestClassA)

    def test_register_all(self):
        factory = Factory()

        classes = {
            "test-a": TestClassA,
            "test-b": TestClassB
        }

        factory.register_all(classes)

        self.assertIsInstance(factory.create("test-a"), TestClassA)
        self.assertIsInstance(factory.create("test-b"), TestClassB)

if __name__ == '__main__':
    unittest.main()
