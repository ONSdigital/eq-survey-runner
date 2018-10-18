from app.questionnaire.questionnaire_schema import QuestionnaireSchema
from app.utilities.schema import load_schema_from_params
from tests.app.app_context_test_case import AppContextTestCase


# pylint: disable=too-many-public-methods
class TestQuestionnaireSchema(AppContextTestCase):
    def test_get_sections(self):
        schema = load_schema_from_params('test', 'repeating_household')
        self.assertEqual(len(schema.sections), 3)

    def test_get_section(self):
        schema = load_schema_from_params('test', 'repeating_household')
        section = schema.get_section('group-1-section')

        self.assertEqual(section['title'], 'Group 1')

    def test_get_blocks(self):
        schema = load_schema_from_params('test', 'repeating_household')
        self.assertEqual(len(schema.blocks), 6)

    def test_get_block(self):
        schema = load_schema_from_params('test', 'repeating_household')
        block = schema.get_block('household-composition')

        self.assertEqual(block['title'], 'Household')

    def test_get_groups(self):
        schema = load_schema_from_params('test', 'repeating_household')
        self.assertEqual(len(schema.groups), 3)

    def test_get_group(self):
        schema = load_schema_from_params('test', 'repeating_household')
        group = schema.get_group('repeating-group')

        self.assertEqual(group['title'], 'Group 2')

    def test_get_questions(self):
        schema = load_schema_from_params('test', 'repeating_household')
        self.assertEqual(len(schema.questions), 4)

    def test_get_question(self):
        schema = load_schema_from_params('test', 'repeating_household')
        question = schema.get_question('household-composition-question')

        self.assertEqual(question['title'], 'Who usually lives here?')

    def test_get_answers(self):
        schema = load_schema_from_params('test', 'repeating_household')
        self.assertEqual(len(schema.answers), 6)

    def test_get_answer(self):
        schema = load_schema_from_params('test', 'repeating_household')
        answer = schema.get_answer('first-name')

        self.assertEqual(answer['label'], 'First Name')

    def test_get_repeating_rule(self):
        schema = load_schema_from_params('test', 'repeating_household')
        groups = [group for group in schema.groups]
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

    def test_get_summary_and_confirmation_blocks_returns_only_summary(self):
        survey_json = {
            'sections': [{
                'id': 'section1',
                'groups': [{
                    'id': 'group1',
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
            }]
        }

        schema = QuestionnaireSchema(survey_json)

        summary_and_confirmation_blocks = schema.get_summary_and_confirmation_blocks()

        self.assertEqual(len(summary_and_confirmation_blocks), 2)
        self.assertTrue('summary-block' in summary_and_confirmation_blocks)
        self.assertTrue('confirmation-block' in summary_and_confirmation_blocks)

    def test_group_has_questions_returns_true_when_group_has_questionnaire_blocks(self):
        survey_json = {
            'sections': [{
                'id': 'section1',
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
            }]
        }

        schema = QuestionnaireSchema(survey_json)

        has_questions = schema.group_has_questions('question-group')

        self.assertTrue(has_questions)

    def test_group_has_questions_returns_false_when_group_doesnt_have_questionnaire_blocks(self):
        survey_json = {
            'sections': [{
                'id': 'section1',
                'groups': [{
                    'id': 'non-question-group',
                    'blocks': [
                        {
                            'id': 'summary-block',
                            'type': 'Summary'
                        }
                    ]
                }]
            }]
        }

        schema = QuestionnaireSchema(survey_json)

        has_questions = schema.group_has_questions('non-question-group')

        self.assertFalse(has_questions)

    def test_is_summary(self):
        survey_json = {
            'sections': [{
                'id': 'section-1',
                'groups': [{
                    'id': 'group-1',
                    'blocks': [
                        {
                            'id': 'block-1',
                            'type': 'Summary'
                        }
                    ]
                }]
            }]
        }

        schema = QuestionnaireSchema(survey_json)
        self.assertTrue(schema.is_summary_section(schema.get_section('section-1')))
        self.assertTrue(schema.is_summary_group(schema.get_group('group-1')))
        self.assertFalse(schema.is_confirmation_section(schema.get_section('section-1')))
        self.assertFalse(schema.is_confirmation_group(schema.get_group('group-1')))

    def test_is_repeating_answer_type_repeating_answer(self):
        survey_json = {
            'sections': [{
                'id': 'section1',
                'groups': [{
                    'id': 'question-group',
                    'blocks': [
                        {
                            'id': 'repeating-question-block',
                            'type': 'Question',
                            'questions': [{
                                'id': 'repeating-question',
                                'type': 'RepeatingAnswer',
                                'answers': [{
                                    'id': 'first-name'
                                }]
                            }]
                        }
                    ]
                }]
            }]
        }
        schema = QuestionnaireSchema(survey_json)

        self.assertTrue(schema.is_repeating_answer_type('first-name'))

    def test_is_confirmation(self):
        survey_json = {
            'sections': [{
                'id': 'section-1',
                'groups': [{
                    'id': 'group-1',
                    'blocks': [
                        {
                            'id': 'block-1',
                            'type': 'Confirmation'
                        }
                    ]
                }]
            }]
        }

        schema = QuestionnaireSchema(survey_json)
        self.assertTrue(schema.is_confirmation_section(schema.get_section('section-1')))
        self.assertTrue(schema.is_confirmation_group(schema.get_group('group-1')))
        self.assertFalse(schema.is_summary_section(schema.get_section('section-1')))
        self.assertFalse(schema.is_summary_group(schema.get_group('group-1')))

    def test_is_repeating_answer_type_general_answer(self):
        survey_json = {
            'sections': [{
                'id': 'section1',
                'groups': [{
                    'id': 'question-group',
                    'blocks': [
                        {
                            'id': 'question-block',
                            'type': 'Question',
                            'questions': [{
                                'id': 'question',
                                'type': 'General',
                                'answers': [{
                                    'id': 'first-name'
                                }]
                            }]
                        }
                    ]
                }]
            }]
        }

        schema = QuestionnaireSchema(survey_json)

        self.assertFalse(schema.is_repeating_answer_type('first-name'))

    def test_is_repeating_answer_type_checkbox(self):
        survey_json = {
            'sections': [{
                'id': 'section1',
                'groups': [{
                    'id': 'question-group',
                    'blocks': [
                        {
                            'id': 'question-block',
                            'type': 'Question',
                            'questions': [{
                                'id': 'question',
                                'type': 'General',
                                'answers': [{
                                    'id': 'frequency-answer',
                                    'options': [{
                                        'value': 'Weekly'
                                    }],
                                    'type': 'Checkbox'
                                }]
                            }]
                        }
                    ]
                }]
            }]
        }

        schema = QuestionnaireSchema(survey_json)

        self.assertTrue(schema.is_repeating_answer_type('frequency-answer'))

    def test_answer_is_in_repeating_group(self):
        schema = load_schema_from_params('test', 'repeating_household')

        self.assertFalse(schema.answer_is_in_repeating_group('first-name'))
        self.assertTrue(schema.answer_is_in_repeating_group('confirm-answer'))

    def test_title_when_dependencies_are_added_to_dependencies(self):
        schema = load_schema_from_params('test', 'titles')
        dependencies = schema.answer_dependencies['behalf-of-answer']

        self.assertIn('gender-answer', dependencies)
        self.assertIn('age-answer', dependencies)
        self.assertEqual(len(dependencies), 2)
