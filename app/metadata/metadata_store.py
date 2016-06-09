from app.authentication.invalid_token_exception import InvalidTokenException
from datetime import datetime
import jsonpickle
import logging

logger = logging.getLogger(__name__)


class MetaDataConstants(object):
    """Constant for meta data values"""
    USER_ID = 'user_id'
    RU_REF = 'ru_ref'
    RU_NAME = 'ru_name'
    EQ_ID = 'eq_id'
    COLLECTION_EXERCISE_SID = 'collection_exercise_sid'
    PERIOD_ID = 'period_id'
    PERIOD_STR = 'period_str'
    REF_P_START_DATE = 'ref_p_start_date'
    REF_P_END_DATE = 'ref_p_end_date'
    FORM_TYPE = 'form_type'
    RETURN_BY = 'return_by'
    TRAD_AS = 'trad_as'
    EMPLOYMENT_DATE = 'employment_date'


class MetaDataStore(object):

    METADATA_KEY = "METADATA"

    VALUES_FOR_VALIDATION = [MetaDataConstants.USER_ID, MetaDataConstants.RU_REF, MetaDataConstants.RU_NAME, MetaDataConstants.EQ_ID,
                             MetaDataConstants.COLLECTION_EXERCISE_SID, MetaDataConstants.PERIOD_ID, MetaDataConstants.PERIOD_STR,
                             MetaDataConstants.REF_P_END_DATE, MetaDataConstants.REF_P_START_DATE, MetaDataConstants.FORM_TYPE,
                             MetaDataConstants.RETURN_BY]

    def __init__(self, user_id, ru_ref, ru_name, eq_id, collection_exercise_sid, period_id, period_str, ref_p_end_date,
                 ref_p_start_date, form_type, return_by, trad_as, employment_date):
        self.user_id = user_id
        self.ru_ref = ru_ref
        self.ru_name = ru_name
        self.eq_id = eq_id
        self.collection_exercise_sid = collection_exercise_sid
        self.period_id = period_id
        self.period_str = period_str
        self.ref_p_end_date = ref_p_end_date
        self.ref_p_start_date = ref_p_start_date
        self.form_type = form_type
        self.return_by = return_by
        self.trad_as = trad_as
        self.employment_date = employment_date

    def get_ru_ref(self):
        return self.ru_ref

    def get_ru_name(self):
        return self.ru_name

    def get_eq_id(self):
        return self.eq_id

    def get_collection_exercise_sid(self):
        return self.collection_exercise_sid

    def get_period_id(self):
        return self.period_id

    def get_period_str(self):
        return self.period_str

    def get_form_type(self):
        return self.form_type

    def get_ref_p_start_date(self):
        return self.ref_p_start_date

    def get_ref_p_end_date(self):
        return self.ref_p_end_date

    def get_trad_as(self):
        return self.trad_as

    def get_return_by(self):
        return self.return_by

    def get_user_id(self):
        return self.user_id

    def get_employment_date(self):
        return self.employment_date

    @staticmethod
    def is_valid(token):
        for value in MetaDataStore.VALUES_FOR_VALIDATION:
            if value not in token:
                return False, value
        return True, ""

    @staticmethod
    def save_instance(user, token):
        try:
            # mandatory values
            user_id = token[MetaDataConstants.USER_ID]
            ru_ref = token[MetaDataConstants.RU_REF]
            ru_name = token[MetaDataConstants.RU_NAME]
            eq_id = token[MetaDataConstants.EQ_ID]
            collection_exercise_sid = token[MetaDataConstants.COLLECTION_EXERCISE_SID]
            period_id = token[MetaDataConstants.PERIOD_ID]
            period_str = token[MetaDataConstants.PERIOD_STR]
            ref_p_end_date = datetime.strptime(token[MetaDataConstants.REF_P_END_DATE], "%Y-%m-%d")
            ref_p_start_date = datetime.strptime(token[MetaDataConstants.REF_P_START_DATE], "%Y-%m-%d")
            form_type = token[MetaDataConstants.FORM_TYPE]
            return_by = datetime.strptime(token[MetaDataConstants.RETURN_BY], "%Y-%m-%d")

            # optional values
            trad_as = token[MetaDataConstants.TRAD_AS] if MetaDataConstants.TRAD_AS in token else None

            # TODO remove when rrm implements employment date
            if MetaDataConstants.EMPLOYMENT_DATE in token and token[MetaDataConstants.EMPLOYMENT_DATE]:

                employment_date = datetime.strptime(token[MetaDataConstants.EMPLOYMENT_DATE], "%Y-%m-%d")
            else:
                employment_date = datetime.strptime("2016-06-10", "%Y-%m-%d")

            metadata = MetaDataStore(user_id, ru_ref, ru_name, eq_id, collection_exercise_sid, period_id, period_str,
                                     ref_p_end_date, ref_p_start_date, form_type, return_by, trad_as, employment_date)

            frozen = jsonpickle.encode(metadata)
            data = user.get_questionnaire_data()
            data[MetaDataStore.METADATA_KEY] = frozen

            return metadata
        except (RuntimeError, ValueError) as e:
            logger.error("Unable to create Metadata store")
            logger.exception(e)
            raise InvalidTokenException("Incorrect date format in token")

    @staticmethod
    def get_instance(user):
        data = user.get_questionnaire_data()
        if MetaDataStore.METADATA_KEY in data:
            metadata = data[MetaDataStore.METADATA_KEY]
            thawed = jsonpickle.decode(metadata)
            return thawed
        else:
            raise RuntimeError("No metadata for user %s", user.get_user_id())
