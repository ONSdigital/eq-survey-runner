import os
import pathlib
import unittest
from json import load

from jsonschema import SchemaError, ValidationError, validate, RefResolver
from structlog import configure
from structlog import getLogger
from structlog.dev import ConsoleRenderer
from structlog.stdlib import LoggerFactory

from app.helpers.schema_helper import SchemaHelper
from app.utilities.schema import get_schema_path, get_schema_definition_path
from app.forms.fields import MIN_NUMBER, MAX_NUMBER, MAX_DECIMAL_PLACES

logger = getLogger()

configure(logger_factory=LoggerFactory(), processors=[ConsoleRenderer()])


class TestSchemaValidation(unittest.TestCase):

    def test_invalid_schema_block(self):
        schema_file = open(get_schema_definition_path(), encoding="utf8")
        schema = load(schema_file)

        file = "test_invalid_routing_block.json"

        json_file = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), file), encoding="utf8")
        json_to_validate = load(json_file)

        errors = self.validate_schema(schema, file, json_to_validate)
        block_errors = [error for error in errors if "invalid block" in error]

        self.assertNotEqual(len(block_errors), 0, "This schema should fail with an invalid block")

    def test_invalid_schema_group(self):
        schema_file = open(get_schema_definition_path(), encoding="utf8")
        schema = load(schema_file)

        file = "test_invalid_routing_group.json"

        json_file = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), file), encoding="utf8")
        json_to_validate = load(json_file)

        errors = self.validate_schema(schema, file, json_to_validate)
        group_errors = [error for error in errors if "invalid group" in error]

        self.assertNotEqual(len(group_errors), 0, "This schema should fail with an invalid group")

    def test_schemas(self):

        errors = []

        files = self.all_schema_files()

        schema_file = open(get_schema_definition_path(), encoding="utf8")
        schema = load(schema_file)

        for file in files:
            with open(file, encoding="utf8") as json_file:
                json_to_validate = load(json_file)

                errors.extend(self.validate_schema(schema, file, json_to_validate))

        if errors:
            for error in errors:
                logger.error(error)

            self.fail("{} Schema Validation Errors.".format(len(errors)))

    def validate_schema(self, schema, file, json_to_validate):

        errors = []

        try:
            errors.extend(self.validate_json_against_schema(file, json_to_validate, schema))

            errors.extend(self.validate_schema_contains_valid_routing_rules(file, json_to_validate))

            errors.extend(self.validate_routing_rules_has_default_if_not_all_answers_routed(file, json_to_validate))

            errors.extend(self.validate_range_types_from_answers(file, json_to_validate))
        except SchemaError as e:
            errors.append("JSON Error! File [{}]. Error [{}]".format(file, e))

        return errors

    def test_no_duplicate_id_in_schema(self):
        # Certain keys need to be ignored to avoid false positives.
        ignored_keys = ['routing_rules', 'skip_conditions']
        self.find_duplicates(ignored_keys, 'id')

    def test_no_duplicate_alias_in_schema(self):
        # Certain keys need to be ignored to avoid false positives.
        ignored_keys = ['routing_rules', 'skip_conditions']
        self.find_duplicates(ignored_keys, 'alias')

    def find_duplicates(self, ignored_keys, special_key):
        schema_files = self.all_schema_files()
        for schema_file in schema_files:
            with open(schema_file, encoding="utf8") as file:
                schema_json = load(file)
                unique_items = []
                for value in self._parse_values(schema_json, ignored_keys, special_key):
                    if value in unique_items:
                        self.fail('Duplicate {} found. Schema: {}, value {}'.format(special_key, schema_file, value))
                    else:
                        unique_items.append(value)

    def test_all_schemas_contain_confirmation_page(self):
        schema_files = self.all_schema_files()

        for schema_file in schema_files:
            self.assertTrue(self.contains_confirmation_or_summary(schema_file),
                            msg='{file} does not have a confirmation or summary page'.format(file=schema_file))

    @staticmethod
    def contains_confirmation_or_summary(schema_file):
        with open(schema_file, encoding="utf8") as file:
            schema_json = load(file)
            blocks = SchemaHelper.get_blocks(schema_json)
            for block in blocks:
                if block['type'] in ["Summary", "Confirmation"]:
                    return True
        return False

    def test_child_answers_define_parent(self):
        for schema_file in self.all_schema_files():
            with open(schema_file, encoding="utf8") as file:
                schema_json = load(file)

                for block in SchemaHelper.get_blocks(schema_json):
                    answers_by_id = SchemaHelper.get_answers_by_id_for_block(block)

                    for answer_id, answer in answers_by_id.items():
                        if answer['type'] in ['Radio', 'Checkbox']:
                            child_answer_ids = (o['child_answer_id'] for o in answer['options'] if 'child_answer_id' in o)

                            for child_answer_id in child_answer_ids:
                                if child_answer_id not in answers_by_id:
                                    self.fail("Child answer with id '%s' does not exist in schema %s"
                                              % (child_answer_id, schema_file))
                                if 'parent_answer_id' not in answers_by_id[child_answer_id]:
                                    self.fail("Child answer '%s' does not define parent_answer_id '%s' in schema %s"
                                              % (child_answer_id, answer_id, schema_file))
                                if answers_by_id[child_answer_id]['parent_answer_id'] != answer_id:
                                    self.fail("Child answer '%s' defines incorrect parent_answer_id '%s' in schema %s: "
                                              "Should be '%s"
                                              % (child_answer_id, answers_by_id[child_answer_id]['parent_answer_id'],
                                                 schema_file, answer_id))

    @staticmethod
    def all_schema_files():
        schema_files = []
        for folder, _, files in os.walk(get_schema_path()):
            for filename in files:
                if filename.endswith(".json"):
                    schema_files.append(os.path.join(folder, filename))
        return schema_files

    def _parse_values(self, schema_json, ignored_keys, parsed_key):
        for key, value in schema_json.items():
            if key == parsed_key:
                yield value
            elif key in ignored_keys:
                continue
            elif isinstance(value, dict):
                yield from self._parse_values(value, ignored_keys, parsed_key)
            elif isinstance(value, list):
                for schema_item in value:
                    if isinstance(schema_item, dict):
                        yield from self._parse_values(schema_item, ignored_keys, parsed_key)

    @staticmethod
    def validate_json_against_schema(file, json_to_validate, schema):
        try:
            baseURI = pathlib.Path(os.path.abspath('data/schema/schema_v1.json')).as_uri()
            resolver = RefResolver(base_uri=baseURI, referrer=schema)
            validate(json_to_validate, schema, resolver=resolver)
            return []
        except ValidationError as e:
            return ["Schema Validation Error! File [{}] does not validate against schema. Error [{}]".format(file, e)]
        except SchemaError as e:
            return ["JSON Parse Error! Could not parse [{}]. Error [{}]".format(file, e)]

    @classmethod
    def validate_schema_contains_valid_routing_rules(cls, file, json_to_validate):

        errors = []

        blocks = SchemaHelper.get_blocks(json_to_validate)
        for block in blocks:
            if 'routing_rules' in block and len(block['routing_rules']) > 0:
                for rule in block['routing_rules']:
                    if 'goto' in rule and 'id' in rule['goto'].keys():
                        block_id = rule['goto']['id']
                        if block_id == 'summary':
                            continue

                        if not cls.contains_block(json_to_validate, block_id):
                            invalid_block_error = "Routing rule routes to invalid block [{}]".format(block_id)
                            errors.append(TestSchemaValidation._error_message(invalid_block_error, file))

                    if 'goto' in rule and 'group' in rule['goto'].keys():
                        group_id = rule['goto']['group']

                        if not cls.contains_group(json_to_validate, group_id):
                            invalid_group_error = "Routing rule routes to invalid group [{}]".format(group_id)
                            errors.append(TestSchemaValidation._error_message(invalid_group_error, file))

        return errors

    @staticmethod
    def validate_routing_rules_has_default_if_not_all_answers_routed(file, json_to_validate):

        errors = []

        for block in SchemaHelper.get_blocks(json_to_validate):
            for question in block.get('questions', []):
                for answer in question.get('answers', []):
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
        return "Schema Integrity Error. File[{}] {}".format(file, message)

    @staticmethod
    def contains_block(json, block_id):
        matching_blocks = [b for b in SchemaHelper.get_blocks(json) if b["id"] == block_id]
        return len(matching_blocks) == 1

    @staticmethod
    def contains_group(json, group_id):
        matching_groups = [g for g in SchemaHelper.get_groups(json) if g["id"] == group_id]
        return len(matching_groups) == 1

    @staticmethod
    def validate_range_types_from_answers(file, json_to_validate):
        errors = []

        for block in SchemaHelper.get_blocks(json_to_validate):
            for answer in SchemaHelper.get_answers_for_block(block):
                used_answers = []
                values = []
                answer_id = answer['id']
                answer_decimals = answer.get('decimal_places', 0)

                if answer.get('max_value') and 'value' in answer.get('max_value'):
                    values.append(answer['max_value']['value'])

                if answer.get('max_value') and 'answer_id' in answer.get('max_value'):
                    used_answers.append(answer['max_value']['answer_id'])

                if answer.get('min_value') and 'value' in answer.get('min_value'):
                    values.append(answer['min_value']['value'])

                if answer.get('min_value') and 'answer_id' in answer.get('min_value'):
                    used_answers.append(answer['min_value']['answer_id'])

                for value in values:
                    errors.extend(TestSchemaValidation.validate_range_value(value, file, answer_id, answer_decimals))

                for used_answer_id in used_answers:
                    errors.extend(TestSchemaValidation.validate_range_type(
                        file, json_to_validate, used_answer_id, answer_id, answer_decimals))

        return errors

    @staticmethod
    def validate_range_type(file, json_to_validate, used_answer_id, answer_id, answer_decimals):
        range_errors = []

        used_answer_exists = False
        for block in SchemaHelper.get_blocks(json_to_validate):
            for answer in SchemaHelper.get_answers_for_block(block):
                if answer.get('id') == used_answer_id:
                    used_answer_exists = True
                    used_answer_type = answer['type']
                    used_answer_decimals = int(answer.get('decimal_places', 0))

        if not used_answer_exists:
            error_message = "{} used for {} is not an answer id in schema".format(used_answer_id, answer_id)
            range_errors.append(TestSchemaValidation._error_message(error_message, file))
        elif used_answer_type not in ['Number', 'Currency', 'Percentage']:
            error_message = "{} is of type {} and therefore can not be passed to max/min values for {}"\
                .format(used_answer_id, used_answer_type, answer_id)
            range_errors.append(TestSchemaValidation._error_message(error_message, file))
        elif used_answer_decimals > answer_decimals:
            if answer_decimals == 0:
                error_message = "{} of type decimal is being passed to " \
                                "max/min value for {} of type integer".format(used_answer_id, answer_id)
            else:
                error_message = "{} is of type decimal with {} places is being passed to" \
                                " max/min value for {} of {} decimal_places"\
                    .format(used_answer_id, used_answer_decimals, answer_id, answer_decimals)

            range_errors.append(TestSchemaValidation._error_message(error_message, file))

        return range_errors

    @staticmethod
    def validate_range_value(value, file, answer_id, answer_decimals):
        error_message = "Decimal Places used in {} should be less than or equal to {}, currently {}" \
            .format(answer_id, MAX_DECIMAL_PLACES, answer_decimals)

        if answer_decimals > MAX_DECIMAL_PLACES:
            return [TestSchemaValidation._error_message(error_message, file)]

        error_message = "Value {} used in {} should be between system limits {} to {}"\
            .format(value, answer_id, MIN_NUMBER, MAX_NUMBER)

        if MIN_NUMBER <= value <= MAX_NUMBER:
            return []
        else:
            return [TestSchemaValidation._error_message(error_message, file)]

if __name__ == '__main__':
    unittest.main()
