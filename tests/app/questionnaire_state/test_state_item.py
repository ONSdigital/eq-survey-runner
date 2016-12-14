from unittest import TestCase

from mock import MagicMock

from app.questionnaire_state.state_item import StateItem
from app.schema.section import Section


class TestStateItem(TestCase):

    def test_find_schema_item_finds_item_in_question(self):
        # Given
        schema_item = MagicMock()

        search_schema = MagicMock()

        child = MagicMock()
        child.schema_item = search_schema
        state_item = StateItem('item_id', schema_item)
        state_item.children = [child]

        # When
        result = state_item.find_state_item(search_schema)

        # Then
        self.assertEqual(result, child)

    def test_find_schema_item_finds_item_in_block(self):
        # Given
        block_schema = MagicMock()
        question_schema = MagicMock()
        answer_schema = MagicMock()

        block = StateItem('block_id', block_schema)
        question = StateItem('question_id', question_schema)
        answer = StateItem('answer_id', answer_schema)

        block.children = [question]
        question.children = [answer]

        # When
        result = block.find_state_item(answer_schema)

        # Then
        self.assertEqual(result, answer)

    def test_find_schema_item_schema_item_not_found(self):
        # Given
        block_schema = MagicMock()
        question_schema = MagicMock()
        answer_schema = MagicMock()

        block = StateItem('block_id', block_schema)
        question = StateItem('question_id', question_schema)
        answer = StateItem('answer_id', answer_schema)

        block.children = [question]
        question.children = [answer]

        not_found_schema = MagicMock()

        # When
        result = block.find_state_item(not_found_schema)

        # Then
        self.assertIsNone(result)

    def test_set_skipped_skips_when_equals_satisfied(self):
        answers = {'12345': 'yes'}

        skip = {
            "when": [
                {
                    "id": "12345",
                    "condition": "equals",
                    "value": "yes"
                }
            ]
        }

        section = Section()
        section.skip_condition = skip

        state_item = StateItem(id='', schema_item=section)

        state_item.set_skipped(answers, {})

        self.assertEqual(state_item.skipped, True)

    def test_set_skipped_skips_when_not_equals_satisfied(self):
        answers = {'12345': 'yes'}

        skip = {
            "when": [
                {
                    "id": "12345",
                    "condition": "not equals",
                    "value": "no"
                }
            ]
        }

        section = Section()
        section.skip_condition = skip

        state_item = StateItem(id='', schema_item=section)

        state_item.set_skipped(answers, {})

        self.assertEqual(state_item.skipped, True)

    def test_set_skipped_skips_when_meta_equals_satisfied(self):

        metadata = {'region_code': 'GB-WLS'}

        skip = {
            "when": [
                {
                    "meta": "region_code",
                    "condition": "equals",
                    "value": "GB-WLS"
                }
            ]
        }

        section = Section()
        section.skip_condition = skip

        state_item = StateItem(id='', schema_item=section)

        state_item.set_skipped({}, metadata)

        self.assertEqual(state_item.skipped, True)

