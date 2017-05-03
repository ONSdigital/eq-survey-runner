import unittest

from app import settings
from app.missing_setting_exception import MissingSettingException


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

    def test_invalid_key_raises_exception(self):
        with self.assertRaises(MissingSettingException) as exception:
            settings.get_env_or_fail("MISSING_ENVIRONMENT_VARIABLE")

        self.assertEqual("Setting 'MISSING_ENVIRONMENT_VARIABLE' Missing", exception.exception.value)

if __name__ == '__main__':
    unittest.main()
