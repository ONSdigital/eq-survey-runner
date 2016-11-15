from unittest import TestCase

from app.templating.summary.answer import Answer


class TestAnswer(TestCase):

    def test_create_answer(self):
        # Given
        answer_schema = {'id': 'answer_1', 'label': 'answer_label', 'type': 'date'}
        user_answer = 'An answer'

        # When
        answer = Answer(answer_schema, user_answer)

        # Then
        self.assertEqual(answer.id, 'answer_1')
        self.assertEqual(answer.label, 'answer_label')
        self.assertEqual(answer.value, user_answer)

    def test_date_answer_type(self):
        # Given
        answer_schema = {'id': 'answer_1', 'label': '', 'type': 'date'}
        user_answer = None

        # When
        answer = Answer(answer_schema, user_answer)

        # Then
        self.assertEqual(answer.type, 'date')
