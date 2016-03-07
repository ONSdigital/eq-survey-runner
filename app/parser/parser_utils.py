from .schema_parser_exception import SchemaParserException


class ParserUtils(object):
    # gets the value associated with key in the dict, or throws an exception if it's not present
    @staticmethod
    def get_required(obj, key):
        if key in obj.keys():
            return obj[key]
        else:
            raise SchemaParserException("Required field '{field}' missing in object".format(field=key))

    # gets the required string, and throws an exception if not present or not a string
    @staticmethod
    def get_required_string(obj, key):
        value = ParserUtils.get_required(obj, key)
        if isinstance(value, str):
            return value
        else:
            raise SchemaParserException("Required string '{field}' is not a string".format(field=key))

    # gets the required integer and casts it to an integer.  Throws an exception if it is missing or not an int
    @staticmethod
    def get_required_integer(obj, key):
        value = ParserUtils.get_required(obj, key)
        if isinstance(value, int):
            return int(value)
        else:
            raise SchemaParserException("Required integer '{field}' is not an integer".format(field=key))

    # gets the value associated with key in the dict, or None if it's not present
    @staticmethod
    def get_optional(obj, key):
        if key in obj.keys():
            return obj[key]
        else:
            return None

    def get_optional_string(obj, key):
        value = ParserUtils.get_optional(obj, key)
        if isinstance(value, str):
            return value
        elif value is None:
            return None
        else:
            raise SchemaParserException("Expected string '{field}' is not a string".format(field=key))

    def get_optional_integer(obj, key):
        value = ParserUtils.get_optional(obj, key)
        if value is not None:
            try:
                value = int(value)
                return value
            except ValueError:
                raise SchemaParserException("Expected integer '{field}' is not an integer".format(field=key))
        else:
            return None
