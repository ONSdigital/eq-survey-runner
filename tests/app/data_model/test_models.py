from datetime import datetime, timedelta

from dateutil.tz import tzutc

from app.data_model.models import EQSession, QuestionnaireState, UsedJtiClaim
from tests.app.app_context_test_case import AppContextTestCase


class TestModels(AppContextTestCase):

    def test_questionnaire_state(self):
        original, new = self._make_models(QuestionnaireState, ['someuser', 'somedata', 1])

        self.assertEqual(original, new)

    def test_eq_session(self):
        expires_at = datetime.now(tz=tzutc()) + timedelta(seconds=5)
        original, new = self._make_models(EQSession, ['sessionid', 'someuser', 'somedata', expires_at])

        self.assertEqual(original, new)

    def test_used_jti_claim(self):
        original, new = self._make_models(UsedJtiClaim, ['claimid', datetime.now()])

        self.assertEqual(original, new)

    @staticmethod
    def _make_models(model_type, args):
        orig = model_type(*args)
        new = model_type.from_app_model(orig.to_app_model())
        orig_dict = orig.__dict__
        del orig_dict['_sa_instance_state']
        new_dict = new.__dict__
        del new_dict['_sa_instance_state']

        return orig_dict, new_dict
