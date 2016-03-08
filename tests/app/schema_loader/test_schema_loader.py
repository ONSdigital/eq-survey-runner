import unittest
from app.schema_loader import schema_loader


class SchemaLoaderTest(unittest.TestCase):

    def test_load_schema(self):
        self.assertIsNotNone(schema_loader.load_schema("1"))

if __name__ == '__main__':
    unittest.main()
