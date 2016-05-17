from flask_login import current_user
from datetime import datetime


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


class AbstractMetaDataStore(object):

    def store(self, data):
        pass

    def get(self):
        pass


class MetaDataStore(object):

    VALUES_FOR_VALIDATION = [MetaDataConstants.USER_ID, MetaDataConstants.RU_REF, MetaDataConstants.RU_NAME, MetaDataConstants.EQ_ID,
                             MetaDataConstants.COLLECTION_EXERCISE_SID, MetaDataConstants.PERIOD_ID, MetaDataConstants.PERIOD_STR,
                             MetaDataConstants.REF_P_END_DATE, MetaDataConstants.REF_P_START_DATE, MetaDataConstants.FORM_TYPE,
                             MetaDataConstants.RETURN_BY]

    def __init__(self, user=None):
        if user:
            self.user = user
        else:
            self.user = current_user

    def store(self, key, value):
        if self.user is not None:
            data = self.user.get_questionnaire_data()
            data[key] = value

    def store_all(self, token):
        for key in token.keys():
            self.store(key, token[key])

    def get(self, key):
        if self.user is None:
            return None

        data = self.user.get_questionnaire_data()
        if key in data:
            return data[key]
        else:
            return None

    def get_ru_ref(self):
        return self.get(MetaDataConstants.RU_REF)

    def get_ru_name(self):
        return self.get(MetaDataConstants.RU_NAME)

    def get_eq_id(self):
        return self.get(MetaDataConstants.EQ_ID)

    def get_collection_exercise_sid(self):
        return self.get(MetaDataConstants.COLLECTION_EXERCISE_SID)

    def get_period_id(self):
        return self.get(MetaDataConstants.PERIOD_ID)

    def get_period_str(self):
        return self.get(MetaDataConstants.PERIOD_STR)

    def get_form_type(self):
        return self.get(MetaDataConstants.FORM_TYPE)

    def get_ref_p_start_date(self):
        if self.user is None:
            return None
        return datetime.strptime(self.get(MetaDataConstants.REF_P_START_DATE), "%Y-%m-%d")

    def get_ref_p_end_date(self):
        if self.user is None:
            return None
        return datetime.strptime(self.get(MetaDataConstants.REF_P_END_DATE), "%Y-%m-%d")

    def get_trad_as(self):
        return self.get(MetaDataConstants.TRAD_AS)

    def get_return_by(self):
        return datetime.strptime(self.get(MetaDataConstants.RETURN_BY), "%Y-%m-%d")

    @staticmethod
    def is_valid(token):
        for value in MetaDataStore.VALUES_FOR_VALIDATION:
            if value not in token:
                return False, value
        return True, ""
