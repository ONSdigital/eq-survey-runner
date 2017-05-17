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

    def test_get_application_version_from_file(self):
        self.assertIsNotNone(settings.read_file('.application-version'))

    def test_missing_get_application_version_from_file(self):
        self.assertEqual(None, settings.read_file('.missing-application-version'))

    def test_none_filename_does_not_attempt_to_load_file(self):
        self.assertEqual(None, settings.read_file(None))

if __name__ == '__main__':
    unittest.main()
