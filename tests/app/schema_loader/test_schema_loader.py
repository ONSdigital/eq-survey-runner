import unittest
from app.schema_loader import schema_loader


class SchemaLoaderTest(unittest.TestCase):

    def test_load_schema(self):
        self.assertIsNotNone(schema_loader.load_schema("1", "0203"))

    def test_load_schema_with_different_form_type(self):
        self.assertIsNotNone(schema_loader.load_schema("1", "0205"))

    def test_load_schema_with_invalid_form_type(self):
        self.assertIsNone(schema_loader.load_schema("1", "0309"))

    def test_load_schema_with_invalid_eq_id(self):
        self.assertIsNone(schema_loader.load_schema("99", "0205"))

if __name__ == '__main__':
    unittest.main()
