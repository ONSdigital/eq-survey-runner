from app.utilities.schema import load_schema_from_params
from tests.app.app_context_test_case import AppContextTestCase


class SchemaLoaderTest(AppContextTestCase):
    def test_load_schema_from_params(self):
        self.assertIsNotNone(load_schema_from_params('test', 'checkbox'))

    def test_load_schema_with_different_form_type(self):
        self.assertIsNotNone(load_schema_from_params('test', 'dates'))

    def test_load_schema_with_invalid_form_type(self):
        with self.assertRaises(FileNotFoundError):
            load_schema_from_params('test', '0309')

    def test_load_schema_with_invalid_eq_id(self):
        with self.assertRaises(FileNotFoundError):
            load_schema_from_params('99', 'checkbox')

    def test_load_schema_with_default_language_code(self):
        self.assertIsNotNone(load_schema_from_params('test', 'language'))

    def test_load_schema_with_passing_default_language_code(self):
        self.assertIsNotNone(load_schema_from_params('test', 'language', 'en'))

    def test_load_schema_with_language_code(self):
        self.assertIsNotNone(load_schema_from_params('test', 'language', 'cy'))
