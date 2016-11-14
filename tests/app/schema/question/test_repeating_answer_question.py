import unittest

from mock import MagicMock

from app.schema.questions.repeating_answer_question import RepeatingAnswerQuestion


class TestRepeatingAnswerQuestion(unittest.TestCase):

    def test_construct_state_no_answer_returns_empty_state(self):
        question = RepeatingAnswerQuestion()
        state = question.construct_state({})
        self.assertIsNotNone(state)

    def test_construct_state_initial_state_contains_schema_answer(self):
        question = RepeatingAnswerQuestion()

        answer = MagicMock()
        question.answers.append(answer)

        state = question.construct_state({})
        self.assertEqual(len(state.answers), 1)
        self.assertEqual(state.answers[0].schema_item, answer)

    def test_construct_state_matches_answers_with_correct_id(self):
        question = RepeatingAnswerQuestion()

        answer = MagicMock()
        answer.id = 'person_name'
        question.answers.append(answer)

        post_data = {
          'person_name': 'Alice',
          'person_name_1': 'Bob',
          'irrelevant': 'Some value',
        }

        state = question.construct_state(post_data)
        self.assertEqual(len(state.answers), 2)

        post_data = {
          'person_name': 'Alice',
          'person_name_1': 'Bob',
          'person_name_2': 'Charles',
          'irrelevant': 'Some value',
        }

        state = question.construct_state(post_data)
        self.assertEqual(len(state.answers), 3)
