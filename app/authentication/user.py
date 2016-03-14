from flask.ext.login import UserMixin

USER_ID = 'user_id'
RU_REF = 'ru_ref'
EQ_ID = 'eq-id'
COLLECTION_EXERCISE_SID = 'collection_exercise_sid'
PERIOD_ID = 'period_id'
PERIOD_STR = 'period_str'
REF_P_START_DATE = 'ref_p_start_date'
REF_P_END_DATE = 'ref_p_end_date'
FORM_TYPE = 'form_type'


class User(UserMixin):
    def __init__(self, jwt):
        self.id = jwt.get(USER_ID) or None
        self.jwt = jwt

    def get_user_id(self):
        return self.jwt.get(USER_ID)

    def get_ru_ref(self):
        return self.jwt.get(RU_REF)

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
