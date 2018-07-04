import datetime

from app.data_model.models import EQSession, QuestionnaireState, UsedJtiClaim
from tests.app.app_context_test_case import AppContextTestCase


class TestModels(AppContextTestCase):

    def test_questionnaire_state(self):
        self._test_model(QuestionnaireState, ['someuser', 'somedata', 1])

    def test_eq_session(self):
        self._test_model(EQSession, ['sessionid', 'someuser', 'somedata'])

    def test_used_jti_claim(self):
        self._test_model(UsedJtiClaim, ['claimid', datetime.datetime.now()])

    def _test_model(self, model_type, args):
        orig = model_type(*args)
        new = model_type.from_app_model(orig.to_app_model())
        orig_dict = orig.__dict__
        del orig_dict['_sa_instance_state']
        new_dict = new.__dict__
        del new_dict['_sa_instance_state']
        self.assertEqual(orig_dict, new_dict)
