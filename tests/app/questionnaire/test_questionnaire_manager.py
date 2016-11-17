from unittest import TestCase

from mock import MagicMock, patch
from app.questionnaire.questionnaire_manager import QuestionnaireManager, Navigator


class TestQuestionnaireManager(TestCase):

    def test_add_answer_adds_answer_to_question(self):
        # Given
        new_answer = MagicMock()
        self.questionnaire_manager._create_new_answer_state = MagicMock(return_value=new_answer)

        question = MagicMock()
        self.questionnaire_manager.state.find_state_item = MagicMock(return_value=question)

        # When
        self.questionnaire_manager.add_answer('block', 'question', self.answer_store)
        question.answers.append.assert_called_with(new_answer)

    def test_add_answer_updates_answer_store(self):
        # Given
        question = MagicMock()
        self.questionnaire_manager.state.find_state_item = MagicMock(return_value=question)
        self.questionnaire_manager.update_questionnaire_store = MagicMock()

        # When
        self.questionnaire_manager.add_answer('block', 'question', self.answer_store)

        # Then
        self.questionnaire_manager.update_questionnaire_store.assert_called_with('block')

    def test_remove_answer_detaches_answer_from_question(self):
        post_data = {
            'action[remove_answer]': '1',
        }

        answer_to_remove = self.answers[1]

        with patch.object(self.question, 'remove_answer') as mock:
            self.questionnaire_manager.remove_answer('block', post_data, self.answer_store)
            mock.assert_called_with(answer_to_remove)

    def test_remove_answer_removes_from_answer_store(self):
        post_data = {
            'action[remove_answer]': '1',
        }

        answer_to_remove = self.answers[1]
        flattened_answer = answer_to_remove.flatten()

        with patch.object(self.answer_store, 'remove') as mock:
            self.questionnaire_manager.remove_answer('block', post_data, self.answer_store)
            mock.assert_called_with(flattened_answer)

    def test_create_new_answer_no_previous_answers(self):
        # Given
        answer_schema = MagicMock()
        answer_schema.widget.name = 'answer'

        answer_state = MagicMock()
        answer_state.schema_item = answer_schema

        answer_schema.construct_state = MagicMock(return_value=answer_state)
        question_state = MagicMock()


        # When
        new_answer = self.questionnaire_manager._create_new_answer_state(answer_schema, question_state, self.answer_store)

        # Then
        self.assertEqual(new_answer.schema_item.widget.name, 'answer_0')
        self.assertEqual(new_answer.answer_instance, 0)

    def test_create_new_answer_with_existing_answers(self):
        # Given
        answer_schema = MagicMock()
        answer_schema.widget.name = 'answer'

        answer_state = MagicMock()
        answer_state.schema_item = answer_schema

        answer_schema.construct_state = MagicMock(return_value=answer_state)
        question_state = MagicMock()

        existing_answers = [{
            'answer_id': 'answer',
            'answer_instance': '0',
        },
        {
            'answer_id': 'answer',
            'answer_instance': '1',
        }]

        self.answer_store.filter = MagicMock(return_value=existing_answers)
        # When
        new_answer = self.questionnaire_manager._create_new_answer_state(answer_schema, question_state, self.answer_store)

        # Then
        self.assertEqual(new_answer.schema_item.widget.name, 'answer_2')
        self.assertEqual(new_answer.answer_instance, 2)

    def setUp(self):
        # Override some behaviours that are difficult to mock.
        self.original_Navigator_init = Navigator.__init__
        self.original_update_questionnaire_store = QuestionnaireManager.update_questionnaire_store

        Navigator.__init__ = MagicMock(return_value=None)
        QuestionnaireManager.update_questionnaire_store = MagicMock(return_value=None)

        # Class under test.
        self.questionnaire_manager = QuestionnaireManager(MagicMock(), MagicMock())

        # Mock answer store.
        answer_store = MagicMock()
        answer_store.filter = MagicMock(return_value=[])
        self.answer_store = answer_store

        # Mock question.
        self.question = MagicMock()

        # Mock answers.
        answers = []
        for i in range(3):
            answer = MagicMock()
            answer.parent = self.question
            answer.id = i
            answer.flatten = MagicMock(return_value=MagicMock())
            answers.append(answer)

        self.answers = answers
        self.questionnaire_manager.state = MagicMock()
        self.questionnaire_manager.state.get_answers = MagicMock(return_value=self.answers)

    def tearDown(self):
        # Reset some behaviours.
        Navigator.__init__ = self.original_Navigator_init
        QuestionnaireManager.update_questionnaire_store = self.original_update_questionnaire_store
