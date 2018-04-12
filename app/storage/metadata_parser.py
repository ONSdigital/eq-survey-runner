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


validators = {
    'date': iso_8601_date_parser,
    'uuid': uuid_4_parser,
    'string': lambda *args: None
}

mandatory_meta = {
    'tx_id': 'uuid',
}


def parse_metadata(metadata_to_check, schema_metadata):

    parsed = metadata_to_check.copy()

    required_metadata = _validate_mandatory_schema_metadata(parsed, schema_metadata)

    mandatory_meta.update(required_metadata)

    try:
        for key, field in mandatory_meta.items():

            if key in parsed:
                attr_value = parsed[key]
                validators[field](attr_value)
                logger.debug('parsing metadata', key=key, value=attr_value)
                parsed[key] = attr_value
            elif key == 'tx_id':
                logger.debug('generating metadata value', key=key)
                parsed[key] = id_generator()

    except (RuntimeError, ValueError, TypeError) as e:
        logger.error('unable to parse metadata', exc_info=e)
        raise InvalidTokenException('incorrect data in token')

    return parsed


def _validate_mandatory_schema_metadata(metadata, schema_metadata):

    for key in schema_metadata.keys():
        if key not in metadata or not metadata[key]:
            if key == 'trad_as_or_ru_name':
                if 'trad_as' in metadata or 'ru_name' in metadata:
                    continue
            raise InvalidTokenException('Missing key/value for {}'.format(key))

    return schema_metadata
