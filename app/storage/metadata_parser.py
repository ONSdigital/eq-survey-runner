import uuid
from datetime import datetime
from structlog import get_logger

from sdc.crypto.exceptions import InvalidTokenException

logger = get_logger()


def iso_8601_date_parser(iso_8601_string):
    return datetime.strptime(iso_8601_string, '%Y-%m-%d')


def uuid_4_parser(plain_string):
    return str(uuid.UUID(plain_string))


def clean_leading_trailing_spaces(metadata):
    for key, value in metadata.items():
        if isinstance(value, str):
            metadata[key] = value.strip()

    return metadata


def id_generator():
    return str(uuid.uuid4())


VALIDATORS = {
    'date': iso_8601_date_parser,
    'uuid': uuid_4_parser,
    'string': lambda *args: None,
    'object': lambda *args: None
}

MANDATORY_METADATA = {
    'eq_id': {
        'validator': 'string'
    },
    'form_type': {
        'validator': 'string'
    },
    'ru_ref': {
        'validator': 'string'
    },
    'collection_exercise_sid': {
        'validator': 'string'
    },
    'tx_id': {
        'validator': 'uuid'
    }
}


def parse_runner_claims(claims):
    cleaned_claims = clean_leading_trailing_spaces(claims.copy())
    cleaned_claims['tx_id'] = claims.get('tx_id', id_generator())  # Generate tx_id if not preset in claims
    validate_metadata(cleaned_claims, MANDATORY_METADATA)

    return cleaned_claims


def validate_metadata(claims, required_metadata):
    _validate_mandatory_metadata(claims, required_metadata)
    _validate_metadata_values(claims, required_metadata)


def _validate_mandatory_metadata(metadata, required_metadata):
    """
    Validate that JWT claims contain the required metadata
    :param metadata:
    :param required_metadata:
    """
    for key in required_metadata.keys():
        if key == 'variant_flags':
            # variant flags is empty by default
            valid = 'variant_flags' in metadata
        elif key == 'trad_as_or_ru_name':
            # either of 'trad_as' or 'ru_name' is required
            valid = 'trad_as' in metadata or 'ru_name' in metadata
        else:
            valid = bool(metadata.get(key))

        if not valid:
            raise InvalidTokenException('Missing key/value for {}'.format(key))


def _validate_metadata_values(claims, validators):
    """
    Validate metadata from the JWT claims that are required by the schema/runner.
    Ensures that the values adhere to the expected format.
    :param claims:
    :param validators:
    """
    try:
        for key, field in validators.items():
            if claims.get(key):
                value = claims[key]
                VALIDATORS[field['validator']](value)
                logger.debug('parsing metadata', key=key, value=value)

    except (RuntimeError, ValueError, TypeError) as error:
        logger.error('unable to parse metadata', exc_info=error)
        raise InvalidTokenException('incorrect data in token') from error
    except KeyError as key_error:
        error_msg = 'Invalid validator for schema metadata - {}'.format(key_error.args[0])
        logger.error(error_msg, exc_info=key_error)
        raise KeyError(error_msg) from key_error
