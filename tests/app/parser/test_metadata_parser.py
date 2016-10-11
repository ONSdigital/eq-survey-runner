import unittest

from app.authentication.invalid_token_exception import InvalidTokenException
from app.parser.metadata_parser import MetadataConstants
from app.parser.metadata_parser import MetadataParser
from tests.app.framework.sr_unittest import SurveyRunnerTestCase


class TestMetadataParser(SurveyRunnerTestCase):

    def setUp(self):
        super().setUp()
        self.jwt = {
            MetadataConstants.USER_ID.claim_id: "1",
            MetadataConstants.FORM_TYPE.claim_id: "a",
            MetadataConstants.COLLECTION_EXERCISE_SID.claim_id: "test-sid",
            MetadataConstants.EQ_ID.claim_id: "2",
            MetadataConstants.PERIOD_ID.claim_id: "3",
            MetadataConstants.PERIOD_STR.claim_id: "2016-01-01",
            MetadataConstants.REF_P_START_DATE.claim_id: "2016-02-02",
            MetadataConstants.REF_P_END_DATE.claim_id: "2016-03-03",
            MetadataConstants.RU_REF.claim_id: "2016-04-04",
            MetadataConstants.RU_NAME.claim_id: "Apple",
            MetadataConstants.RETURN_BY.claim_id: "2016-07-07",
            MetadataConstants.TRANSACTION_ID.claim_id: "4ec3aa9e-e8ac-4c8d-9793-6ed88b957c2f"
        }
        with self.application.test_request_context():
            self.metadata_store = MetadataParser.build_metadata(self.jwt)

    def test_transaction_id(self):
        with self.application.test_request_context():
            self.assertEqual(self.jwt.get(MetadataConstants.TRANSACTION_ID.claim_id), self.metadata_store.tx_id)

    def test_form_type(self):
        with self.application.test_request_context():
            self.assertEquals(self.jwt.get(MetadataConstants.FORM_TYPE.claim_id), self.metadata_store.form_type)

    def test_collection_id(self):
        with self.application.test_request_context():
            self.assertEquals(self.jwt.get(MetadataConstants.COLLECTION_EXERCISE_SID.claim_id), self.metadata_store.collection_exercise_sid)

    def test_get_eq_id(self):
        with self.application.test_request_context():
            self.assertEquals(self.jwt.get(MetadataConstants.EQ_ID.claim_id), self.metadata_store.eq_id)

    def test_get_period_id(self):
        with self.application.test_request_context():
            self.assertEquals(self.jwt.get(MetadataConstants.PERIOD_ID.claim_id), self.metadata_store.period_id)

    def test_get_period_str(self):
        with self.application.test_request_context():
            self.assertEquals(self.jwt.get(MetadataConstants.PERIOD_STR.claim_id), self.metadata_store.period_str)

    def test_ref_p_start_date(self):
        with self.application.test_request_context():
            self.assertEquals(self.jwt.get(MetadataConstants.REF_P_START_DATE.claim_id), self.metadata_store.ref_p_start_date.strftime('%Y-%m-%d'))

    def test_ref_p_end_date(self):
        with self.application.test_request_context():
            self.assertEquals(self.jwt.get(MetadataConstants.REF_P_END_DATE.claim_id), self.metadata_store.ref_p_end_date.strftime('%Y-%m-%d'))

    def test_ru_ref(self):
        with self.application.test_request_context():
            self.assertEquals(self.jwt.get(MetadataConstants.REF_P_END_DATE.claim_id), self.metadata_store.ref_p_end_date.strftime('%Y-%m-%d'))

    def test_is_valid(self):
        with self.application.test_request_context():
            self.assertTrue(MetadataParser.is_valid(self.jwt))

    def test_is_valid_fails_missing_user_id(self):
        jwt = {
            MetadataConstants.FORM_TYPE.claim_id: "a",
            MetadataConstants.COLLECTION_EXERCISE_SID.claim_id: "test-sid",
            MetadataConstants.EQ_ID.claim_id: "2",
            MetadataConstants.PERIOD_ID.claim_id: "3",
            MetadataConstants.PERIOD_STR.claim_id: "2016-01-01",
            MetadataConstants.REF_P_START_DATE.claim_id: "2016-02-02",
            MetadataConstants.REF_P_END_DATE.claim_id: "2016-03-03",
            MetadataConstants.RU_REF.claim_id: "2016-04-04",
            MetadataConstants.RU_NAME.claim_id: "Apple",
            MetadataConstants.RETURN_BY.claim_id: "2016-07-07"
        }
        valid, reason = MetadataParser.is_valid(jwt)
        self.assertFalse(valid)
        self.assertEquals(MetadataConstants.USER_ID.claim_id, reason)

    def test_is_valid_fails_missing_form_type(self):
        jwt = {
            MetadataConstants.USER_ID.claim_id: "1",
            MetadataConstants.FORM_TYPE.claim_id: "a",
            MetadataConstants.COLLECTION_EXERCISE_SID.claim_id: "test-sid",
            MetadataConstants.EQ_ID.claim_id: "2",
            MetadataConstants.PERIOD_ID.claim_id: "3",
            MetadataConstants.PERIOD_STR.claim_id: "2016-01-01",
            MetadataConstants.REF_P_START_DATE.claim_id: "2016-02-02",
            MetadataConstants.REF_P_END_DATE.claim_id: "2016-03-03",
            MetadataConstants.RU_REF.claim_id: "2016-04-04",
            MetadataConstants.RU_NAME.claim_id: "Apple",
            MetadataConstants.RETURN_BY.claim_id: "2016-07-07"
        }
        valid, reason = MetadataParser.is_valid(jwt)
        self.assertFalse(valid)
        self.assertEquals(MetadataConstants.FORM_TYPE.claim_id, reason)

    def test_is_valid_fails_missing_form_type(self):
        jwt = {
            MetadataConstants.USER_ID.claim_id: "1",
            MetadataConstants.COLLECTION_EXERCISE_SID.claim_id: "test-sid",
            MetadataConstants.EQ_ID.claim_id: "2",
            MetadataConstants.PERIOD_ID.claim_id: "3",
            MetadataConstants.PERIOD_STR.claim_id: "2016-01-01",
            MetadataConstants.REF_P_START_DATE.claim_id: "2016-02-02",
            MetadataConstants.REF_P_END_DATE.claim_id: "2016-03-03",
            MetadataConstants.RU_REF.claim_id: "2016-04-04",
            MetadataConstants.RU_NAME.claim_id: "Apple",
            MetadataConstants.RETURN_BY.claim_id: "2016-07-07"
        }
        valid, reason = MetadataParser.is_valid(jwt)
        self.assertFalse(valid)
        self.assertEquals(MetadataConstants.FORM_TYPE.claim_id, reason)

    def test_is_valid_fails_missing_collection_exercise_sid(self):
        jwt = {
            MetadataConstants.USER_ID.claim_id: "1",
            MetadataConstants.FORM_TYPE.claim_id: "a",
            MetadataConstants.EQ_ID.claim_id: "2",
            MetadataConstants.PERIOD_ID.claim_id: "3",
            MetadataConstants.PERIOD_STR.claim_id: "2016-01-01",
            MetadataConstants.REF_P_START_DATE.claim_id: "2016-02-02",
            MetadataConstants.REF_P_END_DATE.claim_id: "2016-03-03",
            MetadataConstants.RU_REF.claim_id: "2016-04-04",
            MetadataConstants.RU_NAME.claim_id: "Apple",
            MetadataConstants.RETURN_BY.claim_id: "2016-07-07"
        }
        valid, reason = MetadataParser.is_valid(jwt)
        self.assertFalse(valid)
        self.assertEquals(MetadataConstants.COLLECTION_EXERCISE_SID.claim_id, reason)

    def test_is_valid_fails_missing_eq_id(self):
        jwt = {
            MetadataConstants.USER_ID.claim_id: "1",
            MetadataConstants.FORM_TYPE.claim_id: "a",
            MetadataConstants.COLLECTION_EXERCISE_SID.claim_id: "test-sid",
            MetadataConstants.PERIOD_ID.claim_id: "3",
            MetadataConstants.PERIOD_STR.claim_id: "2016-01-01",
            MetadataConstants.REF_P_START_DATE.claim_id: "2016-02-02",
            MetadataConstants.REF_P_END_DATE.claim_id: "2016-03-03",
            MetadataConstants.RU_REF.claim_id: "2016-04-04",
            MetadataConstants.RU_NAME.claim_id: "Apple",
            MetadataConstants.RETURN_BY.claim_id: "2016-07-07"
        }
        valid, reason = MetadataParser.is_valid(jwt)
        self.assertFalse(valid)
        self.assertEquals(MetadataConstants.EQ_ID.claim_id, reason)

    def test_is_valid_fails_missing_period_id(self):
        jwt = {
            MetadataConstants.USER_ID.claim_id: "1",
            MetadataConstants.FORM_TYPE.claim_id: "a",
            MetadataConstants.COLLECTION_EXERCISE_SID.claim_id: "test-sid",
            MetadataConstants.EQ_ID.claim_id: "2",
            MetadataConstants.PERIOD_STR.claim_id: "2016-01-01",
            MetadataConstants.REF_P_START_DATE.claim_id: "2016-02-02",
            MetadataConstants.REF_P_END_DATE.claim_id: "2016-03-03",
            MetadataConstants.RU_REF.claim_id: "2016-04-04",
            MetadataConstants.RU_NAME.claim_id: "Apple",
            MetadataConstants.RETURN_BY.claim_id: "2016-07-07"
        }
        valid, reason = MetadataParser.is_valid(jwt)
        self.assertFalse(valid)
        self.assertEquals(MetadataConstants.PERIOD_ID.claim_id, reason)

    def test_is_valid_fails_missing_period_str(self):
        jwt = {
            MetadataConstants.USER_ID.claim_id: "1",
            MetadataConstants.FORM_TYPE.claim_id: "a",
            MetadataConstants.COLLECTION_EXERCISE_SID.claim_id: "test-sid",
            MetadataConstants.EQ_ID.claim_id: "2",
            MetadataConstants.PERIOD_ID.claim_id: "3",
            MetadataConstants.REF_P_START_DATE.claim_id: "2016-02-02",
            MetadataConstants.REF_P_END_DATE.claim_id: "2016-03-03",
            MetadataConstants.RU_REF.claim_id: "2016-04-04",
            MetadataConstants.RU_NAME.claim_id: "Apple",
            MetadataConstants.RETURN_BY.claim_id: "2016-07-07"
        }
        valid, reason = MetadataParser.is_valid(jwt)
        self.assertFalse(valid)
        self.assertEquals(MetadataConstants.PERIOD_STR.claim_id, reason)

    def test_is_valid_fails_missing_ref_p_start_date(self):
        jwt = {
            MetadataConstants.USER_ID.claim_id: "1",
            MetadataConstants.FORM_TYPE.claim_id: "a",
            MetadataConstants.COLLECTION_EXERCISE_SID.claim_id: "test-sid",
            MetadataConstants.EQ_ID.claim_id: "2",
            MetadataConstants.PERIOD_ID.claim_id: "3",
            MetadataConstants.PERIOD_STR.claim_id: "2016-01-01",
            MetadataConstants.REF_P_END_DATE.claim_id: "2016-03-03",
            MetadataConstants.RU_REF.claim_id: "2016-04-04",
            MetadataConstants.RU_NAME.claim_id: "Apple",
            MetadataConstants.RETURN_BY.claim_id: "2016-07-07"
        }
        valid, reason = MetadataParser.is_valid(jwt)
        self.assertFalse(valid)
        self.assertEquals(MetadataConstants.REF_P_START_DATE.claim_id, reason)

    def test_is_valid_fails_invalid_ref_p_start_date(self):
        jwt = {
            MetadataConstants.USER_ID.claim_id: "1",
            MetadataConstants.FORM_TYPE.claim_id: "a",
            MetadataConstants.COLLECTION_EXERCISE_SID.claim_id: "test-sid",
            MetadataConstants.EQ_ID.claim_id: "2",
            MetadataConstants.PERIOD_ID.claim_id: "3",
            MetadataConstants.PERIOD_STR.claim_id: "2016-01-01",
            MetadataConstants.REF_P_START_DATE.claim_id: "2016-13-31",
            MetadataConstants.REF_P_END_DATE.claim_id: "2016-03-03",
            MetadataConstants.RU_REF.claim_id: "2016-04-04",
            MetadataConstants.RU_NAME.claim_id: "Apple",
            MetadataConstants.RETURN_BY.claim_id: "2016-07-07"
        }
        valid, reason = MetadataParser.is_valid(jwt)
        self.assertTrue(valid)
        with self.assertRaises(InvalidTokenException) as ite:
            MetadataParser.build_metadata(jwt)
        self.assertIn("Incorrect data in token", ite.exception.value)

    def test_is_valid_fails_invalid_ref_p_end_date(self):
        jwt = {
            MetadataConstants.USER_ID.claim_id: "1",
            MetadataConstants.FORM_TYPE.claim_id: "a",
            MetadataConstants.COLLECTION_EXERCISE_SID.claim_id: "test-sid",
            MetadataConstants.EQ_ID.claim_id: "2",
            MetadataConstants.PERIOD_ID.claim_id: "3",
            MetadataConstants.PERIOD_STR.claim_id: "2016-01-01",
            MetadataConstants.REF_P_START_DATE.claim_id: "2016-12-31",
            MetadataConstants.REF_P_END_DATE.claim_id: "2016-04-31",
            MetadataConstants.RU_REF.claim_id: "2016-04-04",
            MetadataConstants.RU_NAME.claim_id: "Apple",
            MetadataConstants.RETURN_BY.claim_id: "2016-07-07"
        }
        valid, reason = MetadataParser.is_valid(jwt)
        self.assertTrue(valid)
        with self.assertRaises(InvalidTokenException) as ite:
            MetadataParser.build_metadata(jwt)
        self.assertIn("Incorrect data in token", ite.exception.value)

    def test_is_valid_fails_invalid_return_by(self):
        jwt = {
            MetadataConstants.USER_ID.claim_id: "1",
            MetadataConstants.FORM_TYPE.claim_id: "a",
            MetadataConstants.COLLECTION_EXERCISE_SID.claim_id: "test-sid",
            MetadataConstants.EQ_ID.claim_id: "2",
            MetadataConstants.PERIOD_ID.claim_id: "3",
            MetadataConstants.PERIOD_STR.claim_id: "2016-01-01",
            MetadataConstants.REF_P_START_DATE.claim_id: "2016-12-31",
            MetadataConstants.REF_P_END_DATE.claim_id: "2016-03-31",
            MetadataConstants.RU_REF.claim_id: "2016-04-04",
            MetadataConstants.RU_NAME.claim_id: "Apple",
            MetadataConstants.RETURN_BY.claim_id: "2016-09-31"
        }
        valid, reason = MetadataParser.is_valid(jwt)
        self.assertTrue(valid)
        with self.assertRaises(InvalidTokenException) as ite:
            MetadataParser.build_metadata(jwt)
        self.assertIn("Incorrect data in token", ite.exception.value)

    def test_is_valid_fails_missing_ref_p_end_date(self):
        jwt = {
            MetadataConstants.USER_ID.claim_id: "1",
            MetadataConstants.FORM_TYPE.claim_id: "a",
            MetadataConstants.COLLECTION_EXERCISE_SID.claim_id: "test-sid",
            MetadataConstants.EQ_ID.claim_id: "2",
            MetadataConstants.PERIOD_ID.claim_id: "3",
            MetadataConstants.PERIOD_STR.claim_id: "2016-01-01",
            MetadataConstants.REF_P_START_DATE.claim_id: "2016-02-02",
            MetadataConstants.RU_REF.claim_id: "2016-04-04",
            MetadataConstants.RU_NAME.claim_id: "Apple",
            MetadataConstants.RETURN_BY.claim_id: "2016-07-07"
        }
        valid, reason = MetadataParser.is_valid(jwt)
        self.assertFalse(valid)
        self.assertEquals(MetadataConstants.REF_P_END_DATE.claim_id, reason)

    def test_is_valid_fails_missing_ru_ref(self):
        jwt = {
            MetadataConstants.USER_ID.claim_id: "1",
            MetadataConstants.FORM_TYPE.claim_id: "a",
            MetadataConstants.COLLECTION_EXERCISE_SID.claim_id: "test-sid",
            MetadataConstants.EQ_ID.claim_id: "2",
            MetadataConstants.PERIOD_ID.claim_id: "3",
            MetadataConstants.PERIOD_STR.claim_id: "2016-01-01",
            MetadataConstants.REF_P_START_DATE.claim_id: "2016-02-02",
            MetadataConstants.REF_P_END_DATE.claim_id: "2016-03-03",
            MetadataConstants.RU_NAME.claim_id: "Apple",
            MetadataConstants.RETURN_BY.claim_id: "2016-07-07"
        }
        valid, reason = MetadataParser.is_valid(jwt)
        self.assertFalse(valid)
        self.assertEquals(MetadataConstants.RU_REF.claim_id, reason)

    def test_is_valid_fails_missing_ru_name(self):
        jwt = {
            MetadataConstants.USER_ID.claim_id: "1",
            MetadataConstants.FORM_TYPE.claim_id: "a",
            MetadataConstants.COLLECTION_EXERCISE_SID.claim_id: "test-sid",
            MetadataConstants.EQ_ID.claim_id: "2",
            MetadataConstants.PERIOD_ID.claim_id: "3",
            MetadataConstants.PERIOD_STR.claim_id: "2016-01-01",
            MetadataConstants.REF_P_START_DATE.claim_id: "2016-02-02",
            MetadataConstants.REF_P_END_DATE.claim_id: "2016-03-03",
            MetadataConstants.RU_REF.claim_id: "2016-04-04",
            MetadataConstants.RETURN_BY.claim_id: "2016-07-07"
        }
        valid, reason = MetadataParser.is_valid(jwt)
        self.assertFalse(valid)
        self.assertEquals(MetadataConstants.RU_NAME.claim_id, reason)

    def test_is_valid_fails_missing_return_by(self):
        jwt = {
            MetadataConstants.USER_ID.claim_id: "1",
            MetadataConstants.FORM_TYPE.claim_id: "a",
            MetadataConstants.COLLECTION_EXERCISE_SID.claim_id: "test-sid",
            MetadataConstants.EQ_ID.claim_id: "2",
            MetadataConstants.PERIOD_ID.claim_id: "3",
            MetadataConstants.PERIOD_STR.claim_id: "2016-01-01",
            MetadataConstants.REF_P_START_DATE.claim_id: "2016-02-02",
            MetadataConstants.REF_P_END_DATE.claim_id: "2016-03-03",
            MetadataConstants.RU_REF.claim_id: "2016-04-04",
            MetadataConstants.RU_NAME.claim_id: "Apple"
        }
        valid, reason = MetadataParser.is_valid(jwt)
        self.assertFalse(valid)
        self.assertEquals(MetadataConstants.RETURN_BY.claim_id, reason)

    def test_is_valid_does_not_fail_missing_optional_value_in_token(self):
        # tx_id, trad_as and employment_date are optional and might not be in the token
        jwt = {
            MetadataConstants.USER_ID.claim_id: "1",
            MetadataConstants.FORM_TYPE.claim_id: "a",
            MetadataConstants.COLLECTION_EXERCISE_SID.claim_id: "test-sid",
            MetadataConstants.EQ_ID.claim_id: "2",
            MetadataConstants.PERIOD_ID.claim_id: "3",
            MetadataConstants.PERIOD_STR.claim_id: "2016-01-01",
            MetadataConstants.REF_P_START_DATE.claim_id: "2016-02-02",
            MetadataConstants.REF_P_END_DATE.claim_id: "2016-03-03",
            MetadataConstants.RU_REF.claim_id: "2016-04-04",
            MetadataConstants.RU_NAME.claim_id: "Apple",
            MetadataConstants.RETURN_BY.claim_id: "2016-07-07"
        }
        valid, reason = MetadataParser.is_valid(jwt)
        self.assertTrue(valid)

    def test_invalid_tx_id(self):
        jwt = {
            MetadataConstants.USER_ID.claim_id: "1",
            MetadataConstants.FORM_TYPE.claim_id: "a",
            MetadataConstants.COLLECTION_EXERCISE_SID.claim_id: "test-sid",
            MetadataConstants.EQ_ID.claim_id: "2",
            MetadataConstants.PERIOD_ID.claim_id: "3",
            MetadataConstants.PERIOD_STR.claim_id: "2016-01-01",
            MetadataConstants.REF_P_START_DATE.claim_id: "2016-02-02",
            MetadataConstants.REF_P_END_DATE.claim_id: "2016-03-03",
            MetadataConstants.RU_REF.claim_id: "2016-04-04",
            MetadataConstants.RU_NAME.claim_id: "Apple",
            MetadataConstants.RETURN_BY.claim_id: "2016-07-07",
            # invalid
            MetadataConstants.TRANSACTION_ID.claim_id: "12121"
        }
        valid, reason = MetadataParser.is_valid(jwt)
        self.assertTrue(valid)
        with self.assertRaises(InvalidTokenException) as ite:
            MetadataParser.build_metadata(jwt)
        self.assertIn("Incorrect data in token", ite.exception.value)

    def test_malformed_tx_id(self):
        jwt = {
            MetadataConstants.USER_ID.claim_id: "1",
            MetadataConstants.FORM_TYPE.claim_id: "a",
            MetadataConstants.COLLECTION_EXERCISE_SID.claim_id: "test-sid",
            MetadataConstants.EQ_ID.claim_id: "2",
            MetadataConstants.PERIOD_ID.claim_id: "3",
            MetadataConstants.PERIOD_STR.claim_id: "2016-01-01",
            MetadataConstants.REF_P_START_DATE.claim_id: "2016-02-02",
            MetadataConstants.REF_P_END_DATE.claim_id: "2016-03-03",
            MetadataConstants.RU_REF.claim_id: "2016-04-04",
            MetadataConstants.RU_NAME.claim_id: "Apple",
            MetadataConstants.RETURN_BY.claim_id: "2016-07-07",
            # one character short
            MetadataConstants.TRANSACTION_ID.claim_id: "83a3db82-bea7-403c-a411-6357ff70f2f"
        }
        valid, reason = MetadataParser.is_valid(jwt)
        self.assertTrue(valid)
        with self.assertRaises(InvalidTokenException) as ite:
            MetadataParser.build_metadata(jwt)
        self.assertIn("Incorrect data in token", ite.exception.value)


if __name__ == '__main__':
    unittest.main()
