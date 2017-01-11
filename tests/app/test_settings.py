import unittest

from app import settings


class TestSettings(unittest.TestCase):

    def test_ensure_min_returns_min(self):
        minimum = 1000
        value = 1
        self.assertEqual(minimum, settings.ensure_min(value, minimum))

    def test_ensure_min_returns_value(self):
        minimum = 1000
        value = 10000
        self.assertEqual(value, settings.ensure_min(value, minimum))

if __name__ == '__main__':
    unittest.main()
