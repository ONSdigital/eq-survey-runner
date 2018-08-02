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
    """Strict matching of boolean values from JWT claims.
    :param metadata:
    :raises: TypeError - when a non boolean value has been loaded from the JWT.
    :returns: A boolean value
    """
    if not isinstance(boolean_value, bool):
        raise TypeError('Claim was not of type `bool`')
    return boolean_value


def clean_leading_trailing_spaces(metadata):
    for key, value in metadata.items():
        if isinstance(value, str):
            metadata[key] = value.strip()

    return metadata


VALIDATORS = {
    'date': iso_8601_date_parser,
    'uuid': uuid_4_parser,
    'boolean': boolean_parser,
    'string': lambda *args: None,
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
]


def parse_runner_claims(claims):
    cleaned_claims = clean_leading_trailing_spaces(claims.copy())
    validate_metadata(cleaned_claims, MANDATORY_METADATA)

    return cleaned_claims


def validate_metadata(claims, required_metadata):
    _validate_metadata_is_present(claims, required_metadata)
    _validate_metadata_values_are_valid(claims, required_metadata)


def _validate_metadata_is_present(metadata, required_metadata):
    """
    Validate that JWT claims contain the required metadata (both eq-runner and survey specific required metadata).
    :param metadata:
    :param required_metadata:
    """
    for metadata_field in required_metadata:
        name = metadata_field['name']
        if name == 'trad_as_or_ru_name':
            # either of 'trad_as' or 'ru_name' is required
            valid = bool(metadata.get('trad_as') or metadata.get('ru_name'))
        else:
            # Validate that the value is one of:
            # a) A boolean value
            # b) A non empty value
            value = metadata.get(name)
            valid = isinstance(value, bool) or bool(value)

        if not valid:
            raise InvalidTokenException('Missing key/value for {}'.format(name))


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
            if claim:
                logger.debug('parsing metadata', key=name, value=claim)
                VALIDATORS[metadata_field['validator']](claim)

    except (RuntimeError, ValueError, TypeError) as error:
        logger.error('Unable to parse metadata', key=name, value=claim, exc_info=error)
        raise InvalidTokenException('incorrect data in token') from error
    except KeyError as key_error:
        error_msg = 'Invalid validator for schema metadata - {}'.format(key_error.args[0])
        logger.error(error_msg, exc_info=key_error)
        raise KeyError(error_msg) from key_error
