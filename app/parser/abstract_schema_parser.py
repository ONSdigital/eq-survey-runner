# -*- coding: utf-8 -*-
"""Abstract Schema Parser Module

This module defines the AbstractSchemaParser class which defines the public
interface for all SchemaParsers.

There is a single constructor which accepts a json object reperesenting the
schema.  SchemeParsers are instantiated by a SchemaParserFactory.

The main method of the SchemaParser is parse() which accepts no parameters, but
returns an object of type Questionnaire, or raises a SchemaParserException.

"""
from abc import ABCMeta, abstractmethod


class AbstractSchemaParser(metaclass=ABCMeta):
    """
    Instantiates a parser with the Schema

    :param schema: The schema to parse
    """
    @abstractmethod
    def __init__(self, schema):
        raise NotImplementedError()

    """Get the version of the schema parser

    :returns: The version number for the parser

    """
    @abstractmethod
    def get_parser_version(self):
        raise NotImplementedError()

    """Parse the schema and return an object model, the root of which will be a
    Questionnaire object

    :returns: Questionnaire object

    """
    @abstractmethod
    def parse(self):
        raise NotImplementedError()
