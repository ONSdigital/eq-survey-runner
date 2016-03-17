from flask.ext.login import UserMixin

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

VALUES_FOR_VALIDATION = [USER_ID, RU_REF, RU_NAME, EQ_ID, COLLECTION_EXERCISE_SID, PERIOD_ID, PERIOD_STR,
                         REF_P_END_DATE, REF_P_START_DATE, FORM_TYPE, RETURN_BY]


class User(UserMixin):
    def __init__(self, jwt):
        self.id = jwt.get(USER_ID)
        self.jwt = jwt

    def get_user_id(self):
        return self.jwt.get(USER_ID)

    def get_ru_ref(self):
        return self.jwt.get(RU_REF)

    def get_ru_name(self):
        return self.jwt.get(RU_NAME)

    def get_eq_id(self):
        return self.jwt.get(EQ_ID)

    def get_collection_exercise_sid(self):
        return self.jwt.get(COLLECTION_EXERCISE_SID)

    def get_period_id(self):
        return self.jwt.get(PERIOD_ID)

    def get_period_str(self):
        return self.jwt.get(PERIOD_STR)

    def get_form_type(self):
        return self.jwt.get(FORM_TYPE)

    def get_ref_p_start_date(self):
        return self.jwt.get(REF_P_START_DATE)

    def get_ref_p_end_date(self):
        return self.jwt.get(REF_P_END_DATE)

    def get_trad_as(self):
        return self.jwt.get(TRAD_AS)

    def get_return_by(self):
        return self.jwt.get(RETURN_BY)

    def is_valid(self):
        for value in VALUES_FOR_VALIDATION:
            if not self._has_value(value):
                return False, value
        return True, ""

    def _has_value(self, value):
        return value in self.jwt
