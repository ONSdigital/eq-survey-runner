import logging
import uuid
from datetime import datetime

from app.authentication.invalid_token_exception import InvalidTokenException

import dateutil.parser

logger = logging.getLogger(__name__)


def iso_8601_data_parser(iso_8601_string):
    return datetime.strptime(iso_8601_string, "%Y-%m-%d")


def string_parser(plain_string):
    return plain_string


def uuid_4_parser(plain_string):
    return str(uuid.UUID(plain_string))


def id_generator():
    return str(uuid.uuid4())


class MetadataField(object):
    original_value = None

    def __init__(self, mandatory=True, parser=string_parser, generator=None):
        # the function to convert the value from the jwt into the required data type
        self.parser = parser
        # the function to execute if the value should be auto-generated
        self._generator = generator
        # flag to indicate if the value must exist in the jwt token
        self.mandatory = mandatory

    def parse(self, original_value):
        self.original_value = original_value
        return self.parser(self.original_value)

    def generate(self):
        if self._generator:
            return self._generator()
        elif not self.mandatory:
            return None

metadata_fields = {
  "user_id": MetadataField(),
  "ru_ref": MetadataField(),
  "ru_name": MetadataField(),
  "eq_id": MetadataField(),
  "collection_exercise_sid": MetadataField(),
  "period_id": MetadataField(),
  "period_str": MetadataField(),
  "ref_p_start_date": MetadataField(parser=iso_8601_data_parser),
  "ref_p_end_date": MetadataField(parser=iso_8601_data_parser),
  "form_type": MetadataField(),
  "return_by": MetadataField(parser=iso_8601_data_parser),
  "trad_as": MetadataField(mandatory=False),
  "employment_date": MetadataField(mandatory=False, parser=iso_8601_data_parser),
  "tx_id": MetadataField(mandatory=False, parser=uuid_4_parser, generator=id_generator),
}


class MetadataParser(object):

    @staticmethod
    def parse(metadata_to_check):
        parsed = {}
        try:
            for key, field in metadata_fields.items():
                logger.debug("MetadataParser adding attr %s", key)
                if key in metadata_to_check:
                    value = metadata_to_check[key]
                    attr_value = field.parse(value)
                    logger.debug("with value %s", attr_value)
                elif field.mandatory:
                    logger.warning("Missing field value for %s", key)
                    raise ValueError("Missing field value %s".format(key))
                else:
                    logger.debug("Generating value for %s", key)
                    attr_value = field.generate()

                parsed[key] = attr_value
        except (RuntimeError, ValueError, TypeError) as e:
            logger.error("Unable to parse Metadata")
            logger.exception(e)
            raise InvalidTokenException("Incorrect data in token")

        return parsed

    @staticmethod
    def is_valid(token):
        for key, field in metadata_fields.items():
            if field.mandatory and key not in token:
                return False, key
        return True, ""


def serialise_metadata(metadata):
    # Strip all 'none' values
    metadata = {k: v for k, v in metadata.items() if v is not None}
    serialised_metadata = metadata
    date_fields = [(k, metadata[k]) for k, v in metadata_fields.items() if v.parser == iso_8601_data_parser and k in metadata]
    for key, value in date_fields:
        to_serialise = value
        if isinstance(value, datetime):
            to_serialise = value.strftime("%Y-%m-%d")
        serialised_metadata[key] = to_serialise
    return serialised_metadata


def deserialise_metadata(serialised_metadata):
    # Strip all 'none' values
    serialised_metadata = {k: v for k, v in serialised_metadata.items() if v is not None}
    deserialised_metadata = serialised_metadata
    date_fields = [(k, serialised_metadata[k]) for k, v in metadata_fields.items() if v.parser == iso_8601_data_parser and k in serialised_metadata]
    for key, value in date_fields:
        deserialised_val = dateutil.parser.parse(value)
        deserialised_metadata[key] = deserialised_val

    return deserialised_metadata
