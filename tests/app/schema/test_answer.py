from unittest import TestCase

from mock import MagicMock

from app.schema.answer import Answer


class TestSchemaAnswer(TestCase):

    def test_create_new_answer_state_sets_answer_instance(self):
        # Given
        answer_schema = Answer('answer_id')
        answer_schema.widget = MagicMock()
        answer_schema.widget.name = 'answer_id'
        question = MagicMock()

        # When
        new_answer_state = answer_schema.create_new_answer_state(answer_instance=1, parent=question)

        # Then
        self.assertEqual(new_answer_state.answer_instance, 1)
        question.children.append.assert_called_with(new_answer_state)
