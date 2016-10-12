import unittest
from app.data_model.questionnaire_store import QuestionnaireStore


class TestQuestionnaireStore(unittest.TestCase):

    def test_anonymous_user_throws_error(self):
        with self.assertRaises(ValueError) as ite:
            QuestionnaireStore(None, None)
            self.assertIn("No user_id or user_ik found in session", ite.exception.value)

