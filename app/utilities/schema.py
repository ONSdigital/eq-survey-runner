import json
import os

from structlog import get_logger

from app import cache
from app import settings

logger = get_logger()

DEFAULT_LANGUAGE_CODE = 'en'


@cache.memoize()
def load_schema_from_metadata(metadata):
    return load_schema_from_params(metadata['eq_id'], metadata['form_type'], metadata.get('language_code'))


@cache.memoize()
def load_schema_from_params(eq_id, form_type, language_code=DEFAULT_LANGUAGE_CODE):
    return load_schema_file("{}_{}.json".format(eq_id, form_type), language_code)


def load_schema_file(schema_file, language_code=None):
    """
    Load a schema, optionally for a specified language.
    :param schema_file: The name of the schema e.g. census_household.json
    :param language_code: ISO 2-character code for language e.g. 'en', 'cy'
    """
    language_code = language_code or DEFAULT_LANGUAGE_CODE
    schema_path = get_schema_file_path(schema_file, language_code)

    if language_code != DEFAULT_LANGUAGE_CODE and not os.path.exists(schema_path):
        logger.info("couldn't find requested language schema, falling back to 'en'",
                    schema_file=schema_file, language_code=language_code, schema_path=schema_path)
        schema_path = get_schema_file_path(schema_file, DEFAULT_LANGUAGE_CODE)

    logger.info("loading schema", schema_file=schema_file, language_code=language_code, schema_path=schema_path)

    try:
        with open(schema_path, encoding="utf8") as json_data:
            return json.load(json_data)

    except FileNotFoundError as e:
        logger.error("no schema file exists", filename=schema_path)
        raise e


def get_schema_path(language_code=DEFAULT_LANGUAGE_CODE):
    return os.path.join(settings.EQ_SCHEMA_DIRECTORY, language_code)


def get_schema_file_path(schema_file, language_code=DEFAULT_LANGUAGE_CODE):
    schema_dir = get_schema_path(language_code)
    return os.path.join(schema_dir, schema_file)


def available_json_schemas():
    files = []
    for file in os.listdir(get_schema_path()):
        if os.path.isfile(get_schema_file_path(file)) and file.endswith(".json"):
            files.append(file)
    return sorted(files)
