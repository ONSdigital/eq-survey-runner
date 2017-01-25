
from json import load

import json
import logging
import os
import unittest

import jsonschema
from jsonschema import validate

from app import settings
from app.helpers.schema_helper import SchemaHelper
from app.schema_loader import schema_loader

logger = logging.getLogger(__name__)


class TestSchemaValidation(unittest.TestCase):

    def test_schema(self):

        errors = []

        files = schema_loader.available_schemas()

        schema_file = open(os.path.join(settings.EQ_SCHEMA_DIRECTORY, "schema/schema-v1.json"), encoding="utf8")
        schema = load(schema_file)

        for file in files:
            json_file = open(os.path.join(settings.EQ_SCHEMA_DIRECTORY, file), encoding="utf8")
            json_to_validate = json.load(json_file)

            errors.extend(self.validate_json_against_schema(file, json_to_validate, schema))
            errors.extend(self.validate_schema_contains_valid_routing_rules(file, json_to_validate))
            errors.extend(self.validate_routing_rules_has_default_if_not_all_answers_routed(file, json_to_validate))

        if errors:
            for error in errors:
                logger.error(error)

            self.fail("{} Schema Validation Errors.".format(len(errors)))

    def test_no_duplicate_ids_in_schema(self):
        schema_files = schema_loader.available_schemas()

        # Certain keys need to be ignored to avoid false positives.
        ignored_keys = ['routing_rules', 'skip_condition']

        for schema_file in schema_files:
            unique_id = []
            with open(os.path.join(settings.EQ_SCHEMA_DIRECTORY, schema_file), encoding="utf8") as file:
                schema_json = load(file)
                for id_value in self._parse_id_values(schema_json, ignored_keys):
                    if id_value in unique_id:
                        self.fail('Duplicate Id found. schema: %s, id: %s' % (schema_file, id_value))
                    else:
                        unique_id.append(id_value)

    def _parse_id_values(self, schema_json, ignored_keys):
        for k, v in schema_json.items():
            if k == 'id':
                yield v
            elif k in ignored_keys:
                continue
            elif isinstance(v, dict):
                yield from self._parse_id_values(v, ignored_keys)
            elif isinstance(v, list):
                for schema_item in v:
                    if isinstance(schema_item, dict):
                        yield from self._parse_id_values(schema_item, ignored_keys)


    @staticmethod
    def validate_json_against_schema(file, json_to_validate, schema):
        try:
            validate(json_to_validate, schema)
            return []
        except jsonschema.exceptions.ValidationError as e:
            return ["Schema Validation Error! File [{}] does not validate against schema. Error [{}]".format(file, e)]
        except Exception as e:
            return ["JSON Parse Error! Could not parse [{}]. Error [{}]".format(file, e)]

    @classmethod
    def validate_schema_contains_valid_routing_rules(cls, file, json_to_validate):

        errors = []

        blocks = [SchemaHelper.get_blocks(json_to_validate)]
        for block in blocks:
            if 'routing_rules' in block and len(block['routing_rules']) > 0:
                for rule in block['routing_rules']:
                    if 'goto' in rule and 'id' in rule['goto'].keys():
                        block_id = rule['goto']['id']
                        if block_id == 'summary':
                            continue

                        if not cls.contains_block(blocks, block_id):
                            invalid_block_error = "Routing rule routes to invalid block [{}]".format(block_id)
                            errors.append(TestSchemaValidation._error_message(invalid_block_error, file))

        return errors

    @staticmethod
    def validate_routing_rules_has_default_if_not_all_answers_routed(file, json_to_validate):

        errors = []

        for block in SchemaHelper.get_blocks(json_to_validate):
            for section in (s for s in block['sections'] if 'sections' in block):
                for question in (q for q in section['questions'] if 'questions' in section):
                    for answer in (a for a in question['answers'] if 'answers' in question):
                        errors.extend(TestSchemaValidation.validate_answer(file, block, answer))

        return errors

    @staticmethod
    def validate_answer(file, block, answer):
        answer_errors = []
        if 'routing_rules' in block and len(block['routing_rules']) > 0 and 'options' in answer:
            options = [option['value'] for option in answer['options']]
            has_default_route = False

            for rule in block['routing_rules']:
                if 'goto' in rule and 'when' in rule['goto'].keys():
                    when = rule['goto']['when']
                    if 'id' in when and when['id'] == answer['id'] and when['value'] in options:
                        options.remove(when['value'])
                else:
                    options = []
                    has_default_route = True

            has_unrouted_options = len(options) > 0 and len(options) != len(answer['options'])

            if answer['mandatory'] is False and not has_default_route:
                default_route_not_defined = "Default route not defined for optional question [{}]".format(answer['id'])
                answer_errors.append(TestSchemaValidation._error_message(default_route_not_defined, file))

            if has_unrouted_options:
                unrouted_error_template = "Routing rule not defined for all answers or default not defined for answer [{}] missing options {}"
                unrouted_error = unrouted_error_template.format(answer['id'], options)
                answer_errors.append(TestSchemaValidation._error_message(unrouted_error, file))
        return answer_errors

    @staticmethod
    def _error_message(message, file):
        prefix = "Schema Integrity Error. File[{}]".format(file)
        return "{} {}".format(prefix, message)

    @staticmethod
    def contains_block(blocks, block_id):
        matching_blocks = [b for b in blocks if b["id"] == block_id]
        return len(matching_blocks) == 1


if __name__ == '__main__':
    unittest.main()
