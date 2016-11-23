from app.parser.parser_utils import ParserUtils
from app.parser.schema_parser_exception import SchemaParserException
import unittest


class ParserUtilsTest(unittest.TestCase):
    def test_get_required(self):
        schema = {
            "property": 'tada!'
        }

        self.assertEqual(ParserUtils.get_required(schema, 'property'), 'tada!')

        with self.assertRaises(SchemaParserException):
            ParserUtils.get_required(schema, 'notfound')

    def test_get_required_string(self):
        schema = {
            "string": "value"
        }

        string = ParserUtils.get_required_string(schema, 'string')
        self.assertEqual(string, 'value')
        self.assertTrue(isinstance(string, str))

        with self.assertRaises(SchemaParserException):
            ParserUtils.get_required_string(schema, 'notfound')

    def test_get_required_integer(self):
        schema = {
            "integer": 5
        }

        integer = ParserUtils.get_required_integer(schema, 'integer')
        self.assertEqual(integer, 5)
        self.assertTrue(isinstance(integer, int))

        with self.assertRaises(SchemaParserException):
            ParserUtils.get_required_string(schema, 'notfound')

    def test_get_optional(self):
        schema = {
            "property": 'tada!'
        }

        self.assertEqual(ParserUtils.get_optional(schema, 'property'), 'tada!')
        notfound = ParserUtils.get_optional(schema, 'notfound')
        self.assertIsNone(notfound)

    def test_get_optional_string(self):
        schema = {
            "string": "value"
        }

        string = ParserUtils.get_optional_string(schema, 'string')
        self.assertEqual(string, 'value')
        self.assertTrue(isinstance(string, str))

        notfound = ParserUtils.get_optional_string(schema, 'notfound')
        self.assertIsNone(notfound)

    def test_get_optional_integer(self):
        schema = {
            "integer": 5
        }

        integer = ParserUtils.get_optional_integer(schema, 'integer')
        self.assertEqual(integer, 5)
        self.assertTrue(isinstance(integer, int))

        notfound = ParserUtils.get_optional_integer(schema, 'notfound')
        self.assertIsNone(notfound)
