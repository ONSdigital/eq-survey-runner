from json import JSONDecodeError

from app.schema_loader import schema_loader
import json
import jsonschema
import logging
import unittest
import os

from app import settings

from jsonschema import validate

logger = logging.getLogger(__name__)


class TestSchemaValidation(unittest.TestCase):

    def test_schema(self):

        errors = []

        files = schema_loader.available_local_schemas()

        schema_file = open(os.path.join(settings.EQ_SCHEMA_DIRECTORY, "schema/schema-v1.json"), encoding="utf8")
        schema = json.load(schema_file)

        for file in files:

            json_file = open(os.path.join(settings.EQ_SCHEMA_DIRECTORY, file), encoding="utf8")

            error = self.validate_json_against_schema(file, json_file, schema)

            if error:
                errors.append(error)

        if errors:
            for error in errors:
                logger.error(error)

            self.fail("{} Schema Validation Errors.".format(len(errors)))

    @staticmethod
    def validate_json_against_schema(file, json_file, schema):
        try:
            json_to_validate = json.load(json_file)
            validate(json_to_validate, schema)
        except jsonschema.exceptions.ValidationError as e:
            return "Schema Validation Error! File [{}] does not validate against schema. Error [{}]".format(file, e)
        except JSONDecodeError as e:
            return "JSON Parse Error! Could not parse [{}]. Error [{}]".format(file, e)


if __name__ == '__main__':
    unittest.main()
