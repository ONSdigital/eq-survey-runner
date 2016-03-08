from verlib import NormalizedVersion
import importlib
from app.parser.schema_parser_exception import SchemaParserException


class SchemaParserFactory(object):
    DEFAULT_MODULE = "UNKNOWN"

    @staticmethod
    def get_module_version(version):
        '''Map a version string to a python module
        '''
        return {
            '0.0.1': 'v0_0_1'
        }.get(str(version), SchemaParserFactory.DEFAULT_MODULE)

    @staticmethod
    def create_parser(schema):
        '''Create a parser for the given survey schema

        Examines the given schema for a version number and then creates and
        returns a parser suitable for that schema version.

        Args:
            schema: JSON object or dict containing the schema version

        Raises:
            A SchemaParserException is raised if an appropriate parser cannot
            be instantiated

        '''
        try:
            if "schema_version" in schema.keys():
                # get the schema version number
                schema_version = NormalizedVersion(schema['schema_version'])

                # get the correct module name for this version
                version_module = SchemaParserFactory.get_module_version(schema_version)

            else:
                version_module = SchemaParserFactory.DEFAULT_MODULE

            # Import the appropriate module and return an instance of the parser
            module_name = str("app.parser." + version_module + ".schema_parser")
            class_name = "SchemaParser"
            ParserClass = getattr(importlib.import_module(module_name), class_name)

            return ParserClass(schema)
        except:
            raise SchemaParserException('Could not create parser for version: ' + version_module)
