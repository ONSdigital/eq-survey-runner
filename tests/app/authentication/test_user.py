import unittest
from app.authentication.user import User, UserConstants


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
            RU_REF: "2016-04-04",
            RU_NAME: "Apple",
            RETURN_BY: "2016-07-07"
        }
        self.user = User(self.jwt)

    def test_get_user_id(self):
        self.assertEquals(self.jwt.get(UserConstants.USER_ID), self.user.get_user_id())

    def test_form_type(self):
        self.assertEquals(self.jwt.get(UserConstants.FORM_TYPE), self.user.get_form_type())

    def test_collection_id(self):
        self.assertEquals(self.jwt.get(UserConstants.COLLECTION_EXERCISE_SID), self.user.get_collection_exercise_sid())

    def test_get_eq_id(self):
        self.assertEquals(self.jwt.get(UserConstants.EQ_ID), self.user.get_eq_id())

    def test_get_period_id(self):
        self.assertEquals(self.jwt.get(UserConstants.PERIOD_ID), self.user.get_period_id())

    def test_get_period_str(self):
        self.assertEquals(self.jwt.get(UserConstants.PERIOD_STR), self.user.get_period_str())

    def test_ref_p_start_date(self):
        self.assertEquals(self.jwt.get(UserConstants.REF_P_START_DATE), self.user.get_ref_p_start_date())

    def test_ref_p_end_date(self):
        self.assertEquals(self.jwt.get(UserConstants.REF_P_END_DATE), self.user.get_ref_p_end_date())

    def test_ru_ref(self):
        self.assertEquals(self.jwt.get(UserConstants.REF_P_END_DATE), self.user.get_ref_p_end_date())

    def test_is_valid(self):
        self.assertTrue(self.user.is_valid()[0])

    def test_is_valid_fails_missing_user_id(self):
        user = User({
            UserConstants.FORM_TYPE: "a",
            UserConstants.COLLECTION_EXERCISE_SID: "test-sid",
            UserConstants.EQ_ID: "2",
            UserConstants.PERIOD_ID: "3",
            UserConstants.PERIOD_STR: "2016-01-01",
            UserConstants.REF_P_START_DATE: "2016-02-02",
            UserConstants.REF_P_END_DATE: "2016-03-03",
            UserConstants.RU_REF: "2016-04-04",
            UserConstants.RU_NAME: "Apple",
            UserConstants.RETURN_BY: "2016-07-07"
        })
        valid, reason = user.is_valid()
        self.assertFalse(valid)
        self.assertEquals(UserConstants.USER_ID, reason)

    def test_is_valid_fails_missing_form_type(self):
        user = User({
            UserConstants.USER_ID: "1",
            UserConstants.FORM_TYPE: "a",
            UserConstants.COLLECTION_EXERCISE_SID: "test-sid",
            UserConstants.EQ_ID: "2",
            UserConstants.PERIOD_ID: "3",
            UserConstants.PERIOD_STR: "2016-01-01",
            UserConstants.REF_P_START_DATE: "2016-02-02",
            UserConstants.REF_P_END_DATE: "2016-03-03",
            UserConstants.RU_REF: "2016-04-04",
            UserConstants.RU_NAME: "Apple",
            UserConstants.RETURN_BY: "2016-07-07"
        })
        valid, reason = user.is_valid()
        self.assertFalse(valid)
        self.assertEquals(UserConstants.FORM_TYPE, reason)

    def test_is_valid_fails_missing_form_type(self):
        user = User({
            UserConstants.USER_ID: "1",
            UserConstants.COLLECTION_EXERCISE_SID: "test-sid",
            UserConstants.EQ_ID: "2",
            UserConstants.PERIOD_ID: "3",
            UserConstants.PERIOD_STR: "2016-01-01",
            UserConstants.REF_P_START_DATE: "2016-02-02",
            UserConstants.REF_P_END_DATE: "2016-03-03",
            UserConstants.RU_REF: "2016-04-04",
            UserConstants.RU_NAME: "Apple",
            UserConstants.RETURN_BY: "2016-07-07"
        })
        valid, reason = user.is_valid()
        self.assertFalse(valid)
        self.assertEquals(UserConstants.FORM_TYPE, reason)

    def test_is_valid_fails_missing_collection_exercise_sid(self):
        user = User({
            UserConstants.USER_ID: "1",
            UserConstants.FORM_TYPE: "a",
            UserConstants.EQ_ID: "2",
            UserConstants.PERIOD_ID: "3",
            UserConstants.PERIOD_STR: "2016-01-01",
            UserConstants.REF_P_START_DATE: "2016-02-02",
            UserConstants.REF_P_END_DATE: "2016-03-03",
            UserConstants.RU_REF: "2016-04-04",
            UserConstants.RU_NAME: "Apple",
            UserConstants.RETURN_BY: "2016-07-07"
        })
        valid, reason = user.is_valid()
        self.assertFalse(valid)
        self.assertEquals(UserConstants.COLLECTION_EXERCISE_SID, reason)

    def test_is_valid_fails_missing_eq_id(self):
        user = User({
            UserConstants.USER_ID: "1",
            UserConstants.FORM_TYPE: "a",
            UserConstants.COLLECTION_EXERCISE_SID: "test-sid",
            UserConstants.PERIOD_ID: "3",
            UserConstants.PERIOD_STR: "2016-01-01",
            UserConstants.REF_P_START_DATE: "2016-02-02",
            UserConstants.REF_P_END_DATE: "2016-03-03",
            UserConstants.RU_REF: "2016-04-04",
            UserConstants.RU_NAME: "Apple",
            UserConstants.RETURN_BY: "2016-07-07"
        })
        valid, reason = user.is_valid()
        self.assertFalse(valid)
        self.assertEquals(UserConstants.EQ_ID, reason)

    def test_is_valid_fails_missing_period_id(self):
        user = User({
            UserConstants.USER_ID: "1",
            UserConstants.FORM_TYPE: "a",
            UserConstants.COLLECTION_EXERCISE_SID: "test-sid",
            UserConstants.EQ_ID: "2",
            UserConstants.PERIOD_STR: "2016-01-01",
            UserConstants.REF_P_START_DATE: "2016-02-02",
            UserConstants.REF_P_END_DATE: "2016-03-03",
            UserConstants.RU_REF: "2016-04-04",
            UserConstants.RU_NAME: "Apple",
            UserConstants.RETURN_BY: "2016-07-07"
        })
        valid, reason = user.is_valid()
        self.assertFalse(valid)
        self.assertEquals(UserConstants.PERIOD_ID, reason)

    def test_is_valid_fails_missing_period_str(self):
        user = User({
            UserConstants.USER_ID: "1",
            UserConstants.FORM_TYPE: "a",
            UserConstants.COLLECTION_EXERCISE_SID: "test-sid",
            UserConstants.EQ_ID: "2",
            UserConstants.PERIOD_ID: "3",
            UserConstants.REF_P_START_DATE: "2016-02-02",
            UserConstants.REF_P_END_DATE: "2016-03-03",
            UserConstants.RU_REF: "2016-04-04",
            UserConstants.RU_NAME: "Apple",
            UserConstants.RETURN_BY: "2016-07-07"
        })
        valid, reason = user.is_valid()
        self.assertFalse(valid)
        self.assertEquals(UserConstants.PERIOD_STR, reason)

    def test_is_valid_fails_missing_ref_p_start_date(self):
        user = User({
            UserConstants.USER_ID: "1",
            UserConstants.FORM_TYPE: "a",
            UserConstants.COLLECTION_EXERCISE_SID: "test-sid",
            UserConstants.EQ_ID: "2",
            UserConstants.PERIOD_ID: "3",
            UserConstants.PERIOD_STR: "2016-01-01",
            UserConstants.REF_P_END_DATE: "2016-03-03",
            UserConstants.RU_REF: "2016-04-04",
            UserConstants.RU_NAME: "Apple",
            UserConstants.RETURN_BY: "2016-07-07"
        })
        valid, reason = user.is_valid()
        self.assertFalse(valid)
        self.assertEquals(UserConstants.REF_P_START_DATE, reason)

    def test_is_valid_fails_missing_ref_p_end_date(self):
        user = User({
            UserConstants.USER_ID: "1",
            UserConstants.FORM_TYPE: "a",
            UserConstants.COLLECTION_EXERCISE_SID: "test-sid",
            UserConstants.EQ_ID: "2",
            UserConstants.PERIOD_ID: "3",
            UserConstants.PERIOD_STR: "2016-01-01",
            UserConstants.REF_P_START_DATE: "2016-02-02",
            UserConstants.RU_REF: "2016-04-04",
            UserConstants.RU_NAME: "Apple",
            UserConstants.RETURN_BY: "2016-07-07"
        })
        valid, reason = user.is_valid()
        self.assertFalse(valid)
        self.assertEquals(UserConstants.REF_P_END_DATE, reason)

    def test_is_valid_fails_missing_ru_ref(self):
        user = User({
            UserConstants.USER_ID: "1",
            UserConstants.FORM_TYPE: "a",
            UserConstants.COLLECTION_EXERCISE_SID: "test-sid",
            UserConstants.EQ_ID: "2",
            UserConstants.PERIOD_ID: "3",
            UserConstants.PERIOD_STR: "2016-01-01",
            UserConstants.REF_P_START_DATE: "2016-02-02",
            UserConstants.REF_P_END_DATE: "2016-03-03",
            UserConstants.RU_NAME: "Apple",
            UserConstants.RETURN_BY: "2016-07-07"
        })
        valid, reason = user.is_valid()
        self.assertFalse(valid)
        self.assertEquals(UserConstants.RU_REF, reason)

    def test_is_valid_fails_missing_ru_name(self):
        user = User({
            UserConstants.USER_ID: "1",
            UserConstants.FORM_TYPE: "a",
            UserConstants.COLLECTION_EXERCISE_SID: "test-sid",
            UserConstants.EQ_ID: "2",
            UserConstants.PERIOD_ID: "3",
            UserConstants.PERIOD_STR: "2016-01-01",
            UserConstants.REF_P_START_DATE: "2016-02-02",
            UserConstants.REF_P_END_DATE: "2016-03-03",
            UserConstants.RU_REF: "2016-04-04",
            UserConstants.RETURN_BY: "2016-07-07"
        })
        valid, reason = user.is_valid()
        self.assertFalse(valid)
        self.assertEquals(UserConstants.RU_NAME, reason)

    def test_is_valid_fails_missing_return_by(self):
        user = User({
            UserConstants.USER_ID: "1",
            UserConstants.FORM_TYPE: "a",
            UserConstants.COLLECTION_EXERCISE_SID: "test-sid",
            UserConstants.EQ_ID: "2",
            UserConstants.PERIOD_ID: "3",
            UserConstants.PERIOD_STR: "2016-01-01",
            UserConstants.REF_P_START_DATE: "2016-02-02",
            UserConstants.REF_P_END_DATE: "2016-03-03",
            UserConstants.RU_REF: "2016-04-04",
            UserConstants.RU_NAME: "Apple"
        })
        valid, reason = user.is_valid()
        self.assertFalse(valid)
        self.assertEquals(UserConstants.RETURN_BY, reason)

    def test_is_valid_does_not_fail_missing_trading_name(self):
        user = User({
            UserConstants.USER_ID: "1",
            UserConstants.FORM_TYPE: "a",
            UserConstants.COLLECTION_EXERCISE_SID: "test-sid",
            UserConstants.EQ_ID: "2",
            UserConstants.PERIOD_ID: "3",
            UserConstants.PERIOD_STR: "2016-01-01",
            UserConstants.REF_P_START_DATE: "2016-02-02",
            UserConstants.REF_P_END_DATE: "2016-03-03",
            UserConstants.RU_REF: "2016-04-04",
            UserConstants.RU_NAME: "Apple",
            UserConstants.RETURN_BY: "2016-07-07"
        })
        valid, reason = user.is_valid()
        self.assertTrue(valid)

if __name__ == '__main__':
    unittest.main()
