from unittest import TestCase

from mock import MagicMock

from app.questionnaire_state.state_answer import StateAnswer
from app.schema.answer import Answer


class TestSchemaAnswer(TestCase):

    def test_create_new_answer_state_when_no_answer_state(self):
        # Given
        answer_schema = Answer('answer_id')
        answer_schema.widget = MagicMock()
        answer_schema.widget.name = 'answer_id'

        # When
        new_answer_state = answer_schema.create_new_answer_state([], answer_instance=1)

        # Then
        self.assertEqual(new_answer_state.answer_instance, 1)
        self.assertEqual(new_answer_state.id, answer_schema.id)
        self.assertEqual(new_answer_state.schema_item.widget.name, 'answer_id_1')

    def test_create_new_answer_state_when_answer_state_exists(self):
        # Given
        answer_schema = Answer('answer_id')
        answer_schema.widget = MagicMock()
        answer_schema.widget.name = 'answer_id'

        answer1 = StateAnswer('answer_id', answer_schema)

        # When
        new_answer_state = answer_schema.create_new_answer_state([answer1], answer_instance=2)

        # Then
        self.assertEqual(new_answer_state.answer_instance, 2)
        self.assertEqual(new_answer_state.id, answer_schema.id)
        self.assertEqual(new_answer_state.schema_item.widget.name, 'answer_id_2')

    def test_no_new_answer_state_when_answer_state_exists(self):
        # Given
        answer_schema = Answer('answer_id')
        answer_schema.widget = MagicMock()
        answer_schema.widget.name = 'answer_id'

        answer1 = StateAnswer('answer_id', answer_schema)
        answer1.answer_instance = 1

        # When
        new_answer_state = answer_schema.create_new_answer_state([answer1], answer_instance=1)

        # Then
        self.assertIsNone(new_answer_state)

    def test_answer_state_when_multiple_answer_states_exist(self):
        # Given
        answer_schema = Answer('answer_id')
        answer_schema.widget = MagicMock()
        answer_schema.widget.name = 'answer_id'

        answer_states = []
        for x in range(5):
            answer_state = StateAnswer('answer_id', answer_schema)
            answer_state.answer_instance = x
            answer_states.append(answer_state)

        # When
        new_answer_state = answer_schema.create_new_answer_state(answer_states, answer_instance=1)
        self.assertIsNone(new_answer_state)

        new_answer_state = answer_schema.create_new_answer_state(answer_states, answer_instance=5)
        self.assertEqual(new_answer_state.answer_instance, 5)
        self.assertEqual(new_answer_state.id, answer_schema.id)
        self.assertEqual(new_answer_state.schema_item.widget.name, 'answer_id_5')
