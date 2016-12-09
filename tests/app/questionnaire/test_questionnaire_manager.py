from unittest import TestCase

from mock import MagicMock, Mock, patch, call
from app.questionnaire.questionnaire_manager import QuestionnaireManager
from app.questionnaire_state.state_item import StateItem
from app.schema.section import Section
from app.schema.skip_condition import SkipCondition
from app.schema.when import When


def mock_answer(answer_id, answer_instance=0, question=MagicMock()):
    answer = MagicMock()
    answer.id = answer_id
    answer.answer_instance = answer_instance
    answer.parent = question
    answer.flatten = MagicMock(return_value=MagicMock())
    return answer


class TestQuestionnaireManager(TestCase):

    def setUp(self):
        # Override some behaviours that are difficult to mock.
        self.original_update_questionnaire_store = QuestionnaireManager.update_questionnaire_store

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
            answers.append(mock_answer('answer', i, self.question))

        self.answers = answers
        self.questionnaire_manager.state = MagicMock()
        self.questionnaire_manager.state.get_answers = MagicMock(return_value=self.answers)

    def tearDown(self):
        # Reset some behaviours.
        QuestionnaireManager.update_questionnaire_store = self.original_update_questionnaire_store

    def test_add_answer_creates_new_answer_state(self):
        # Given
        answer_schema = MagicMock()

        question_schema = MagicMock()
        question_schema.answers = [answer_schema]

        self.questionnaire_manager._schema.get_item_by_id = MagicMock(return_value=question_schema)
        self.questionnaire_manager._get_next_answer_instance = MagicMock(return_value=1)

        new_answer_state = MagicMock()
        self.questionnaire_manager._create_new_answer_state = MagicMock(return_value=new_answer_state)

        question_state = MagicMock()
        self.questionnaire_manager.state.find_state_item = MagicMock(return_value=question_state)

        # When
        self.questionnaire_manager.add_answer('block', 'question', self.answer_store)

        # Then
        question_state.create_new_answer_state.assert_called_with(answer_schema, 1)

    def test_add_answer_updates_answer_store(self):
        # Given
        question = MagicMock()
        self.questionnaire_manager.state.find_state_item = MagicMock(return_value=question)
        self.questionnaire_manager.update_questionnaire_store = MagicMock()

        # When
        self.questionnaire_manager.add_answer('block', 'question', self.answer_store)

        # Then
        self.questionnaire_manager.update_questionnaire_store.assert_called_with('block')

    def test_remove_answer_single_answer(self):
        # Given
        should_remove = mock_answer('answer', 0, self.question)
        answers = [should_remove]
        self.questionnaire_manager.state.get_answers = MagicMock(return_value=answers)
        self.question.remove_answer = Mock()

        # When
        self.questionnaire_manager.remove_answer('block', self.answer_store, 0)

        # Then
        self.question.remove_answer.assert_called_with(should_remove)

    def test_remove_answer_single_answer_multiple_instances(self):
        # Given
        answers = [
            mock_answer('answer', 0, self.question),
            mock_answer('answer', 1, self.question),
            mock_answer('answer', 2, self.question),
        ]
        self.questionnaire_manager.state.get_answers = MagicMock(return_value=answers)
        self.question.remove_answer = Mock()

        # When
        self.questionnaire_manager.remove_answer('block', self.answer_store, 1)

        # Then
        self.question.remove_answer.assert_called_with(answers[1])

    def test_remove_answer_multiple_answer_single_instance(self):
        # Given
        answers = [
            mock_answer('first', 0, self.question),
            mock_answer('middle', 0, self.question),
            mock_answer('last', 0, self.question)
        ]
        self.questionnaire_manager.state.get_answers = MagicMock(return_value=answers)
        self.question.remove_answer = Mock()

        # When
        self.questionnaire_manager.remove_answer('block', self.answer_store, 0)

        # Then
        calls = [
            call(answers[0]), call(answers[1]), call(answers[2])
        ]
        self.question.remove_answer.assert_has_calls(calls)

    def test_remove_answer_multiple_answer_multiple_instances(self):
        # Given
        answers = [
            mock_answer('first', 0, self.question),
            mock_answer('middle', 0, self.question),
            mock_answer('last', 0, self.question),
            mock_answer('first', 1, self.question),
            mock_answer('middle', 1, self.question),
            mock_answer('last', 1, self.question),
        ]
        self.questionnaire_manager.state.get_answers = MagicMock(return_value=answers)
        self.question.remove_answer = Mock()

        # When
        self.questionnaire_manager.remove_answer('block', self.answer_store, 1)

        # Then
        calls = [
            call(answers[3]), call(answers[4]), call(answers[5])
        ]
        self.question.remove_answer.assert_has_calls(calls)

    def test_get_next_answer_instance_no_previous_answers(self):
        # Given
        qm = self.questionnaire_manager
        answer_store = MagicMock()
        answer_schema = MagicMock()
        answers = []
        answer_store.filter = MagicMock(return_value=answers)

        # When
        next_id = qm._get_next_answer_instance(answer_store, answer_schema)

        # Then
        self.assertEqual(next_id, 0)

    def test_get_next_answer_instance_one_previous_answer(self):
        # Given
        qm = self.questionnaire_manager
        answer_store = MagicMock()
        answer_schema = MagicMock()
        answers = [{'answer_instance': '0'}]
        answer_store.filter = MagicMock(return_value=answers)

        # When
        next_id = qm._get_next_answer_instance(answer_store, answer_schema)

        # Then
        self.assertEqual(next_id, 1)

    def test_get_next_answer_instance_two_previous_answers(self):
        # Given
        qm = self.questionnaire_manager
        answer_store = MagicMock()
        answer_schema = MagicMock()
        answers = [{'answer_instance': '0'}, {'answer_instance': '1'}]
        answer_store.filter = MagicMock(return_value=answers)

        # When
        next_id = qm._get_next_answer_instance(answer_store, answer_schema)

        # Then
        self.assertEqual(next_id, 2)

    def test_get_next_answer_instance_one_more_than_previous_answers(self):
        # Given
        qm = self.questionnaire_manager
        answer_store = MagicMock()
        answer_schema = MagicMock()
        answers = [{'answer_instance': '5'}]
        answer_store.filter = MagicMock(return_value=answers)

        # When
        next_id = qm._get_next_answer_instance(answer_store, answer_schema)

        # Then
        self.assertEqual(next_id, 6)

    def test_conditional_display_skips_when_equals(self):

        with patch('app.globals.get_answer_store') as get_answer_store:
            answers = {'12345': 'yes'}
            get_answer_store().map = Mock(return_value=answers)

            skip = SkipCondition()
            skip.when = When()

            skip.when.id = '12345'
            skip.when.condition = 'equals'
            skip.when.value = 'yes'

            section = Section()
            section.skip_condition = skip

            state_item = StateItem(id='', schema_item=section)

            self.questionnaire_manager._conditional_display(state_item)

            self.assertEqual(state_item.skipped, True)

    def test_conditional_display_skips_when_not_equals(self):

        with patch('app.globals.get_answer_store') as get_answer_store:
            answers = {'12345': 'yes'}
            get_answer_store().map = Mock(return_value=answers)

            skip = SkipCondition()
            skip.when = When()

            skip.when.id = '12345'
            skip.when.condition = 'not equals'
            skip.when.value = 'no'

            section = Section()
            section.skip_condition = skip

            state_item = StateItem(id='', schema_item=section)

            self.questionnaire_manager._conditional_display(state_item)

            self.assertEqual(state_item.skipped, True)
