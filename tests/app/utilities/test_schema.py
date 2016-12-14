from app.utilities.schema import get_schema
import unittest


class TestSchema(unittest.TestCase):

    def test_get_schema_raises_exception_when_no_schema_found(self):
        metadata = {
            "eq_id": "123",
            "form_type": "456"
        }

        with self.assertRaises(ValueError) as context:
            get_schema(metadata)

        self.assertTrue('No schema available' in context.exception.args)
