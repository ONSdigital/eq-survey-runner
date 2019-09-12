import os
import requests
import simplejson as json

from structlog import get_logger
from werkzeug.exceptions import NotFound

from app.questionnaire.questionnaire_schema import (
    QuestionnaireSchema,
    DEFAULT_LANGUAGE_CODE,
)
from app.setup import cache

logger = get_logger()

DEFAULT_SCHEMA_DIR = 'data'

LANGUAGES_MAP = {
    'test_language': [['en', 'cy']],
    'census_household_gb_wls': [['en', 'cy']],
    'census_individual_gb_wls': [['en', 'cy']],
    'census_household_gb_nir': [['en'], ['en', 'ga'], ['en', 'en_US']],
    'census_individual_gb_nir': [['en'], ['en', 'ga'], ['en', 'en_US']],
}


def get_allowed_languages(schema_name, launch_language):
    for language_combination in LANGUAGES_MAP.get(schema_name, []):
        if launch_language in language_combination:
            return language_combination
    return [DEFAULT_LANGUAGE_CODE]


def load_schema_from_metadata(metadata):
    if metadata.get('survey_url'):
        return load_schema_from_url(
            metadata['survey_url'], metadata.get('language_code')
        )

    return load_schema_from_name(
        metadata.get('schema_name'), language_code=metadata.get('language_code')
    )


def load_schema_from_session_data(session_data):
    return load_schema_from_metadata(vars(session_data))


@cache.memoize()
def load_schema_from_name(schema_name, language_code=None):
    language_code = language_code or DEFAULT_LANGUAGE_CODE
    schema_json = _load_schema_file(schema_name, language_code)

    return QuestionnaireSchema(schema_json, language_code)


def transform_case_type(case_type_input):
    census_case_types = {
        'HH': 'household',
        'HI': 'individual',
        'CE': 'communal_establishment',
        'CI': 'communal_individual',
    }

    return census_case_types[case_type_input]


def transform_region_code(region_code_input):
    return region_code_input.lower().replace('-', '_')


def transform_survey(survey_input):
    return survey_input.lower()


def get_schema_name_from_census_params(survey, case_type, region_code):
    try:
        case_type_transformed = transform_case_type(case_type)
    except KeyError:
        raise ValueError(
            'Invalid case_type parameter was specified. Must be one of `HH`, `HI`, `CE`, `CI`'
        )

    region_code_transformed = transform_region_code(region_code)
    survey_transformed = transform_survey(survey)

    schema_name = (
        f'{survey_transformed}_{case_type_transformed}_{region_code_transformed}'
    )
    return schema_name


def _load_schema_file(schema_name, language_code):
    """
    Load a schema, optionally for a specified language.
    :param schema_name: The name of the schema e.g. census_household
    :param language_code: ISO 2-character code for language e.g. 'en', 'cy'
    """
    schema_path = get_schema_file_path(schema_name, language_code)

    if language_code != DEFAULT_LANGUAGE_CODE and not os.path.exists(schema_path):
        logger.info(
            "couldn't find requested language schema, falling back to 'en'",
            schema_file=schema_name,
            language_code=language_code,
            schema_path=schema_path,
        )
        schema_path = get_schema_file_path(schema_name, DEFAULT_LANGUAGE_CODE)

    logger.info(
        'loading schema',
        schema_name=schema_name,
        language_code=language_code,
        schema_path=schema_path,
    )

    try:
        with open(schema_path, encoding='utf8') as json_data:
            return json.load(json_data, use_decimal=True)

    except FileNotFoundError as e:
        logger.error('no schema file exists', filename=schema_path)
        raise e


@cache.memoize()
def load_schema_from_url(survey_url, language_code):
    language_code = language_code or DEFAULT_LANGUAGE_CODE
    logger.info(
        'loading schema from URL', survey_url=survey_url, language_code=language_code
    )

    constructed_survey_url = '{}?language={}'.format(survey_url, language_code)

    req = requests.get(constructed_survey_url)
    schema_response = req.content.decode()

    if req.status_code == 404:
        logger.error('no schema exists', survey_url=constructed_survey_url)
        raise NotFound

    return QuestionnaireSchema(json.loads(schema_response), language_code)


def get_schema_path(language_code, schema_dir=DEFAULT_SCHEMA_DIR):
    return os.path.join(schema_dir, language_code)


def get_schema_file_path(schema_name, language_code):
    schema_dir = get_schema_path(language_code)
    schema_filename = f'{schema_name}.json'
    return os.path.join(schema_dir, schema_filename)
