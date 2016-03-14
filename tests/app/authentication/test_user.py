import unittest
from app.authentication.user import User, FORM_TYPE, COLLECTION_EXERCISE_SID, EQ_ID, PERIOD_ID, PERIOD_STR, REF_P_END_DATE, REF_P_START_DATE, RU_REF, USER_ID


class TestUser(unittest.TestCase):

    def setUp(self):
        self.jwt = {
            USER_ID: "1",
            FORM_TYPE: "a",
            COLLECTION_EXERCISE_SID: "test-sid",
            EQ_ID: "2",
            PERIOD_ID: "3",
            PERIOD_STR: "2016-01-01",
            REF_P_START_DATE: "2016-02-02",
            REF_P_END_DATE: "2016-03-03",
            RU_REF: "2016-04-04"
        }
        self.user = User(self.jwt)

    def test_get_user_id(self):
        self.assertEquals(self.jwt.get(USER_ID), self.user.get_user_id())


    def test_form_type(self):
        self.assertEquals(self.jwt.get(FORM_TYPE), self.user.get_form_type())


if __name__ == '__main__':
    unittest.main()
