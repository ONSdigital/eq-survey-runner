import logging

from app.data_model.questionnaire_store import get_metadata
from app.parser.schema_parser_factory import SchemaParserFactory
from app.schema_loader.schema_loader import load_schema

from flask_login import current_user

logger = logging.getLogger(__name__)


def get_schema():
    metadata = get_metadata(current_user)

    eq_id = metadata["eq_id"]
    form_type = metadata["form_type"]
    logger.debug("Requested questionnaire %s for form type %s", eq_id, form_type)

    schema = load_and_parse_schema(eq_id, form_type)
    if not schema:
        raise ValueError("No schema available")
    logger.debug("Constructing brand new User Journey Manager")
    return schema


def load_and_parse_schema(eq_id, form_type):
    """
    Use the schema loader to get the schema from disk. Then use the parse to construct the object schema
    :param eq_id: the id of the questionnaire
    :param form_type: the form type
    :return: an object schema
    """
    # load the schema

    json_schema = load_schema(eq_id, form_type)
    if json_schema:
        parser = SchemaParserFactory.create_parser(json_schema)
        schema = parser.parse()
        return schema
    else:
        return None
