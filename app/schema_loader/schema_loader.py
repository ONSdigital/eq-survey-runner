import json
import logging
import os

from app import settings


class SchemaNotFound(Exception):
    pass

logger = logging.getLogger(__name__)


def load_schema(eq_id, form_type, language_code='en'):
    """
    Given a schema id this method will load the correct schema file from disk. Currently the parameter is ignored
    and the MCI schema is returned
    :param eq_id: The id of the schema file
    :param form_type the form type of the file
    :param language_code the language of the schema to load
    :return: The Schema representing in a dict
    """
    logging.debug("About to load schema for eq-id %s and form type %s and language %s", eq_id, form_type, language_code)

    filename_format = "{}.json"

    if form_type and form_type != "-1":
        filename_format = "{}_" + filename_format

    # form type is mandatory JWT claim, but it isn't needed when getting schemas from the schema bucket
    # in that case default it to -1 and ignore it
    if form_type and form_type != "-1":
        return load_schema_file(filename_format.format(eq_id, form_type), language_code)


def load_schema_file(schema_file, language_code='en'):
    try:
        if language_code is not None and language_code != 'en':
            schema_dir = os.path.join(settings.EQ_SCHEMA_DIRECTORY, language_code)
        else:
            schema_dir = settings.EQ_SCHEMA_DIRECTORY

        schema_path = os.path.join(schema_dir, schema_file)
        with open(schema_path, encoding="utf8") as json_data:
            return json.load(json_data)

    except FileNotFoundError:
        if language_code != 'en':
            return load_schema_file(schema_file, 'en')
        else:
            logging.error("No schema file exists %s", schema_file)
            return None


def available_schemas():
    files = []
    for file in os.listdir(settings.EQ_SCHEMA_DIRECTORY):
        if os.path.isfile(os.path.join(settings.EQ_SCHEMA_DIRECTORY, file)):
            # ignore hidden file
            if file.endswith(".json"):
                files.append(file)
    return sorted(files)
