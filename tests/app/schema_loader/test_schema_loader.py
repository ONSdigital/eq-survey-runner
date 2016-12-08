import unittest
import json

from app.schema_loader.schema_loader import load_schema, load_s3_schema_file, available_s3_schemas
from mock import patch, Mock
from app import settings

import botocore


class SchemaLoaderTest(unittest.TestCase):

    def setUp(self):
        self.original_bucket = settings.EQ_SCHEMA_BUCKET
        settings.EQ_SCHEMA_BUCKET = "test-test-test"

    def tearDown(self):
        settings.EQ_SCHEMA_BUCKET = self.original_bucket

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

    def test_available_s3_schemas(self):
        mocked_keys = [Mock(key='test_schema_1.json'), Mock(key='test_schema_2.json')]
        mocked_connection = Mock()
        with patch('boto3.resource', Mock(return_value=mocked_connection)):
            mocked_bucket = Mock()
            mocked_connection.Bucket = Mock(return_value=mocked_bucket)
            mocked_bucket.objects.all = Mock(return_value=mocked_keys)

            expected = ['test_schema_1.json', 'test_schema_2.json']

            self.assertEqual(expected, available_s3_schemas())

    def test_load_s3_schema(self):
        mocked_json = '{"survey": "some_survey"}'
        mocked_connection = Mock()
        with patch('boto3.resource', Mock(return_value=mocked_connection)):
            mocked_file = Mock()
            mocked_file.read = Mock(return_value=mocked_json.encode())
            mocked_object = Mock()
            mocked_connection.Object = Mock(return_value=mocked_object)
            mocked_object.get.return_value = {"Body": mocked_file}

            self.assertEqual(json.loads(mocked_json), load_s3_schema_file("ignored_filename.json"))

    def test_load_invalid_s3_schema(self):

        mocked_connection = Mock()
        with patch('boto3.resource', Mock(return_value=mocked_connection)) as mocked_resource:
            stubbed_error = {'Error': {'Code': '500', 'Message': "Couldn't find file"}}
            mocked_resource.side_effect = botocore.exceptions.ClientError(stubbed_error, "Some operation")

            self.assertIsNone(load_s3_schema_file("999999.json"))

if __name__ == '__main__':
    unittest.main()
