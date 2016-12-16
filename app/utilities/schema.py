import logging

from app.parser.v0_0_1.schema_parser import SchemaParser
from app.schema_loader.schema_loader import load_schema

logger = logging.getLogger(__name__)


def get_schema(metadata):
    """
    Get the schema for the current user
    :return: (json, schema) # Tuple of json and schema object from schema file
    """

    eq_id = metadata["eq_id"]
    form_type = metadata["form_type"]
    language_code = metadata["language_code"] if "language_code" in metadata else None
    logger.debug("Requested questionnaire %s for form type %s", eq_id, form_type)

    json_schema, schema = load_and_parse_schema(eq_id, form_type, language_code)
    if not json_schema:
        raise ValueError("No schema available")

    return json_schema, schema


def load_and_parse_schema(eq_id, form_type, language_code):
    """
    Use the schema loader to get the schema from disk. Then use the parse to construct the object schema
    :param eq_id: the id of the questionnaire
    :param form_type: the form type
    :return: (json, schema) # Tuple of json and schema object from schema file
    """
    # load the schema

    json_schema = load_schema(eq_id, form_type, language_code)
    if json_schema:
        parser = SchemaParser(json_schema)
        schema = parser.parse()
        return json_schema, schema
    else:
        return None, None
