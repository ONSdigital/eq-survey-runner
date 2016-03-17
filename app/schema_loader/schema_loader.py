from app import settings
import json
import os
import logging


logger = logging.getLogger(__name__)


def load_schema(eq_id, form_type):
    """
    Given a schema id this method will load the correct schema file from disk. Currently the parameter is ignored
    and the MCI schema is returned
    :param eq_id: The id of the schema file
    :param form_type the form type of the file
    :return: The Schema representing in a dict
    """
    logging.debug("About to load schema for eq-id %s and form type %s" + form_type)
    try:
        schema_file = open(os.path.join(settings.EQ_SCHEMA_DIRECTORY, eq_id + "_" + form_type + ".json"), encoding="utf8")
        return json.load(schema_file)
    except FileNotFoundError:
        logging.error("No file exists for eq-id %s and form type %s")
        return None
