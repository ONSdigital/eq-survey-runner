import unittest

from app.helpers.schema_helper import SchemaHelper
from app.utilities.schema import load_schema_file


# pylint: disable=too-many-public-methods
class TestSchemaHelper(unittest.TestCase):

    def test_first_block_id(self):
        survey = load_schema_file("test_repeating_household.json")

        first_block_id = "introduction"

        self.assertEqual(SchemaHelper.get_first_block_id(survey), first_block_id)

    def test_last_block_id(self):
        survey = load_schema_file("test_repeating_household.json")

        last_block_id = "summary"

        self.assertEqual(SchemaHelper.get_last_block_id(survey), last_block_id)

    def test_first_group_id(self):
        survey = load_schema_file("test_repeating_household.json")

        first_group_id = "multiple-questions-group"

        self.assertEqual(SchemaHelper.get_first_group_id(survey), first_group_id)

    def test_last_group_id(self):
        survey = load_schema_file("test_repeating_household.json")

        last_group_id = "summary-group"

        self.assertEqual(last_group_id, SchemaHelper.get_last_group_id(survey))

    def test_get_blocks(self):
        survey = load_schema_file("test_repeating_household.json")
        blocks = [b for b in SchemaHelper.get_blocks(survey)]

        self.assertEqual(len(blocks), 5)

    def test_get_groups(self):
        survey = load_schema_file("test_repeating_household.json")
        groups = [group for group in SchemaHelper.get_groups(survey)]

        self.assertEqual(len(groups), 3)

    def test_get_group(self):
        survey = load_schema_file("test_repeating_household.json")
        group = SchemaHelper.get_group(survey, "repeating-group")

        self.assertEqual(group['title'], "Group 2")

    def test_get_block(self):
        survey = load_schema_file("test_repeating_household.json")
        block = SchemaHelper.get_block(survey, "repeating-block-1")

        self.assertEqual(block['title'], "Block 2")

    def test_get_repeating_rule(self):
        survey = load_schema_file("test_repeating_household.json")
        groups = [group for group in SchemaHelper.get_groups(survey)]
        rule = SchemaHelper.get_repeat_rule(groups[1])

        self.assertEqual(
            {
                'type': 'answer_count',
                'answer_id': 'first-name',
                'navigation_label_answer_ids': ['first-name', 'last-name'],
            }, rule)

    def test_get_answers_that_repeat_in_block(self):
        survey = load_schema_file("test_repeating_household.json")
        answers = [answer for answer in SchemaHelper.get_answers_that_repeat_in_block(survey, 'household-composition')]

        self.assertEqual(len(answers), 3)

    def test_get_groups_that_repeat_with_answer_id(self):
        survey = load_schema_file("test_repeating_household.json")
        groups = [group for group in SchemaHelper.get_groups_that_repeat_with_answer_id(survey, 'first-name')]

        self.assertEqual(len(groups), 1)

    def test_get_parent_options_for_block(self):
        survey = load_schema_file("test_checkbox.json")
        block_json = SchemaHelper.get_block(survey, 'mandatory-checkbox')

        parent_options = SchemaHelper.get_parent_options_for_block(block_json)

        expected = {
            'mandatory-checkbox-answer': {
                'index': 6,
                'child_answer_id': 'other-answer-mandatory'
            }
        }

        self.assertEqual(parent_options, expected)

    def test_get_last_block_returns_none_when_no_blocks(self):
        empty_group = {}

        last_block = SchemaHelper.get_last_block_in_group(empty_group)

        self.assertIsNone(last_block)

    def test_get_last_block_returns_last_block(self):
        group = {
            'blocks': [{
                'id': 'block1',
            }, {
                'id': 'block2'
            }]
        }

        last_block = SchemaHelper.get_last_block_in_group(group)

        self.assertIsNotNone(last_block)
        self.assertEqual(last_block['id'], 'block2')

    def test_is_summary_or_confirmation_returns_false_when_block_is_none(self):
        block = None

        is_summary_or_confirmation = SchemaHelper.is_summary_or_confirmation(block)

        self.assertFalse(is_summary_or_confirmation)

    def test_is_summary_or_confirmation_returns_false_when_block_has_no_type(self):
        block = {
            'id': 'block-with-no-type',
        }

        is_summary_or_confirmation = SchemaHelper.is_summary_or_confirmation(block)

        self.assertFalse(is_summary_or_confirmation)

    def test_is_summary_or_confirmation_returns_false_when_type_is_questionnaire(self):
        block = {
            'type': 'Questionnaire',
        }

        is_summary_or_confirmation = SchemaHelper.is_summary_or_confirmation(block)

        self.assertFalse(is_summary_or_confirmation)

    def test_is_summary_or_confirmation_returns_true_when_type_is_summary(self):
        block = {
            'type': 'Summary',
        }

        is_summary_or_confirmation = SchemaHelper.is_summary_or_confirmation(block)

        self.assertTrue(is_summary_or_confirmation)

    def test_is_summary_or_confirmation_returns_true_when_type_is_confirmation(self):
        block = {
            'type': 'Confirmation',
        }

        is_summary_or_confirmation = SchemaHelper.is_summary_or_confirmation(block)

        self.assertTrue(is_summary_or_confirmation)

    def test_group_has_questions_returns_true_when_group_has_questionnaire_blocks(self):
        group = {
            'blocks': [
                {
                    'id': 'introduction',
                    'type': 'Introduction'
                },
                {
                    'id': 'question',
                    'type': 'Questionnaire'
                }
            ]
        }

        has_questions = SchemaHelper.group_has_questions(group)

        self.assertTrue(has_questions)

    def test_group_has_questions_returns_false_when_group_doesnt_have_questionnaire_blocks(self):
        group = {
            'blocks': [
                {
                    'id': 'summary-block',
                    'type': 'Summary'
                },
            ]
        }

        has_questions = SchemaHelper.group_has_questions(group)

        self.assertFalse(has_questions)
