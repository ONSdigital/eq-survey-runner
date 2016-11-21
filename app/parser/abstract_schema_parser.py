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

    """Get the version of the schema parser

    :returns: The version number for the parser

    """
    @abstractmethod
    def get_parser_version(self):
        raise NotImplementedError()

    @abstractmethod
    def parse(self):
        """Parse the schema and return an object schema, the root of which will be a
        Questionnaire object

        :returns: Questionnaire object
        """
        raise NotImplementedError()
