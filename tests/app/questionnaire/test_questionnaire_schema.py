from app.questionnaire.questionnaire_schema import QuestionnaireSchema
from tests.app.app_context_test_case import AppContextTestCase


# pylint: disable=too-many-public-methods
class TestQuestionnaireSchema(AppContextTestCase):
    def test_get_sections(self):
        survey_json = {
            'sections': [{
                'id': 'section1',
                'groups': [{
                    'id': 'group1',
                    'blocks': [
                        {
                            'id': 'block1',
                            'type': 'Question'
                        }
                    ]
                }]
            }]
        }

        schema = QuestionnaireSchema(survey_json)
        self.assertEqual(len(schema.sections), 1)

    def test_get_section(self):
        survey_json = {
            'sections': [{
                'id': 'section1',
                'title': 'Section 1',
                'groups': [{
                    'id': 'group1',
                    'blocks': [
                        {
                            'id': 'block1',
                            'type': 'Question'
                        }
                    ]
                }]
            }]
        }

        schema = QuestionnaireSchema(survey_json)
        section = schema.get_section('section1')
        self.assertEqual(section['title'], 'Section 1')

    def test_get_blocks(self):
        survey_json = {
            'sections': [{
                'id': 'section1',
                'groups': [{
                    'id': 'group1',
                    'blocks': [
                        {
                            'id': 'block1',
                            'type': 'Question'
                        }
                    ]
                }]
            }]
        }

        schema = QuestionnaireSchema(survey_json)
        self.assertEqual(len(schema.blocks), 1)

    def test_get_block(self):
        survey_json = {
            'sections': [{
                'id': 'section1',
                'groups': [{
                    'id': 'group1',
                    'blocks': [
                        {
                            'id': 'block1',
                            'type': 'Question',
                            'title': 'Block 1'
                        }
                    ]
                }]
            }]
        }

        schema = QuestionnaireSchema(survey_json)
        block = schema.get_block('block1')

        self.assertEqual(block['title'], 'Block 1')

    def test_get_groups(self):
        survey_json = {
            'sections': [{
                'id': 'section1',
                'groups': [{
                    'id': 'group1',
                    'blocks': [
                        {
                            'id': 'block1',
                            'type': 'Question',
                            'title': 'Block 1'
                        }
                    ]
                }]
            }]
        }

        schema = QuestionnaireSchema(survey_json)
        self.assertEqual(len(schema.groups), 1)

    def test_get_group(self):
        survey_json = {
            'sections': [{
                'id': 'section1',
                'groups': [{
                    'id': 'group1',
                    'title': 'Group 1',
                    'blocks': [
                        {
                            'id': 'block1',
                            'type': 'Question',
                            'title': 'Block 1'
                        }
                    ]
                }]
            }]
        }

        schema = QuestionnaireSchema(survey_json)
        group = schema.get_group('group1')

        self.assertEqual(group['title'], 'Group 1')

    def test_get_questions(self):
        survey_json = {
            'sections': [{
                'id': 'section1',
                'groups': [{
                    'id': 'group1',
                    'title': 'Group 1',
                    'blocks': [
                        {
                            'id': 'block1',
                            'type': 'Question',
                            'title': 'Block 1',
                            'questions': [
                                {
                                    'id': 'question1'
                                }
                            ]
                        }
                    ]
                }]
            }]
        }

        schema = QuestionnaireSchema(survey_json)
        self.assertEqual(len(schema.questions), 1)

    def test_get_question(self):
        survey_json = {
            'sections': [{
                'id': 'section1',
                'groups': [{
                    'id': 'group1',
                    'title': 'Group 1',
                    'blocks': [
                        {
                            'id': 'block1',
                            'type': 'Question',
                            'title': 'Block 1',
                            'questions': [
                                {
                                    'id': 'question1',
                                    'title': 'Question 1'
                                }
                            ]
                        }
                    ]
                }]
            }]
        }

        schema = QuestionnaireSchema(survey_json)
        question = schema.get_question('question1')

        self.assertEqual(question['title'], 'Question 1')

    def test_get_answers(self):
        survey_json = {
            'sections': [{
                'id': 'section1',
                'groups': [{
                    'id': 'group1',
                    'title': 'Group 1',
                    'blocks': [
                        {
                            'id': 'block1',
                            'type': 'Question',
                            'title': 'Block 1',
                            'questions': [
                                {
                                    'id': 'question1',
                                    'title': 'Question 1',
                                    'answers': [
                                        {
                                            'id': 'answer1',
                                            'label': 'Answer 1'
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }]
            }]
        }

        schema = QuestionnaireSchema(survey_json)
        self.assertEqual(len(schema.answers), 1)

    def test_get_answer(self):
        survey_json = {
            'sections': [{
                'id': 'section1',
                'groups': [{
                    'id': 'group1',
                    'title': 'Group 1',
                    'blocks': [
                        {
                            'id': 'block1',
                            'type': 'Question',
                            'title': 'Block 1',
                            'questions': [
                                {
                                    'id': 'question1',
                                    'title': 'Question 1',
                                    'answers': [
                                        {
                                            'id': 'answer1',
                                            'label': 'Answer 1'
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }]
            }]
        }

        schema = QuestionnaireSchema(survey_json)
        answer = schema.get_answer('answer1')

        self.assertEqual(answer['label'], 'Answer 1')

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
