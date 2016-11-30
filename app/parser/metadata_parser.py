import logging
import uuid
from datetime import datetime

from app.authentication.invalid_token_exception import InvalidTokenException

logger = logging.getLogger(__name__)


def iso_8601_data_parser(iso_8601_string):
    return datetime.strptime(iso_8601_string, "%Y-%m-%d")


def uuid_4_parser(plain_string):
    return str(uuid.UUID(plain_string))


def id_generator():
    return str(uuid.uuid4())


class MetadataField(object):
    def __init__(self, mandatory=True, validator=None, generator=None):
        # the function to convert the value from the jwt into the required data type
        self._validator = validator
        # the function to execute if the value should be auto-generated
        self._generator = generator
        # flag to indicate if the value must exist in the jwt token
        self.mandatory = mandatory

    def validate(self, original_value):
        if self.mandatory and original_value is None:
            raise ValueError("Missing mandatory field value")
        if self._validator:
            # The parser methods throw exceptions on incorrect data
            self._validator(original_value)

    def generate(self):
        if self._generator:
            return self._generator()

        return None

metadata_fields = {
    "user_id": MetadataField(),
    "ru_ref": MetadataField(),
    "ru_name": MetadataField(),
    "eq_id": MetadataField(),
    "collection_exercise_sid": MetadataField(),
    "period_id": MetadataField(),
    "period_str": MetadataField(),
    "ref_p_start_date": MetadataField(validator=iso_8601_data_parser),
    "ref_p_end_date": MetadataField(validator=iso_8601_data_parser),
    "form_type": MetadataField(),
    "return_by": MetadataField(validator=iso_8601_data_parser),
    "trad_as": MetadataField(mandatory=False),
    "employment_date": MetadataField(mandatory=False, validator=iso_8601_data_parser),
    "region_code": MetadataField(mandatory=False),
    "tx_id": MetadataField(mandatory=False, validator=uuid_4_parser, generator=id_generator),
    "variant_flags": MetadataField(mandatory=False),
}


def parse_metadata(metadata_to_check):
    parsed = {}
    try:
        for key, field in metadata_fields.items():
            logger.debug("parse_metadata: Adding attr %s", key)
            if key in metadata_to_check:
                attr_value = metadata_to_check[key]
                field.validate(attr_value)
                logger.debug("with value %s", attr_value)
            else:
                logger.debug("Generating value for %s", key)
                attr_value = field.generate()

            parsed[key] = attr_value
    except (RuntimeError, ValueError, TypeError) as e:
        logger.error("parse_metadata: Unable to parse")
        logger.exception(e)
        raise InvalidTokenException("Incorrect data in token")
    return parsed


def is_valid_metadata(metadata):
    for key, field in metadata_fields.items():
        if field.mandatory and key not in metadata:
            return False, key
    return True, ""
