from app.parser.parser_utils import ParserUtils
from app.parser.schema_parser_exception import SchemaParserException
import unittest


class ParserUtilsTest(unittest.TestCase):
    def test_get_required(self):
        schema = {
            "property": 'tada!'
        }

        try:
            self.assertEqual(ParserUtils.get_required(schema, 'property'), 'tada!')
        except:
            self.fail('An unexpected exception was thrown')

        with self.assertRaises(SchemaParserException) as spe:
            notfound = ParserUtils.get_required(schema, 'notfound')

    def test_get_required_string(self):
        schema = {
            "string": "value"
        }

        try:
            string = ParserUtils.get_required_string(schema, 'string')
            self.assertEqual(string, 'value')
            self.assertTrue(isinstance(string, str))
        except:
            self.fail('An unexpected exception was raised')

        with self.assertRaises(SchemaParserException) as spe:
            notfound = ParserUtils.get_required_string(schema, 'notfound')

    def test_get_required_integer(self):
        schema = {
            "integer": 5
        }

        try:
            integer = ParserUtils.get_required_integer(schema, 'integer')
            self.assertEqual(integer, 5)
            self.assertTrue(isinstance(integer, int))
        except:
            self.fail('An unexpected exception was raised')

        with self.assertRaises(SchemaParserException) as spe:
            notfound = ParserUtils.get_required_string(schema, 'notfound')

    def test_get_optional(self):
        schema = {
            "property": 'tada!'
        }

        try:
            self.assertEqual(ParserUtils.get_optional(schema, 'property'), 'tada!')
        except:
            self.fail('An unexpected exception was thrown')

        try:
            notfound = ParserUtils.get_optional(schema, 'notfound')
            self.assertIsNone(notfound)
        except:
            self.fail('An unexpected exception was thrown')

    def test_get_optional_string(self):
        schema = {
            "string": "value"
        }

        try:
            string = ParserUtils.get_optional_string(schema, 'string')
            self.assertEqual(string, 'value')
            self.assertTrue(isinstance(string, str))
        except:
            self.fail('An unexpected exception was raised')

        try:
            notfound = ParserUtils.get_optional_string(schema, 'notfound')
            self.assertIsNone(notfound)
        except:
            self.fail('An unexpected exception was thrown')

    def test_get_optional_integer(self):
        schema = {
            "integer": 5
        }
        try:
            integer = ParserUtils.get_optional_integer(schema, 'integer')
            self.assertEqual(integer, 5)
            self.assertTrue(isinstance(integer, int))
        except:
            self.fail('An unexpected exception was raised')

        try:
            notfound = ParserUtils.get_optional_integer(schema, 'notfound')
            self.assertIsNone(notfound)
        except:
            self.fail('An unexpected exception was thrown')
