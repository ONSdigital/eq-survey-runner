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

mandatory_metadata = {
    'tx_id': 'uuid',
}


def parse_metadata(decrypted_token, schema_metadata):
    """
    Extracts values from the JWT claims that are defined in the schema's metadata.
    Ensures that the values adhere to the expected format.
    :param decrypted_token:
    :param schema_metadata:
    :return: Validated claims
    """

    required_schema_metadata = _validate_mandatory_schema_metadata(decrypted_token, schema_metadata)
    mandatory_metadata.update(required_schema_metadata)
    claims = decrypted_token.copy()
    claims['tx_id'] = claims.get('tx_id', id_generator())  # Generate tx_id if not preset in claims

    try:
        for key, field in mandatory_metadata.items():
            if key in claims:
                value = claims[key]
                validators[field](value)
                logger.debug('parsing metadata', key=key, value=value)

    except (RuntimeError, ValueError, TypeError) as e:
        logger.error('unable to parse metadata', exc_info=e)
        raise InvalidTokenException('incorrect data in token')

    return claims


def _validate_mandatory_schema_metadata(metadata, schema_metadata):
    """
    Validate that JWT claims contain metadata defined within the schema
    :param metadata:
    :param schema_metadata:
    :return:
    """
    for key in schema_metadata.keys():
        if not metadata.get(key):
            if key == 'trad_as_or_ru_name':
                if 'trad_as' in metadata or 'ru_name' in metadata:
                    continue
            raise InvalidTokenException('Missing key/value for {}'.format(key))

    return schema_metadata
