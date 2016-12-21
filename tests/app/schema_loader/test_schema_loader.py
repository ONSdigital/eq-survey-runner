import unittest

from app.schema_loader.schema_loader import load_schema


class SchemaLoaderTest(unittest.TestCase):

    def test_load_schema(self):
        self.assertIsNotNone(load_schema("1", "0203"))

    def test_load_schema_with_different_form_type(self):
        self.assertIsNotNone(load_schema("1", "0205"))

    def test_load_schema_with_invalid_form_type(self):
        self.assertIsNone(load_schema("1", "0309"))

    def test_load_schema_with_invalid_eq_id(self):
        self.assertIsNone(load_schema("99", "0205"))

    def test_load_schema_with_default_language_code(self):
        self.assertIsNotNone(load_schema("test", "language"))

    def test_load_schema_with_passing_default_language_code(self):
        self.assertIsNotNone(load_schema("test", "language", "en"))

    def test_load_schema_with_language_code(self):
        self.assertIsNotNone(load_schema("test", "language", "cy"))
