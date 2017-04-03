from app.utilities.schema import load_schema_from_metadata

from tests.app.app_context_test_case import AppContextTestCase


class TestSchema(AppContextTestCase):

    def test_load_schema_from_metadata_raises_exception_when_no_schema_found(self):
        metadata = {
            "eq_id": "123",
            "form_type": "456"
        }

        with self.assertRaises(FileNotFoundError):
            load_schema_from_metadata(metadata)
