from app.utilities.schema import load_schema_from_name
from tests.app.app_context_test_case import AppContextTestCase


class SchemaLoaderTest(AppContextTestCase):
    def test_load_schema_from_name(self):
        self.assertIsNotNone(load_schema_from_name('test_checkbox'))

    def test_load_schema_with_different_schema_name(self):
        self.assertIsNotNone(load_schema_from_name('test_dates'))

    def test_load_schema_with_invalid_schema_name(self):
        with self.assertRaises(FileNotFoundError):
            load_schema_from_name('test_0309')

    def test_load_schema_with_default_language_code(self):
        self.assertIsNotNone(load_schema_from_name('test_language'))

    def test_load_schema_with_passing_default_language_code(self):
        self.assertIsNotNone(load_schema_from_name('test_language', language_code='en'))

    def test_load_schema_with_language_code(self):
        self.assertIsNotNone(load_schema_from_name('test_language', language_code='cy'))
