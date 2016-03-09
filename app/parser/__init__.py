"""The Parser Module

This module is responsible for converting a survey schema json object into a
questionnaire object tree.

The primary interface to this module is the SchemaParserFactory which exposes a
static method called create_parser(schema) which examines the schema given and
returns an instance of SchemaParser appropriate for the schema version.

If a SchemaParser cannot be instantiated for the version, then a
SchemaParserException is raised.
"""
