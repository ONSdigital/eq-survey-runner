from flask.ext.login import UserMixin


class UserConstants(object):
    """Constant for user values"""
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


class User(UserMixin):

    VALUES_FOR_VALIDATION = [UserConstants.USER_ID, UserConstants.RU_REF, UserConstants.RU_NAME, UserConstants.EQ_ID,
                             UserConstants.COLLECTION_EXERCISE_SID, UserConstants.PERIOD_ID, UserConstants.PERIOD_STR,
                             UserConstants.REF_P_END_DATE, UserConstants.REF_P_START_DATE, UserConstants.FORM_TYPE,
                             UserConstants.RETURN_BY]

    def __init__(self, jwt):
        self.id = jwt.get(UserConstants.USER_ID)
        self.jwt = jwt

    def get_user_id(self):
        return self.jwt.get(UserConstants.USER_ID)

    def get_ru_ref(self):
        return self.jwt.get(UserConstants.RU_REF)

    def get_ru_name(self):
        return self.jwt.get(UserConstants.RU_NAME)

    def get_eq_id(self):
        return self.jwt.get(UserConstants.EQ_ID)

    def get_collection_exercise_sid(self):
        return self.jwt.get(UserConstants.COLLECTION_EXERCISE_SID)

    def get_period_id(self):
        return self.jwt.get(UserConstants.PERIOD_ID)

    def get_period_str(self):
        return self.jwt.get(UserConstants.PERIOD_STR)

    def get_form_type(self):
        return self.jwt.get(UserConstants.FORM_TYPE)

    def get_ref_p_start_date(self):
        return self.jwt.get(UserConstants.REF_P_START_DATE)

    def get_ref_p_end_date(self):
        return self.jwt.get(UserConstants.REF_P_END_DATE)

    def get_trad_as(self):
        return self.jwt.get(UserConstants.TRAD_AS)

    def get_return_by(self):
        return self.jwt.get(UserConstants.RETURN_BY)

    def is_valid(self):
        for value in User.VALUES_FOR_VALIDATION:
            if not self._has_value(value):
                return False, value
        return True, ""

    def _has_value(self, value):
        return value in self.jwt
