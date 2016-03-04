from verlib import NormalizedVersion
import importlib
from .schema_parser_exception import SchemaParserException

class SchemaParserFactory(object):
    DEFAULT_MODULE = "v0_1"

    @staticmethod
    def get_module_version(version):
        # map version numbers to directory names
        return {
            '0.0.1' : 'v0_1'
        }.get(str(version), SchemaParserFactory.DEFAULT_MODULE)

    @staticmethod
    def create_parser(schema):
        if "schema" in schema.keys():
            # get the schema version number
            schema_version = NormalizedVersion(schema['schema'])

            # get the correct module name for this version
            version_module = SchemaParserFactory.get_module_version(schema_version)

        else:
            version_module = SchemaParserFactory.DEFAULT_MODULE


        # Import the appropriate module and return an instance of the parser
        module_name = str("." + version_module + ".schema_parser")
        class_name = "SchemaParser"
        ParserClass = getattr(importlib.import_module(module_name), class_name)

        return ParserClass(schema)
