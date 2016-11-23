# -*- coding: utf-8 -*-
"""Parser Utils Module

This module defines a ParserUtils class with several static methods to be used
by parser implementations.

"""

from .schema_parser_exception import SchemaParserException


class ParserUtils(object):
    """ParserUtils

    The ParserUtils class exposes a number of static utility methods that are
    intended to be called from within parser implementations.

    """

    @staticmethod
    def get_required(obj, key):
        """Get a required value from the dict.

        Gets the value associated with key in the dict, or raises a
        SchemaParserException if it's not present.

        :param obj: A dict on json object
        :param key: The name of the property to retrieve

        :returns: The value if found

        :raises: A SchemaParserException if the key is not found

        """
        if key in obj.keys():
            return obj[key]
        else:
            raise SchemaParserException("Required field '{field}' missing in object".format(field=key))

    @staticmethod
    def get_required_string(obj, key):
        """Get a required string from the dict

        Gets the string value associated with the key in the dict, and raises a
        SchemaParserException if the key is not present or the value is not a
        string.

        :param obj: A dict on json object
        :param key: The name of the property to retrieve

        :returns: The value as a string if found

        :raises: A SchemaParserException if the key is not found, or the value is not a string

        """
        value = ParserUtils.get_required(obj, key)
        if isinstance(value, str):
            return value
        else:
            raise SchemaParserException("Required string '{field}' is not a string".format(field=key))

    @staticmethod
    def get_required_integer(obj, key):
        """Get a required integer from the dict

        Gets the integer value associated with the key in the dict, and raises a
        SchemaParserException if the key is not present or the value is not an
        integer.

        :param obj: A dict on json object
        :param key: The name of the property to retrieve

        :returns: The value as an integer if found

        :raises: A SchemaParserException if the key is not found, or the value is not an integer

        """
        value = ParserUtils.get_required(obj, key)
        if isinstance(value, int):
            return int(value)
        else:
            raise SchemaParserException("Required integer '{field}' is not an integer".format(field=key))

    @staticmethod
    def get_required_boolean(obj, key):
        """Get a required boolean from the dict

        Gets the boolean value associated with the key in the dict, and raises a
        SchemaParserException if the key is not present or the value is not an
        boolean.

        :param obj: A dict on json object
        :param key: The name of the property to retrieve

        :returns: The value as an boolean if found

        :raises: A SchemaParserException if the key is not found, or the value is not an boolean

        """
        value = ParserUtils.get_required(obj, key)
        if isinstance(value, bool):
            return value
        else:
            raise SchemaParserException("Required boolean '{field}' is not an boolean".format(field=key))

    @staticmethod
    def get_optional(obj, key):
        """Get an optional property from the dict

        Gets the optional value associated with the key in the dict, or returns
        None if the key is not found.

        :param obj: A dict on json object
        :param key: The name of the property to retrieve

        :returns: The value if found, otherwise returns None

        """
        if key in obj.keys():
            return obj[key]
        else:
            return None

    @staticmethod
    def get_optional_array(obj, key):
        """Get an optional property from the dict

        Gets the optional values associated with the key in the dict, or returns
        None if the key is not found.

        :param obj: A dict on json object
        :param key: The name of the property to retrieve

        :returns: An array of the values or None

        """
        options = []
        if key in obj.keys():
            for option in obj[key]:
                options.append(option)
            return options
        else:
            return None

    @staticmethod
    def get_optional_string(obj, key, default_value=None):
        """Get an optional string property from the dict

        Gets the optional string value associated with the key in the dict, or returns
        the default value if the key is not found.

        :param obj: A dict on json object
        :param key: The name of the property to retrieve
        :param default_value: Value to use if nothing to parse

        :returns: The value if found, otherwise returns default_value

        :raises: A SchemaParserException is raised if the value exists and is not a string

        """
        value = ParserUtils.get_optional(obj, key)
        if isinstance(value, str):
            return value
        elif value is None:
            return default_value
        else:
            raise SchemaParserException("Expected string '{field}' is not a string".format(field=key))

    @staticmethod
    def get_optional_integer(obj, key):
        """Get an optional integer property from the dict

        Gets the optional integer value associated with the key in the dict, or returns
        None if the key is not found.

        :param obj: A dict on json object
        :param key: The name of the property to retrieve

        :returns: The value if found cast to an integer, otherwise returns None

        :raises: A SchemeParserException is raised if the value is not an integer

        """
        value = ParserUtils.get_optional(obj, key)
        if value is not None:
            try:
                value = int(value)
                return value
            except ValueError:
                raise SchemaParserException("Expected integer '{field}' is not an integer".format(field=key))
        else:
            return None
