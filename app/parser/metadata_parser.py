import logging
import uuid
from datetime import datetime

from app.authentication.invalid_token_exception import InvalidTokenException

logger = logging.getLogger(__name__)


def iso_8601_data_parser(iso_8601_string):
    return datetime.strptime(iso_8601_string, "%Y-%m-%d")


def string_parser(plain_string):
    return plain_string


def uuid_4_parser(plain_string):
    return str(uuid.UUID(plain_string))


def id_generator():
    return str(uuid.uuid4())


class MetadataConstant(object):
    def __init__(self, mandatory=True, parser=string_parser, generator=None):
        # the function to convert the value from the jwt into the required data type
        self.parser = parser
        # flag to indicate if the value must exist in the jwt token
        self.mandatory = mandatory
        # the function to execute if the value should be auto-generated
        self.generator = generator


metadata_constants = {
    "user_id": MetadataConstant(),
    "ru_ref": MetadataConstant(),
    "ru_name": MetadataConstant(),
    "eq_id": MetadataConstant(),
    "collection_exercise_sid": MetadataConstant(),
    "period_id": MetadataConstant(),
    "period_str": MetadataConstant(),
    "ref_p_start_date": MetadataConstant(parser=iso_8601_data_parser),
    "ref_p_end_date": MetadataConstant(parser=iso_8601_data_parser),
    "form_type": MetadataConstant(),
    "return_by": MetadataConstant(parser=iso_8601_data_parser),
    "trad_as": MetadataConstant(mandatory=False),
    "employment_date": MetadataConstant(mandatory=False, parser=iso_8601_data_parser),
    "tx_id": MetadataConstant(mandatory=False, parser=uuid_4_parser, generator=id_generator),
}


class MetadataParser(object):

    @staticmethod
    def is_valid(token):
        for key, constant in metadata_constants.items():
            if constant.mandatory and key not in token:
                return False, key
        return True, ""

    @staticmethod
    def build_metadata(token):
        try:
            metadata = {}
            # loop around all the constants and add them as attributes of the metadata object
            for attr_name, constant in metadata_constants.items():
                logger.debug("MetadataParser adding attr %s", attr_name)
                if attr_name in token:
                    value = token[attr_name]
                    attr_value = constant.parser(value)
                    logger.debug("with value %s", attr_value)
                elif constant.mandatory:
                    logger.warning("Missing constant value for %s", constant.claim_id)
                    raise ValueError("Missing constant value %s".format(constant.claim_id))
                else:
                    if constant.generator:
                        logger.debug("Generating value for %s", attr_name)
                        attr_value = constant.generator()
                    else:
                        logger.debug("No value provide for %s but this is not mandatory, setting to None", attr_name)
                        attr_value = None
                metadata[attr_name] = attr_value
            return metadata
        except (RuntimeError, ValueError, TypeError) as e:
            logger.error("Unable to parse Metadata")
            logger.exception(e)
            raise InvalidTokenException("Incorrect data in token")
