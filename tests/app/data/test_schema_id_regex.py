import os
import unittest

from json import load

from jsonschema import ValidationError, validate

from app import settings
from app.utilities.schema import get_schema_file_path


def create_schema_with_id(schema_id='answer'):
    """
    Utility method that loads a JSON schema file and swaps out an answer Id.
    :param schema_id: The Id to use for the answer.
    :return: The JSON file with the Id swapped for schema_id
    """
    json_file = open(get_schema_file_path("test_percentage.json"))
    json_content = load(json_file)
    json_content['groups'][0]['blocks'][0]['sections'][0]['questions'][0]['answers'][0]['id'] = schema_id
    return json_content


def validate_json_against_schema(json_to_validate, schema):
    try:
        validate(json_to_validate, schema)
        return []
    except ValidationError as e:
        return ["Schema Validation Error! JSON [{}] does not validate against schema. Error [{}]"
                .format(json_to_validate, e)]


class TestSchemaIdRegEx(unittest.TestCase):

    def setUp(self):
        schema_file = open(os.path.join(settings.EQ_SCHEMA_DIRECTORY, "schema/schema_v1.json"), encoding="utf8")
        self.errors = []
        self.schema = load(schema_file)

    def test_default_id_should_pass_validation(self):
        # Given
        json_to_validate = create_schema_with_id()

        # When
        errors = validate_json_against_schema(json_to_validate, self.schema)

        # Then
        self.assertEqual(len(errors), 0)

    def test_guid_should_pass_validation(self):
        # Given
        json_to_validate = create_schema_with_id('star-wars')

        # When
        errors = validate_json_against_schema(json_to_validate, self.schema)

        # Then
        self.assertEqual(len(errors), 0)

    def test_id_with_hyphenated_names_should_pass_validation(self):
        # Given
        json_to_validate = create_schema_with_id('name-with-hyphens')

        # When
        errors = validate_json_against_schema(json_to_validate, self.schema)

        # Then
        self.assertEqual(len(errors), 0)

    def test_id_with_numeric_should_pass_validation(self):
        # Given
        json_to_validate = create_schema_with_id('this-is-a-valid-id-0')

        # When
        errors = validate_json_against_schema(json_to_validate, self.schema)

        # Then
        self.assertEqual(len(errors), 0)

    def test_id_with_numeric_at_start_should_pass_validation(self):
        # Given
        json_to_validate = create_schema_with_id('0-this-is-a-valid-id-0')

        # When
        errors = validate_json_against_schema(json_to_validate, self.schema)

        # Then
        self.assertEqual(len(errors), 0)

    def test_id_with_punctuation_should_fail_validation(self):
        # Given
        json_to_validate = create_schema_with_id('!n0t-@-valid-id')

        # When
        errors = validate_json_against_schema(json_to_validate, self.schema)

        # Then
        self.assertEqual(len(errors), 1)

    def test_id_with_spaces_should_fail_validation(self):
        # Given
        json_to_validate = create_schema_with_id('not a valid id')

        # When
        errors = validate_json_against_schema(json_to_validate, self.schema)

        # Then
        self.assertEqual(len(errors), 1)

    def test_id_with_capital_letters_should_fail_validation(self):
        # Given
        json_to_validate = create_schema_with_id('NOT-A-VALID-ID')

        # When
        errors = validate_json_against_schema(json_to_validate, self.schema)

        # Then
        self.assertEqual(len(errors), 1)

    def test_id_with_underscores_should_pass_validation(self):
        # Given
        json_to_validate = create_schema_with_id('not_a_valid_id')

        # When
        errors = validate_json_against_schema(json_to_validate, self.schema)

        # Then
        self.assertEqual(len(errors), 1)
