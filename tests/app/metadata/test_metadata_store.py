import unittest
from app.authentication.user import User
from app.authentication.invalid_token_exception import InvalidTokenException
from tests.app.framework.sr_unittest import SurveyRunnerTestCase
from app.data_model.metadata_store import MetaDataStore
from app.data_model.metadata_store import MetaDataConstants


class TestMetadataStore(SurveyRunnerTestCase):

    def setUp(self):
        super().setUp()
        self.jwt = {
            MetaDataConstants.USER_ID.claim_id: "1",
            MetaDataConstants.FORM_TYPE.claim_id: "a",
            MetaDataConstants.COLLECTION_EXERCISE_SID.claim_id: "test-sid",
            MetaDataConstants.EQ_ID.claim_id: "2",
            MetaDataConstants.PERIOD_ID.claim_id: "3",
            MetaDataConstants.PERIOD_STR.claim_id: "2016-01-01",
            MetaDataConstants.REF_P_START_DATE.claim_id: "2016-02-02",
            MetaDataConstants.REF_P_END_DATE.claim_id: "2016-03-03",
            MetaDataConstants.RU_REF.claim_id: "2016-04-04",
            MetaDataConstants.RU_NAME.claim_id: "Apple",
            MetaDataConstants.RETURN_BY.claim_id: "2016-07-07",
            MetaDataConstants.TRANSACTION_ID.claim_id: "4ec3aa9e-e8ac-4c8d-9793-6ed88b957c2f"
        }
        with self.application.test_request_context():
            user = User("1", "2")
            self.metadata_store = MetaDataStore.save_instance(user, self.jwt)

    def test_transaction_id(self):
        with self.application.test_request_context():
            self.assertEqual(self.jwt.get(MetaDataConstants.TRANSACTION_ID.claim_id), self.metadata_store.tx_id)

    def test_form_type(self):
        with self.application.test_request_context():
            self.assertEquals(self.jwt.get(MetaDataConstants.FORM_TYPE.claim_id), self.metadata_store.form_type)

    def test_collection_id(self):
        with self.application.test_request_context():
            self.assertEquals(self.jwt.get(MetaDataConstants.COLLECTION_EXERCISE_SID.claim_id), self.metadata_store.collection_exercise_sid)

    def test_get_eq_id(self):
        with self.application.test_request_context():
            self.assertEquals(self.jwt.get(MetaDataConstants.EQ_ID.claim_id), self.metadata_store.eq_id)

    def test_get_period_id(self):
        with self.application.test_request_context():
            self.assertEquals(self.jwt.get(MetaDataConstants.PERIOD_ID.claim_id), self.metadata_store.period_id)

    def test_get_period_str(self):
        with self.application.test_request_context():
            self.assertEquals(self.jwt.get(MetaDataConstants.PERIOD_STR.claim_id), self.metadata_store.period_str)

    def test_ref_p_start_date(self):
        with self.application.test_request_context():
            self.assertEquals(self.jwt.get(MetaDataConstants.REF_P_START_DATE.claim_id), self.metadata_store.ref_p_start_date.strftime('%Y-%m-%d'))

    def test_ref_p_end_date(self):
        with self.application.test_request_context():
            self.assertEquals(self.jwt.get(MetaDataConstants.REF_P_END_DATE.claim_id), self.metadata_store.ref_p_end_date.strftime('%Y-%m-%d'))

    def test_ru_ref(self):
        with self.application.test_request_context():
            self.assertEquals(self.jwt.get(MetaDataConstants.REF_P_END_DATE.claim_id), self.metadata_store.ref_p_end_date.strftime('%Y-%m-%d'))

    def test_is_valid(self):
        with self.application.test_request_context():
            self.assertTrue(MetaDataStore.is_valid(self.jwt))

    def test_is_valid_fails_missing_user_id(self):
        jwt = {
            MetaDataConstants.FORM_TYPE.claim_id: "a",
            MetaDataConstants.COLLECTION_EXERCISE_SID.claim_id: "test-sid",
            MetaDataConstants.EQ_ID.claim_id: "2",
            MetaDataConstants.PERIOD_ID.claim_id: "3",
            MetaDataConstants.PERIOD_STR.claim_id: "2016-01-01",
            MetaDataConstants.REF_P_START_DATE.claim_id: "2016-02-02",
            MetaDataConstants.REF_P_END_DATE.claim_id: "2016-03-03",
            MetaDataConstants.RU_REF.claim_id: "2016-04-04",
            MetaDataConstants.RU_NAME.claim_id: "Apple",
            MetaDataConstants.RETURN_BY.claim_id: "2016-07-07"
        }
        valid, reason = MetaDataStore.is_valid(jwt)
        self.assertFalse(valid)
        self.assertEquals(MetaDataConstants.USER_ID.claim_id, reason)

    def test_is_valid_fails_missing_form_type(self):
        jwt = {
            MetaDataConstants.USER_ID.claim_id: "1",
            MetaDataConstants.FORM_TYPE.claim_id: "a",
            MetaDataConstants.COLLECTION_EXERCISE_SID.claim_id: "test-sid",
            MetaDataConstants.EQ_ID.claim_id: "2",
            MetaDataConstants.PERIOD_ID.claim_id: "3",
            MetaDataConstants.PERIOD_STR.claim_id: "2016-01-01",
            MetaDataConstants.REF_P_START_DATE.claim_id: "2016-02-02",
            MetaDataConstants.REF_P_END_DATE.claim_id: "2016-03-03",
            MetaDataConstants.RU_REF.claim_id: "2016-04-04",
            MetaDataConstants.RU_NAME.claim_id: "Apple",
            MetaDataConstants.RETURN_BY.claim_id: "2016-07-07"
        }
        valid, reason = MetaDataStore.is_valid(jwt)
        self.assertFalse(valid)
        self.assertEquals(MetaDataConstants.FORM_TYPE.claim_id, reason)

    def test_is_valid_fails_missing_form_type(self):
        jwt = {
            MetaDataConstants.USER_ID.claim_id: "1",
            MetaDataConstants.COLLECTION_EXERCISE_SID.claim_id: "test-sid",
            MetaDataConstants.EQ_ID.claim_id: "2",
            MetaDataConstants.PERIOD_ID.claim_id: "3",
            MetaDataConstants.PERIOD_STR.claim_id: "2016-01-01",
            MetaDataConstants.REF_P_START_DATE.claim_id: "2016-02-02",
            MetaDataConstants.REF_P_END_DATE.claim_id: "2016-03-03",
            MetaDataConstants.RU_REF.claim_id: "2016-04-04",
            MetaDataConstants.RU_NAME.claim_id: "Apple",
            MetaDataConstants.RETURN_BY.claim_id: "2016-07-07"
        }
        valid, reason = MetaDataStore.is_valid(jwt)
        self.assertFalse(valid)
        self.assertEquals(MetaDataConstants.FORM_TYPE.claim_id, reason)

    def test_is_valid_fails_missing_collection_exercise_sid(self):
        jwt = {
            MetaDataConstants.USER_ID.claim_id: "1",
            MetaDataConstants.FORM_TYPE.claim_id: "a",
            MetaDataConstants.EQ_ID.claim_id: "2",
            MetaDataConstants.PERIOD_ID.claim_id: "3",
            MetaDataConstants.PERIOD_STR.claim_id: "2016-01-01",
            MetaDataConstants.REF_P_START_DATE.claim_id: "2016-02-02",
            MetaDataConstants.REF_P_END_DATE.claim_id: "2016-03-03",
            MetaDataConstants.RU_REF.claim_id: "2016-04-04",
            MetaDataConstants.RU_NAME.claim_id: "Apple",
            MetaDataConstants.RETURN_BY.claim_id: "2016-07-07"
        }
        valid, reason = MetaDataStore.is_valid(jwt)
        self.assertFalse(valid)
        self.assertEquals(MetaDataConstants.COLLECTION_EXERCISE_SID.claim_id, reason)

    def test_is_valid_fails_missing_eq_id(self):
        jwt = {
            MetaDataConstants.USER_ID.claim_id: "1",
            MetaDataConstants.FORM_TYPE.claim_id: "a",
            MetaDataConstants.COLLECTION_EXERCISE_SID.claim_id: "test-sid",
            MetaDataConstants.PERIOD_ID.claim_id: "3",
            MetaDataConstants.PERIOD_STR.claim_id: "2016-01-01",
            MetaDataConstants.REF_P_START_DATE.claim_id: "2016-02-02",
            MetaDataConstants.REF_P_END_DATE.claim_id: "2016-03-03",
            MetaDataConstants.RU_REF.claim_id: "2016-04-04",
            MetaDataConstants.RU_NAME.claim_id: "Apple",
            MetaDataConstants.RETURN_BY.claim_id: "2016-07-07"
        }
        valid, reason = MetaDataStore.is_valid(jwt)
        self.assertFalse(valid)
        self.assertEquals(MetaDataConstants.EQ_ID.claim_id, reason)

    def test_is_valid_fails_missing_period_id(self):
        jwt = {
            MetaDataConstants.USER_ID.claim_id: "1",
            MetaDataConstants.FORM_TYPE.claim_id: "a",
            MetaDataConstants.COLLECTION_EXERCISE_SID.claim_id: "test-sid",
            MetaDataConstants.EQ_ID.claim_id: "2",
            MetaDataConstants.PERIOD_STR.claim_id: "2016-01-01",
            MetaDataConstants.REF_P_START_DATE.claim_id: "2016-02-02",
            MetaDataConstants.REF_P_END_DATE.claim_id: "2016-03-03",
            MetaDataConstants.RU_REF.claim_id: "2016-04-04",
            MetaDataConstants.RU_NAME.claim_id: "Apple",
            MetaDataConstants.RETURN_BY.claim_id: "2016-07-07"
        }
        valid, reason = MetaDataStore.is_valid(jwt)
        self.assertFalse(valid)
        self.assertEquals(MetaDataConstants.PERIOD_ID.claim_id, reason)

    def test_is_valid_fails_missing_period_str(self):
        jwt = {
            MetaDataConstants.USER_ID.claim_id: "1",
            MetaDataConstants.FORM_TYPE.claim_id: "a",
            MetaDataConstants.COLLECTION_EXERCISE_SID.claim_id: "test-sid",
            MetaDataConstants.EQ_ID.claim_id: "2",
            MetaDataConstants.PERIOD_ID.claim_id: "3",
            MetaDataConstants.REF_P_START_DATE.claim_id: "2016-02-02",
            MetaDataConstants.REF_P_END_DATE.claim_id: "2016-03-03",
            MetaDataConstants.RU_REF.claim_id: "2016-04-04",
            MetaDataConstants.RU_NAME.claim_id: "Apple",
            MetaDataConstants.RETURN_BY.claim_id: "2016-07-07"
        }
        valid, reason = MetaDataStore.is_valid(jwt)
        self.assertFalse(valid)
        self.assertEquals(MetaDataConstants.PERIOD_STR.claim_id, reason)

    def test_is_valid_fails_missing_ref_p_start_date(self):
        jwt = {
            MetaDataConstants.USER_ID.claim_id: "1",
            MetaDataConstants.FORM_TYPE.claim_id: "a",
            MetaDataConstants.COLLECTION_EXERCISE_SID.claim_id: "test-sid",
            MetaDataConstants.EQ_ID.claim_id: "2",
            MetaDataConstants.PERIOD_ID.claim_id: "3",
            MetaDataConstants.PERIOD_STR.claim_id: "2016-01-01",
            MetaDataConstants.REF_P_END_DATE.claim_id: "2016-03-03",
            MetaDataConstants.RU_REF.claim_id: "2016-04-04",
            MetaDataConstants.RU_NAME.claim_id: "Apple",
            MetaDataConstants.RETURN_BY.claim_id: "2016-07-07"
        }
        valid, reason = MetaDataStore.is_valid(jwt)
        self.assertFalse(valid)
        self.assertEquals(MetaDataConstants.REF_P_START_DATE.claim_id, reason)

    def test_is_valid_fails_invalid_ref_p_start_date(self):
        jwt = {
            MetaDataConstants.USER_ID.claim_id: "1",
            MetaDataConstants.FORM_TYPE.claim_id: "a",
            MetaDataConstants.COLLECTION_EXERCISE_SID.claim_id: "test-sid",
            MetaDataConstants.EQ_ID.claim_id: "2",
            MetaDataConstants.PERIOD_ID.claim_id: "3",
            MetaDataConstants.PERIOD_STR.claim_id: "2016-01-01",
            MetaDataConstants.REF_P_START_DATE.claim_id: "2016-13-31",
            MetaDataConstants.REF_P_END_DATE.claim_id: "2016-03-03",
            MetaDataConstants.RU_REF.claim_id: "2016-04-04",
            MetaDataConstants.RU_NAME.claim_id: "Apple",
            MetaDataConstants.RETURN_BY.claim_id: "2016-07-07"
        }
        valid, reason = MetaDataStore.is_valid(jwt)
        self.assertTrue(valid)
        with self.assertRaises(InvalidTokenException) as ite:
            MetaDataStore.save_instance(User("1", "2"), jwt)
        self.assertIn("Incorrect data in token", ite.exception.value)

    def test_is_valid_fails_invalid_ref_p_end_date(self):
        jwt = {
            MetaDataConstants.USER_ID.claim_id: "1",
            MetaDataConstants.FORM_TYPE.claim_id: "a",
            MetaDataConstants.COLLECTION_EXERCISE_SID.claim_id: "test-sid",
            MetaDataConstants.EQ_ID.claim_id: "2",
            MetaDataConstants.PERIOD_ID.claim_id: "3",
            MetaDataConstants.PERIOD_STR.claim_id: "2016-01-01",
            MetaDataConstants.REF_P_START_DATE.claim_id: "2016-12-31",
            MetaDataConstants.REF_P_END_DATE.claim_id: "2016-04-31",
            MetaDataConstants.RU_REF.claim_id: "2016-04-04",
            MetaDataConstants.RU_NAME.claim_id: "Apple",
            MetaDataConstants.RETURN_BY.claim_id: "2016-07-07"
        }
        valid, reason = MetaDataStore.is_valid(jwt)
        self.assertTrue(valid)
        with self.assertRaises(InvalidTokenException) as ite:
            MetaDataStore.save_instance(User("1", "2"), jwt)
        self.assertIn("Incorrect data in token", ite.exception.value)

    def test_is_valid_fails_invalid_return_by(self):
        jwt = {
            MetaDataConstants.USER_ID.claim_id: "1",
            MetaDataConstants.FORM_TYPE.claim_id: "a",
            MetaDataConstants.COLLECTION_EXERCISE_SID.claim_id: "test-sid",
            MetaDataConstants.EQ_ID.claim_id: "2",
            MetaDataConstants.PERIOD_ID.claim_id: "3",
            MetaDataConstants.PERIOD_STR.claim_id: "2016-01-01",
            MetaDataConstants.REF_P_START_DATE.claim_id: "2016-12-31",
            MetaDataConstants.REF_P_END_DATE.claim_id: "2016-03-31",
            MetaDataConstants.RU_REF.claim_id: "2016-04-04",
            MetaDataConstants.RU_NAME.claim_id: "Apple",
            MetaDataConstants.RETURN_BY.claim_id: "2016-09-31"
        }
        valid, reason = MetaDataStore.is_valid(jwt)
        self.assertTrue(valid)
        with self.assertRaises(InvalidTokenException) as ite:
            MetaDataStore.save_instance(User("1", "2"), jwt)
        self.assertIn("Incorrect data in token", ite.exception.value)

    def test_is_valid_fails_missing_ref_p_end_date(self):
        jwt = {
            MetaDataConstants.USER_ID.claim_id: "1",
            MetaDataConstants.FORM_TYPE.claim_id: "a",
            MetaDataConstants.COLLECTION_EXERCISE_SID.claim_id: "test-sid",
            MetaDataConstants.EQ_ID.claim_id: "2",
            MetaDataConstants.PERIOD_ID.claim_id: "3",
            MetaDataConstants.PERIOD_STR.claim_id: "2016-01-01",
            MetaDataConstants.REF_P_START_DATE.claim_id: "2016-02-02",
            MetaDataConstants.RU_REF.claim_id: "2016-04-04",
            MetaDataConstants.RU_NAME.claim_id: "Apple",
            MetaDataConstants.RETURN_BY.claim_id: "2016-07-07"
        }
        valid, reason = MetaDataStore.is_valid(jwt)
        self.assertFalse(valid)
        self.assertEquals(MetaDataConstants.REF_P_END_DATE.claim_id, reason)

    def test_is_valid_fails_missing_ru_ref(self):
        jwt = {
            MetaDataConstants.USER_ID.claim_id: "1",
            MetaDataConstants.FORM_TYPE.claim_id: "a",
            MetaDataConstants.COLLECTION_EXERCISE_SID.claim_id: "test-sid",
            MetaDataConstants.EQ_ID.claim_id: "2",
            MetaDataConstants.PERIOD_ID.claim_id: "3",
            MetaDataConstants.PERIOD_STR.claim_id: "2016-01-01",
            MetaDataConstants.REF_P_START_DATE.claim_id: "2016-02-02",
            MetaDataConstants.REF_P_END_DATE.claim_id: "2016-03-03",
            MetaDataConstants.RU_NAME.claim_id: "Apple",
            MetaDataConstants.RETURN_BY.claim_id: "2016-07-07"
        }
        valid, reason = MetaDataStore.is_valid(jwt)
        self.assertFalse(valid)
        self.assertEquals(MetaDataConstants.RU_REF.claim_id, reason)

    def test_is_valid_fails_missing_ru_name(self):
        jwt = {
            MetaDataConstants.USER_ID.claim_id: "1",
            MetaDataConstants.FORM_TYPE.claim_id: "a",
            MetaDataConstants.COLLECTION_EXERCISE_SID.claim_id: "test-sid",
            MetaDataConstants.EQ_ID.claim_id: "2",
            MetaDataConstants.PERIOD_ID.claim_id: "3",
            MetaDataConstants.PERIOD_STR.claim_id: "2016-01-01",
            MetaDataConstants.REF_P_START_DATE.claim_id: "2016-02-02",
            MetaDataConstants.REF_P_END_DATE.claim_id: "2016-03-03",
            MetaDataConstants.RU_REF.claim_id: "2016-04-04",
            MetaDataConstants.RETURN_BY.claim_id: "2016-07-07"
        }
        valid, reason = MetaDataStore.is_valid(jwt)
        self.assertFalse(valid)
        self.assertEquals(MetaDataConstants.RU_NAME.claim_id, reason)

    def test_is_valid_fails_missing_return_by(self):
        jwt = {
            MetaDataConstants.USER_ID.claim_id: "1",
            MetaDataConstants.FORM_TYPE.claim_id: "a",
            MetaDataConstants.COLLECTION_EXERCISE_SID.claim_id: "test-sid",
            MetaDataConstants.EQ_ID.claim_id: "2",
            MetaDataConstants.PERIOD_ID.claim_id: "3",
            MetaDataConstants.PERIOD_STR.claim_id: "2016-01-01",
            MetaDataConstants.REF_P_START_DATE.claim_id: "2016-02-02",
            MetaDataConstants.REF_P_END_DATE.claim_id: "2016-03-03",
            MetaDataConstants.RU_REF.claim_id: "2016-04-04",
            MetaDataConstants.RU_NAME.claim_id: "Apple"
        }
        valid, reason = MetaDataStore.is_valid(jwt)
        self.assertFalse(valid)
        self.assertEquals(MetaDataConstants.RETURN_BY.claim_id, reason)

    def test_is_valid_does_not_fail_missing_optional_value_in_token(self):
        # tx_id, trad_as and employment_date are optional and might not be in the token
        jwt = {
            MetaDataConstants.USER_ID.claim_id: "1",
            MetaDataConstants.FORM_TYPE.claim_id: "a",
            MetaDataConstants.COLLECTION_EXERCISE_SID.claim_id: "test-sid",
            MetaDataConstants.EQ_ID.claim_id: "2",
            MetaDataConstants.PERIOD_ID.claim_id: "3",
            MetaDataConstants.PERIOD_STR.claim_id: "2016-01-01",
            MetaDataConstants.REF_P_START_DATE.claim_id: "2016-02-02",
            MetaDataConstants.REF_P_END_DATE.claim_id: "2016-03-03",
            MetaDataConstants.RU_REF.claim_id: "2016-04-04",
            MetaDataConstants.RU_NAME.claim_id: "Apple",
            MetaDataConstants.RETURN_BY.claim_id: "2016-07-07"
        }
        valid, reason = MetaDataStore.is_valid(jwt)
        self.assertTrue(valid)

    def test_invalid_tx_id(self):
        jwt = {
            MetaDataConstants.USER_ID.claim_id: "1",
            MetaDataConstants.FORM_TYPE.claim_id: "a",
            MetaDataConstants.COLLECTION_EXERCISE_SID.claim_id: "test-sid",
            MetaDataConstants.EQ_ID.claim_id: "2",
            MetaDataConstants.PERIOD_ID.claim_id: "3",
            MetaDataConstants.PERIOD_STR.claim_id: "2016-01-01",
            MetaDataConstants.REF_P_START_DATE.claim_id: "2016-02-02",
            MetaDataConstants.REF_P_END_DATE.claim_id: "2016-03-03",
            MetaDataConstants.RU_REF.claim_id: "2016-04-04",
            MetaDataConstants.RU_NAME.claim_id: "Apple",
            MetaDataConstants.RETURN_BY.claim_id: "2016-07-07",
            # invalid
            MetaDataConstants.TRANSACTION_ID.claim_id: "12121"
        }
        valid, reason = MetaDataStore.is_valid(jwt)
        self.assertTrue(valid)
        with self.assertRaises(InvalidTokenException) as ite:
            MetaDataStore.save_instance(User("1", "2"), jwt)
        self.assertIn("Incorrect data in token", ite.exception.value)

    def test_malformed_tx_id(self):
        jwt = {
            MetaDataConstants.USER_ID.claim_id: "1",
            MetaDataConstants.FORM_TYPE.claim_id: "a",
            MetaDataConstants.COLLECTION_EXERCISE_SID.claim_id: "test-sid",
            MetaDataConstants.EQ_ID.claim_id: "2",
            MetaDataConstants.PERIOD_ID.claim_id: "3",
            MetaDataConstants.PERIOD_STR.claim_id: "2016-01-01",
            MetaDataConstants.REF_P_START_DATE.claim_id: "2016-02-02",
            MetaDataConstants.REF_P_END_DATE.claim_id: "2016-03-03",
            MetaDataConstants.RU_REF.claim_id: "2016-04-04",
            MetaDataConstants.RU_NAME.claim_id: "Apple",
            MetaDataConstants.RETURN_BY.claim_id: "2016-07-07",
            # one character short
            MetaDataConstants.TRANSACTION_ID.claim_id: "83a3db82-bea7-403c-a411-6357ff70f2f"
        }
        valid, reason = MetaDataStore.is_valid(jwt)
        self.assertTrue(valid)
        with self.assertRaises(InvalidTokenException) as ite:
            MetaDataStore.save_instance(User("1", "2"), jwt)
        self.assertIn("Incorrect data in token", ite.exception.value)


if __name__ == '__main__':
    unittest.main()
