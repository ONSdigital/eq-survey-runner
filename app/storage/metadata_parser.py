import uuid
from datetime import datetime

from structlog import get_logger

from sdc.crypto.exceptions import InvalidTokenException

logger = get_logger()


def iso_8601_date_parser(iso_8601_string):
    return datetime.strptime(iso_8601_string, '%Y-%m-%d')


def uuid_4_parser(plain_string):
    return str(uuid.UUID(plain_string))


def id_generator():
    return str(uuid.uuid4())


def parse_metadata(decrypted_token, schema_metadata):

    validators = {
        'date': iso_8601_date_parser,
        'uuid': uuid_4_parser,
        'string': lambda *args: None
    }

    mandatory_metadata = {
        'tx_id': 'uuid',
    }

    required_schema_metadata = _validate_mandatory_schema_metadata(decrypted_token, schema_metadata)
    mandatory_metadata.update(required_schema_metadata)
    claims = decrypted_token.copy()

    try:
        for key, field in mandatory_metadata.items():
            if key in claims:
                value = claims[key]
                validators[field](value)
                logger.debug('parsing metadata', key=key, value=value)
            elif key == 'tx_id':
                logger.debug('generating metadata value', key=key)
                claims[key] = id_generator()
    except (RuntimeError, ValueError, TypeError) as e:
        logger.error('unable to parse metadata', exc_info=e)
        raise InvalidTokenException('incorrect data in token')

    return claims


def _validate_mandatory_schema_metadata(metadata, schema_metadata):

    for key in schema_metadata.keys():
        if not metadata.get(key):
            if key == 'trad_as_or_ru_name':
                if 'trad_as' in metadata or 'ru_name' in metadata:
                    continue
            raise InvalidTokenException('Missing key/value for {}'.format(key))

    return schema_metadata
