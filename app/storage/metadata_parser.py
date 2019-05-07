import uuid
from datetime import datetime
from structlog import get_logger

from sdc.crypto.exceptions import InvalidTokenException

logger = get_logger()


def iso_8601_date_parser(iso_8601_string):
    return datetime.strptime(iso_8601_string, '%Y-%m-%d')


def uuid_4_parser(plain_string):
    return str(uuid.UUID(plain_string))


def boolean_parser(boolean_value):
    if not isinstance(boolean_value, bool):
        raise TypeError('Claim was not of type `bool`')
    return boolean_value


def string_parser(string_value):
    if not isinstance(string_value, str) or string_value == '':
        raise TypeError('Claim not a valid string value')
    return string_value


def optional_string_parser(optional_string_value):
    if not isinstance(optional_string_value, str):
        raise TypeError('Claim not a valid/empty string')
    return optional_string_value


def clean_leading_trailing_spaces(metadata):
    for key, value in metadata.items():
        if isinstance(value, str):
            metadata[key] = value.strip()

    return metadata


VALIDATORS = {
    'date': iso_8601_date_parser,
    'uuid': uuid_4_parser,
    'boolean': boolean_parser,
    'string': string_parser,
    'optional_string': optional_string_parser,
}

MANDATORY_METADATA = [
    {
        'name': 'eq_id',
        'validator': 'string',
    },
    {
        'name': 'form_type',
        'validator': 'string',
    },
    {
        'name': 'ru_ref',
        'validator': 'string',
    },
    {
        'name': 'collection_exercise_sid',
        'validator': 'string',
    },
    {
        'name': 'tx_id',
        'validator': 'uuid',
    },
    {
        'name': 'case_id',
        'validator': 'uuid',
    },
    {
        'name': 'response_id',
        'validator': 'string',
    },
]


def parse_runner_claims(claims):
    cleaned_claims = clean_leading_trailing_spaces(claims.copy())
    validate_metadata(cleaned_claims, MANDATORY_METADATA)

    return cleaned_claims


def validate_metadata(claims, required_metadata):
    _validate_metadata_values_are_valid(claims, required_metadata)


def _validate_metadata_values_are_valid(claims, required_metadata):
    """
    Validate metadata from the JWT claims that are required by the schema/runner.
    Ensures that the values adhere to the expected format.
    :param claims:
    :param required_metadata:
    """
    try:
        for metadata_field in required_metadata:
            name = metadata_field['name']
            claim = claims.get(name)
            if name not in claims:
                raise InvalidTokenException('Missing required key {} from claims'.format(name))

            logger.debug('parsing metadata', key=name, value=claim)
            VALIDATORS[metadata_field['validator']](claim)

    except (RuntimeError, ValueError, TypeError) as error:
        logger.error('Unable to parse metadata', key=name, value=claim, exc_info=error)
        raise InvalidTokenException('incorrect data in token for {}'.format(name)) from error
    except KeyError as key_error:
        error_msg = 'Invalid validator for schema metadata - {}'.format(key_error.args[0])
        logger.error(error_msg, exc_info=key_error)
        raise KeyError(error_msg) from key_error
