from app.data_model.models import QuestionnaireState
from tests.app.app_context_test_case import AppContextTestCase


class TestModels(AppContextTestCase):

    def test_questionnaire_state(self):
        questionnaire_state_args = [
            'someuser',
            'somedata',
            1,
            'some_collection_exercise_id',
            'some_form_type',
            'some_ru_ref',
            'some_eq_id']

        original, new = self._make_models(QuestionnaireState, questionnaire_state_args)

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
