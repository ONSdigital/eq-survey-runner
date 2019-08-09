import unittest

from mock import Mock

from app.data_model.answer import Answer
from app.data_model.answer_store import AnswerStore
from app.libs.utils import ObjectFromDict, get_answer
from app.utilities.schema import load_schema_from_name
from tests.app.app_context_test_case import AppContextTestCase


class ObjectFromDictTest(unittest.TestCase):
    def test_simple_object(self):
        simple_dict = {
            'property_one': 'string',
            'property_two': 2,
            'property_three': [],
        }

        obj = ObjectFromDict(simple_dict)

        # pylint: disable=maybe-no-member
        # Object is dynamically built and properties dynamically assigned
        self.assertEqual(obj.property_one, 'string')
        self.assertEqual(obj.property_two, 2)
        self.assertEqual(len(obj.property_three), 0)


class TestGetAnswer(unittest.TestCase):
    def test_get_answer_without_repeat(self):
        schema = Mock()
        schema.is_answer_in_list_collector_block = Mock(return_value=False)
        schema.is_answer_in_repeating_section = Mock(return_value=False)

        answer_id = 'mandatory-checkbox-answer'

        expected_answer = Answer(answer_id=answer_id, value=['Cheese', 'Ham'])

        answer_store = AnswerStore([expected_answer.for_json()])

        answer_value = get_answer(schema, answer_store, answer_id)

        assert answer_value == expected_answer

    def test_get_answer_without_repeat_with_list_item_id(self):
        schema = Mock()
        schema.is_answer_in_list_collector_block = Mock(return_value=False)
        schema.is_answer_in_repeating_section = Mock(return_value=False)

        answer_id = 'mandatory-checkbox-answer'

        expected_answer = Answer(answer_id=answer_id, value=['Cheese', 'Ham'])

        answer_store = AnswerStore([expected_answer.for_json()])

        answer_value = get_answer(
            schema, answer_store, answer_id, list_item_id='abc123'
        )

        assert answer_value == expected_answer

    def test_get_answer_within_repeat_with_list_item_id(self):
        schema = Mock()
        schema.is_answer_in_list_collector_block = Mock(return_value=True)
        schema.is_answer_in_repeating_section = Mock(return_value=True)

        answer_id = 'date-of-birth-answer'
        list_item_id = 'abc123'

        expected_answer = Answer(
            answer_id=answer_id, value='2019-01-07', list_item_id=list_item_id
        )

        answer_store = AnswerStore([expected_answer.for_json()])

        answer_value = get_answer(schema, answer_store, answer_id, list_item_id)

        assert answer_value == expected_answer

    def test_get_answer_within_repeat_without_list_item_id(self):
        schema = Mock()
        schema.is_answer_in_list_collector_block = Mock(return_value=True)
        schema.is_answer_in_repeating_section = Mock(return_value=True)

        answer_id = 'date-of-birth-answer'

        expected_answer = Answer(
            answer_id=answer_id, value='2019-01-07', list_item_id='abc123'
        )

        answer_store = AnswerStore([expected_answer.for_json()])

        answer_value = get_answer(schema, answer_store, answer_id)

        assert not answer_value
