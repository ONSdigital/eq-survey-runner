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
    def __init__(self, claim_id, mandatory=True, parser=string_parser, generator=None):
        # the claim id from the JWT token
        self.claim_id = claim_id
        # the function to convert the value from the jwt into the required data type
        self.parser = parser
        # flag to indicate if the value must exist in the jwt token
        self.mandatory = mandatory
        # the function to execute if the value should be auto-generated
        self.generator = generator


class MetadataConstants(object):
    """Constant for meta data values"""
    USER_ID = MetadataConstant(claim_id='user_id')
    RU_REF = MetadataConstant(claim_id='ru_ref')
    RU_NAME = MetadataConstant(claim_id='ru_name')
    EQ_ID = MetadataConstant(claim_id='eq_id')
    COLLECTION_EXERCISE_SID = MetadataConstant(claim_id='collection_exercise_sid')
    PERIOD_ID = MetadataConstant(claim_id='period_id')
    PERIOD_STR = MetadataConstant(claim_id='period_str')
    REF_P_START_DATE = MetadataConstant(claim_id='ref_p_start_date', parser=iso_8601_data_parser)
    REF_P_END_DATE = MetadataConstant(claim_id='ref_p_end_date', parser=iso_8601_data_parser)
    FORM_TYPE = MetadataConstant(claim_id='form_type')
    RETURN_BY = MetadataConstant(claim_id='return_by', parser=iso_8601_data_parser)
    TRAD_AS = MetadataConstant(claim_id='trad_as', mandatory=False)
    EMPLOYMENT_DATE = MetadataConstant(claim_id='employment_date', mandatory=False, parser=iso_8601_data_parser)
    TRANSACTION_ID = MetadataConstant(claim_id='tx_id', mandatory=False, parser=uuid_4_parser, generator=id_generator)


class MetadataParser(object):

    @staticmethod
    def _get_constants():
        for attr in dir(MetadataConstants):
            constant = getattr(MetadataConstants, attr)
            if isinstance(constant, MetadataConstant):
                yield constant

    @staticmethod
    def is_valid(token):
        for constant in MetadataParser._get_constants():
            if constant.mandatory and constant.claim_id not in token:
                return False, constant.claim_id
        return True, ""

    @staticmethod
    def build_metadata(token):
        try:
            metadata = MetadataParser()
            # loop around all the constants and add them as attributes of the metadata object
            for constant in MetadataParser._get_constants():
                attr_name = constant.claim_id
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
                setattr(metadata, attr_name, attr_value)
            return metadata
        except (RuntimeError, ValueError, TypeError) as e:
            logger.error("Unable to parse Metadata")
            logger.exception(e)
            raise InvalidTokenException("Incorrect data in token")
