from app.parser.schema_parser_factory import SchemaParserFactory
from app.parser.schema_parser_exception import SchemaParserException
import unittest


class SchemaParserFactoryTest(unittest.TestCase):

    def test_schema_parser_factory(self):
        schema = {
            "schema_version": "0.0.1"
        }

        parser = SchemaParserFactory.create_parser(schema)
        self.assertEqual(parser.get_parser_version(), '0.0.1', "The parser and schema version numbers did not match")

    def test_invalid_schema_version(self):
        schema = {
            "schema_version": '0.0.0'   # invalid schema version
        }

        try:
            SchemaParserFactory.create_parser(schema)
            self.fail('Tried to instantiate a parser for an invalid schema version')
        except SchemaParserException:
            assert True
