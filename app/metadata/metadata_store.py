from app.authentication.invalid_token_exception import InvalidTokenException
from datetime import datetime
import jsonpickle
import logging
import uuid

logger = logging.getLogger(__name__)


def iso_8601_data_parser(iso_8601_string):
    return datetime.strptime(iso_8601_string, "%Y-%m-%d")


def string_parser(plain_string):
    return plain_string


def uuid_4_parser(plain_string):
    return str(uuid.UUID(plain_string))


def id_generator():
    return str(uuid.uuid4())


class MetaDataConstant(object):
    def __init__(self, claim_id, mandatory=True, parser=string_parser, generator=None):
        # the claim id from the JWT token
        self.claim_id = claim_id
        # the function to convert the value from the jwt into the required data type
        self.parser = parser
        # flag to indicate if the value must exist in the jwt token
        self.mandatory = mandatory
        # the function to execute if the value should be auto-generated
        self.generator = generator


class MetaDataConstants(object):
    """Constant for meta data values"""
    USER_ID = MetaDataConstant(claim_id='user_id')
    RU_REF = MetaDataConstant(claim_id='ru_ref')
    RU_NAME = MetaDataConstant(claim_id='ru_name')
    EQ_ID = MetaDataConstant(claim_id='eq_id')
    COLLECTION_EXERCISE_SID = MetaDataConstant(claim_id='collection_exercise_sid')
    PERIOD_ID = MetaDataConstant(claim_id='period_id')
    PERIOD_STR = MetaDataConstant(claim_id='period_str')
    REF_P_START_DATE = MetaDataConstant(claim_id='ref_p_start_date', parser=iso_8601_data_parser)
    REF_P_END_DATE = MetaDataConstant(claim_id='ref_p_end_date', parser=iso_8601_data_parser)
    FORM_TYPE = MetaDataConstant(claim_id='form_type')
    RETURN_BY = MetaDataConstant(claim_id='return_by', parser=iso_8601_data_parser)
    TRAD_AS = MetaDataConstant(claim_id='trad_as', mandatory=False)
    EMPLOYMENT_DATE = MetaDataConstant(claim_id='employment_date', mandatory=False, parser=iso_8601_data_parser)
    TRANSACTION_ID = MetaDataConstant(claim_id='tx_id', mandatory=False, parser=uuid_4_parser, generator=id_generator)


class MetaDataStore(object):

    METADATA_KEY = "METADATA"

    @staticmethod
    def _get_constants():
        for attr in dir(MetaDataConstants):
            constant = getattr(MetaDataConstants, attr)
            if isinstance(constant, MetaDataConstant):
                yield constant

    @staticmethod
    def is_valid(token):
        for constant in MetaDataStore._get_constants():
            if constant.mandatory and constant.claim_id not in token:
                return False, constant.claim_id
        return True, ""

    @staticmethod
    def save_instance(user, token):
        try:
            metadata = MetaDataStore()
            # loop around all the constants and add them as attributes of the metadata store object
            for constant in MetaDataStore._get_constants():
                attr_name = constant.claim_id
                logger.debug("MetaDataStore adding attr %s", attr_name)
                if attr_name in token:
                    value = token[constant.claim_id]
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

            frozen = jsonpickle.encode(metadata)
            data = user.get_questionnaire_data()
            data[MetaDataStore.METADATA_KEY] = frozen

            return metadata
        except (RuntimeError, ValueError, TypeError) as e:
            logger.error("Unable to create Metadata store")
            logger.exception(e)
            raise InvalidTokenException("Incorrect data in token")

    @staticmethod
    def get_instance(user):

        try:
            data = user.get_questionnaire_data()
            if MetaDataStore.METADATA_KEY in data:
                metadata = data[MetaDataStore.METADATA_KEY]
                thawed = jsonpickle.decode(metadata)
                return thawed
            else:
                raise RuntimeError("No metadata for user %s", user.get_user_id())
        except AttributeError:
            logger.debug("Anonymous user requesting metadata get instance")
            # anonymous user mixin - this happens on the error pages before authentication
            return None
