from app.questionnaire.questionnaire_schema import QuestionnaireSchema
from app.utilities.schema import load_schema_from_params
from tests.app.app_context_test_case import AppContextTestCase


# pylint: disable=too-many-public-methods
class TestQuestionnaireSchema(AppContextTestCase):

    def test_get_blocks(self):
        schema = load_schema_from_params('test', 'repeating_household')
        blocks = [b for b in schema.get_blocks()]

        self.assertEqual(len(blocks), 5)

    def test_get_groups(self):
        schema = load_schema_from_params('test', 'repeating_household')
        groups = [group for group in schema.get_groups()]

        self.assertEqual(len(groups), 3)

    def test_get_group(self):
        schema = load_schema_from_params('test', 'repeating_household')
        group = schema.get_group('repeating-group')

        self.assertEqual(group['title'], 'Group 2')

    def test_get_block(self):
        schema = load_schema_from_params('test', 'repeating_household')
        block = schema.get_block('household-composition')

        self.assertEqual(block['title'], 'Household')

    def test_get_repeating_rule(self):
        schema = load_schema_from_params('test', 'repeating_household')
        groups = [group for group in schema.get_groups()]
        rule = schema.get_repeat_rule(groups[1])

        self.assertEqual(
            {
                'type': 'answer_count',
                'answer_id': 'first-name'
            }, rule)

    def test_get_answers_that_repeat_in_block(self):
        schema = load_schema_from_params('test', 'repeating_household')
        answers = [answer for answer in schema.get_answers_that_repeat_in_block('household-composition')]

        self.assertEqual(len(answers), 3)

    def test_get_groups_that_repeat_with_answer_id(self):
        schema = load_schema_from_params('test', 'repeating_household')
        groups = [group for group in schema.get_groups_that_repeat_with_answer_id('first-name')]

        self.assertEqual(len(groups), 1)

    def test_get_parent_options_for_block(self):
        schema = load_schema_from_params('test', 'checkbox')

        parent_options = schema.get_parent_options_for_block('mandatory-checkbox')

        expected = {
            'mandatory-checkbox-answer': {
                'index': 6,
                'child_answer_id': 'other-answer-mandatory'
            }
        }

        self.assertEqual(parent_options, expected)

    def test_get_duplicate_aliases(self):
        survey_json = {
            'groups': [{
                'blocks': [{
                    'questions': [{
                        'answers': [
                            {
                                'id': '1',
                                'alias': 'alias_name',
                                'type': 'Checkbox'
                            },
                            {
                                'id': '2',
                                'alias': 'alias_name',
                                'type': 'Checkbox'
                            }
                        ]
                    }]
                }]
            }]
        }

        with self.assertRaises(Exception)as err:
            QuestionnaireSchema(survey_json)

        self.assertEqual('Duplicate alias found: alias_name', str(err.exception))

    def test_get_summary_and_confirmation_blocks_returns_only_summary(self):
        survey_json = {
            'groups': [{
                'blocks': [
                    {
                        'id': 'questionnaire-block',
                        'type': 'Question'
                    },
                    {
                        'id': 'summary-block',
                        'type': 'Summary'
                    },
                    {
                        'id': 'confirmation-block',
                        'type': 'Confirmation'
                    }
                ]
            }]
        }

        schema = QuestionnaireSchema(survey_json)

        summary_and_confirmation_blocks = schema.get_summary_and_confirmation_blocks()

        self.assertEqual(len(summary_and_confirmation_blocks), 2)
        self.assertTrue('summary-block' in summary_and_confirmation_blocks)
        self.assertTrue('confirmation-block' in summary_and_confirmation_blocks)

    def test_group_has_questions_returns_true_when_group_has_questionnaire_blocks(self):
        survey_json = {
            'groups': [{
                'id': 'question-group',
                'blocks': [
                    {
                        'id': 'introduction',
                        'type': 'Introduction'
                    },
                    {
                        'id': 'question',
                        'type': 'Question'
                    }
                ]
            }]
        }

        schema = QuestionnaireSchema(survey_json)

        has_questions = schema.group_has_questions('question-group')

        self.assertTrue(has_questions)

    def test_group_has_questions_returns_false_when_group_doesnt_have_questionnaire_blocks(self):
        survey_json = {
            'groups': [{
                'id': 'non-question-group',
                'blocks': [
                    {
                        'id': 'summary-block',
                        'type': 'Summary'
                    }
                ]
            }]
        }

        schema = QuestionnaireSchema(survey_json)

        has_questions = schema.group_has_questions('non-question-group')

        self.assertFalse(has_questions)
