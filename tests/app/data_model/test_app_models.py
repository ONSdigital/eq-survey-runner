import datetime

from dateutil.tz import tzutc

from app.data_model.app_models import EQSession, QuestionnaireState, UsedJtiClaim, SubmittedResponse
from app.storage.dynamodb_api import TABLE_CONFIG
from tests.app.app_context_test_case import AppContextTestCase


NOW = datetime.datetime.now(tz=tzutc()).replace(microsecond=0)


class TestAppModels(AppContextTestCase):

    def test_submitted_response(self):
        self._test_model(SubmittedResponse('txid', 'somedata', NOW))

    def test_questionnaire_state(self):
        new = self._test_model(QuestionnaireState('someuser', 'somedata', 1))
        self.assertGreaterEqual(new.created_at, NOW)
        self.assertGreaterEqual(new.updated_at, NOW)

    def test_eq_session(self):
        new = self._test_model(EQSession('sessionid', 'someuser', 'somedata'))
        self.assertGreaterEqual(new.created_at, NOW)
        self.assertGreaterEqual(new.updated_at, NOW)

    def test_used_jti_claim(self):
        self._test_model(UsedJtiClaim('claimid', NOW, NOW))

    def _test_model(self, orig):
        config = TABLE_CONFIG[type(orig)]
        schema = config['schema'](strict=True)

        item, _ = schema.dump(orig)
        new, _ = schema.load(item)
        self.assertEqual(orig.__dict__, new.__dict__)
        return new
