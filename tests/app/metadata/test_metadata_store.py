import unittest
from app.authentication.user import User
from tests.app.framework.sr_unittest import SurveyRunnerTestCase
from app.metadata.metadata_store import MetaDataStore
from app.metadata.metadata_store import MetaDataConstants


class TestMetadataStore(SurveyRunnerTestCase):

    def setUp(self):
        super().setUp()
        self.jwt = {
            MetaDataConstants.USER_ID: "1",
            MetaDataConstants.FORM_TYPE: "a",
            MetaDataConstants.COLLECTION_EXERCISE_SID: "test-sid",
            MetaDataConstants.EQ_ID: "2",
            MetaDataConstants.PERIOD_ID: "3",
            MetaDataConstants.PERIOD_STR: "2016-01-01",
            MetaDataConstants.REF_P_START_DATE: "2016-02-02",
            MetaDataConstants.REF_P_END_DATE: "2016-03-03",
            MetaDataConstants.RU_REF: "2016-04-04",
            MetaDataConstants.RU_NAME: "Apple",
            MetaDataConstants.RETURN_BY: "2016-07-07"
        }
        with self.application.test_request_context():
            user = User("1")
            self.metadata_store = MetaDataStore(user)
            self.metadata_store.store_all(self.jwt)

    def test_form_type(self):
        with self.application.test_request_context():
            self.assertEquals(self.jwt.get(MetaDataConstants.FORM_TYPE), self.metadata_store.get_form_type())

    def test_collection_id(self):
        with self.application.test_request_context():
            self.assertEquals(self.jwt.get(MetaDataConstants.COLLECTION_EXERCISE_SID), self.metadata_store.get_collection_exercise_sid())

    def test_get_eq_id(self):
        with self.application.test_request_context():
            self.assertEquals(self.jwt.get(MetaDataConstants.EQ_ID), self.metadata_store.get_eq_id())

    def test_get_period_id(self):
        with self.application.test_request_context():
            self.assertEquals(self.jwt.get(MetaDataConstants.PERIOD_ID), self.metadata_store.get_period_id())

    def test_get_period_str(self):
        with self.application.test_request_context():
            self.assertEquals(self.jwt.get(MetaDataConstants.PERIOD_STR), self.metadata_store.get_period_str())

    def test_ref_p_start_date(self):
        with self.application.test_request_context():
            self.assertEquals(self.jwt.get(MetaDataConstants.REF_P_START_DATE), self.metadata_store.get_ref_p_start_date())

    def test_ref_p_end_date(self):
        with self.application.test_request_context():
            self.assertEquals(self.jwt.get(MetaDataConstants.REF_P_END_DATE), self.metadata_store.get_ref_p_end_date())

    def test_ru_ref(self):
        with self.application.test_request_context():
            self.assertEquals(self.jwt.get(MetaDataConstants.REF_P_END_DATE), self.metadata_store.get_ref_p_end_date())

    def test_is_valid(self):
        with self.application.test_request_context():
            self.assertTrue(MetaDataStore.is_valid(self.jwt))

    def test_is_valid_fails_missing_user_id(self):
        jwt = {
            MetaDataConstants.FORM_TYPE: "a",
            MetaDataConstants.COLLECTION_EXERCISE_SID: "test-sid",
            MetaDataConstants.EQ_ID: "2",
            MetaDataConstants.PERIOD_ID: "3",
            MetaDataConstants.PERIOD_STR: "2016-01-01",
            MetaDataConstants.REF_P_START_DATE: "2016-02-02",
            MetaDataConstants.REF_P_END_DATE: "2016-03-03",
            MetaDataConstants.RU_REF: "2016-04-04",
            MetaDataConstants.RU_NAME: "Apple",
            MetaDataConstants.RETURN_BY: "2016-07-07"
        }
        valid, reason = MetaDataStore.is_valid(jwt)
        self.assertFalse(valid)
        self.assertEquals(MetaDataConstants.USER_ID, reason)

    def test_is_valid_fails_missing_form_type(self):
        jwt = {
            MetaDataConstants.USER_ID: "1",
            MetaDataConstants.FORM_TYPE: "a",
            MetaDataConstants.COLLECTION_EXERCISE_SID: "test-sid",
            MetaDataConstants.EQ_ID: "2",
            MetaDataConstants.PERIOD_ID: "3",
            MetaDataConstants.PERIOD_STR: "2016-01-01",
            MetaDataConstants.REF_P_START_DATE: "2016-02-02",
            MetaDataConstants.REF_P_END_DATE: "2016-03-03",
            MetaDataConstants.RU_REF: "2016-04-04",
            MetaDataConstants.RU_NAME: "Apple",
            MetaDataConstants.RETURN_BY: "2016-07-07"
        }
        valid, reason = MetaDataStore.is_valid(jwt)
        self.assertFalse(valid)
        self.assertEquals(MetaDataConstants.FORM_TYPE, reason)

    def test_is_valid_fails_missing_form_type(self):
        jwt = {
            MetaDataConstants.USER_ID: "1",
            MetaDataConstants.COLLECTION_EXERCISE_SID: "test-sid",
            MetaDataConstants.EQ_ID: "2",
            MetaDataConstants.PERIOD_ID: "3",
            MetaDataConstants.PERIOD_STR: "2016-01-01",
            MetaDataConstants.REF_P_START_DATE: "2016-02-02",
            MetaDataConstants.REF_P_END_DATE: "2016-03-03",
            MetaDataConstants.RU_REF: "2016-04-04",
            MetaDataConstants.RU_NAME: "Apple",
            MetaDataConstants.RETURN_BY: "2016-07-07"
        }
        valid, reason = MetaDataStore.is_valid(jwt)
        self.assertFalse(valid)
        self.assertEquals(MetaDataConstants.FORM_TYPE, reason)

    def test_is_valid_fails_missing_collection_exercise_sid(self):
        jwt = {
            MetaDataConstants.USER_ID: "1",
            MetaDataConstants.FORM_TYPE: "a",
            MetaDataConstants.EQ_ID: "2",
            MetaDataConstants.PERIOD_ID: "3",
            MetaDataConstants.PERIOD_STR: "2016-01-01",
            MetaDataConstants.REF_P_START_DATE: "2016-02-02",
            MetaDataConstants.REF_P_END_DATE: "2016-03-03",
            MetaDataConstants.RU_REF: "2016-04-04",
            MetaDataConstants.RU_NAME: "Apple",
            MetaDataConstants.RETURN_BY: "2016-07-07"
        }
        valid, reason = MetaDataStore.is_valid(jwt)
        self.assertFalse(valid)
        self.assertEquals(MetaDataConstants.COLLECTION_EXERCISE_SID, reason)

    def test_is_valid_fails_missing_eq_id(self):
        jwt = {
            MetaDataConstants.USER_ID: "1",
            MetaDataConstants.FORM_TYPE: "a",
            MetaDataConstants.COLLECTION_EXERCISE_SID: "test-sid",
            MetaDataConstants.PERIOD_ID: "3",
            MetaDataConstants.PERIOD_STR: "2016-01-01",
            MetaDataConstants.REF_P_START_DATE: "2016-02-02",
            MetaDataConstants.REF_P_END_DATE: "2016-03-03",
            MetaDataConstants.RU_REF: "2016-04-04",
            MetaDataConstants.RU_NAME: "Apple",
            MetaDataConstants.RETURN_BY: "2016-07-07"
        }
        valid, reason = MetaDataStore.is_valid(jwt)
        self.assertFalse(valid)
        self.assertEquals(MetaDataConstants.EQ_ID, reason)

    def test_is_valid_fails_missing_period_id(self):
        jwt = {
            MetaDataConstants.USER_ID: "1",
            MetaDataConstants.FORM_TYPE: "a",
            MetaDataConstants.COLLECTION_EXERCISE_SID: "test-sid",
            MetaDataConstants.EQ_ID: "2",
            MetaDataConstants.PERIOD_STR: "2016-01-01",
            MetaDataConstants.REF_P_START_DATE: "2016-02-02",
            MetaDataConstants.REF_P_END_DATE: "2016-03-03",
            MetaDataConstants.RU_REF: "2016-04-04",
            MetaDataConstants.RU_NAME: "Apple",
            MetaDataConstants.RETURN_BY: "2016-07-07"
        }
        valid, reason = MetaDataStore.is_valid(jwt)
        self.assertFalse(valid)
        self.assertEquals(MetaDataConstants.PERIOD_ID, reason)

    def test_is_valid_fails_missing_period_str(self):
        jwt = {
            MetaDataConstants.USER_ID: "1",
            MetaDataConstants.FORM_TYPE: "a",
            MetaDataConstants.COLLECTION_EXERCISE_SID: "test-sid",
            MetaDataConstants.EQ_ID: "2",
            MetaDataConstants.PERIOD_ID: "3",
            MetaDataConstants.REF_P_START_DATE: "2016-02-02",
            MetaDataConstants.REF_P_END_DATE: "2016-03-03",
            MetaDataConstants.RU_REF: "2016-04-04",
            MetaDataConstants.RU_NAME: "Apple",
            MetaDataConstants.RETURN_BY: "2016-07-07"
        }
        valid, reason = MetaDataStore.is_valid(jwt)
        self.assertFalse(valid)
        self.assertEquals(MetaDataConstants.PERIOD_STR, reason)

    def test_is_valid_fails_missing_ref_p_start_date(self):
        jwt = {
            MetaDataConstants.USER_ID: "1",
            MetaDataConstants.FORM_TYPE: "a",
            MetaDataConstants.COLLECTION_EXERCISE_SID: "test-sid",
            MetaDataConstants.EQ_ID: "2",
            MetaDataConstants.PERIOD_ID: "3",
            MetaDataConstants.PERIOD_STR: "2016-01-01",
            MetaDataConstants.REF_P_END_DATE: "2016-03-03",
            MetaDataConstants.RU_REF: "2016-04-04",
            MetaDataConstants.RU_NAME: "Apple",
            MetaDataConstants.RETURN_BY: "2016-07-07"
        }
        valid, reason = MetaDataStore.is_valid(jwt)
        self.assertFalse(valid)
        self.assertEquals(MetaDataConstants.REF_P_START_DATE, reason)

    def test_is_valid_fails_missing_ref_p_end_date(self):
        jwt = {
            MetaDataConstants.USER_ID: "1",
            MetaDataConstants.FORM_TYPE: "a",
            MetaDataConstants.COLLECTION_EXERCISE_SID: "test-sid",
            MetaDataConstants.EQ_ID: "2",
            MetaDataConstants.PERIOD_ID: "3",
            MetaDataConstants.PERIOD_STR: "2016-01-01",
            MetaDataConstants.REF_P_START_DATE: "2016-02-02",
            MetaDataConstants.RU_REF: "2016-04-04",
            MetaDataConstants.RU_NAME: "Apple",
            MetaDataConstants.RETURN_BY: "2016-07-07"
        }
        valid, reason = MetaDataStore.is_valid(jwt)
        self.assertFalse(valid)
        self.assertEquals(MetaDataConstants.REF_P_END_DATE, reason)

    def test_is_valid_fails_missing_ru_ref(self):
        jwt = {
            MetaDataConstants.USER_ID: "1",
            MetaDataConstants.FORM_TYPE: "a",
            MetaDataConstants.COLLECTION_EXERCISE_SID: "test-sid",
            MetaDataConstants.EQ_ID: "2",
            MetaDataConstants.PERIOD_ID: "3",
            MetaDataConstants.PERIOD_STR: "2016-01-01",
            MetaDataConstants.REF_P_START_DATE: "2016-02-02",
            MetaDataConstants.REF_P_END_DATE: "2016-03-03",
            MetaDataConstants.RU_NAME: "Apple",
            MetaDataConstants.RETURN_BY: "2016-07-07"
        }
        valid, reason = MetaDataStore.is_valid(jwt)
        self.assertFalse(valid)
        self.assertEquals(MetaDataConstants.RU_REF, reason)

    def test_is_valid_fails_missing_ru_name(self):
        jwt = {
            MetaDataConstants.USER_ID: "1",
            MetaDataConstants.FORM_TYPE: "a",
            MetaDataConstants.COLLECTION_EXERCISE_SID: "test-sid",
            MetaDataConstants.EQ_ID: "2",
            MetaDataConstants.PERIOD_ID: "3",
            MetaDataConstants.PERIOD_STR: "2016-01-01",
            MetaDataConstants.REF_P_START_DATE: "2016-02-02",
            MetaDataConstants.REF_P_END_DATE: "2016-03-03",
            MetaDataConstants.RU_REF: "2016-04-04",
            MetaDataConstants.RETURN_BY: "2016-07-07"
        }
        valid, reason = MetaDataStore.is_valid(jwt)
        self.assertFalse(valid)
        self.assertEquals(MetaDataConstants.RU_NAME, reason)

    def test_is_valid_fails_missing_return_by(self):
        jwt = {
            MetaDataConstants.USER_ID: "1",
            MetaDataConstants.FORM_TYPE: "a",
            MetaDataConstants.COLLECTION_EXERCISE_SID: "test-sid",
            MetaDataConstants.EQ_ID: "2",
            MetaDataConstants.PERIOD_ID: "3",
            MetaDataConstants.PERIOD_STR: "2016-01-01",
            MetaDataConstants.REF_P_START_DATE: "2016-02-02",
            MetaDataConstants.REF_P_END_DATE: "2016-03-03",
            MetaDataConstants.RU_REF: "2016-04-04",
            MetaDataConstants.RU_NAME: "Apple"
        }
        valid, reason = MetaDataStore.is_valid(jwt)
        self.assertFalse(valid)
        self.assertEquals(MetaDataConstants.RETURN_BY, reason)

    def test_is_valid_does_not_fail_missing_trading_name(self):
        jwt = {
            MetaDataConstants.USER_ID: "1",
            MetaDataConstants.FORM_TYPE: "a",
            MetaDataConstants.COLLECTION_EXERCISE_SID: "test-sid",
            MetaDataConstants.EQ_ID: "2",
            MetaDataConstants.PERIOD_ID: "3",
            MetaDataConstants.PERIOD_STR: "2016-01-01",
            MetaDataConstants.REF_P_START_DATE: "2016-02-02",
            MetaDataConstants.REF_P_END_DATE: "2016-03-03",
            MetaDataConstants.RU_REF: "2016-04-04",
            MetaDataConstants.RU_NAME: "Apple",
            MetaDataConstants.RETURN_BY: "2016-07-07"
        }
        valid, reason = MetaDataStore.is_valid(jwt)
        self.assertTrue(valid)

if __name__ == '__main__':
    unittest.main()
