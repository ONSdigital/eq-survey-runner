from app.parser.schema_parser_exception import SchemaParserException

from app.parser.v0_0_1.schema_parser import SchemaParser

from verlib import NormalizedVersion


class SchemaParserFactory(object):

    @staticmethod
    def create_parser(schema):
        """Create a parser for the given survey schema

        Examines the given schema for a version number and then creates and
        returns a parser suitable for that schema version.

        :param schema: JSON object or dict containing the schema version

        :returns: An implementation of SchemaParser

        :raises: A SchemaParserException is raised if an appropriate parser cannot be instantiated

        """

        # get the schema version number
        schema_version = str(NormalizedVersion(schema['schema_version']))

        if schema_version == '0.0.1':
            return SchemaParser(schema)

        raise SchemaParserException('Could not create parser for version: ' + schema_version)
