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

    def test_get_questions_with_variants(self):
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
                            'question_variants': [{
                                'when': [{}],
                                'question': {
                                    'id': 'question1',
                                    'title': 'Question 1',
                                    'answers': [
                                        {
                                            'id': 'answer1',
                                            'label': 'Answer 1'
                                        }
                                    ]
                                }
                            }, {
                                'when': [{}],
                                'question': {
                                    'id': 'question1',
                                    'title': 'Another Question 1',
                                    'answers': [
                                        {
                                            'id': 'answer1',
                                            'label': 'Answer 1'
                                        }
                                    ]
                                }
                            }]
                        }
                    ]
                }]
            }]
        }

        schema = QuestionnaireSchema(survey_json)
        questions = schema.get_questions('question1')

        self.assertEqual(len(questions), 2)
        self.assertEqual(questions[0]['title'], 'Question 1')
        self.assertEqual(questions[1]['title'], 'Another Question 1')

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
                            'question': {
                                'id': 'question1',
                                'title': 'Question 1',
                                'answers': [
                                    {
                                        'id': 'answer1',
                                        'label': 'Answer 1'
                                    }
                                ]
                            }
                        }
                    ]
                }]
            }]
        }

        schema = QuestionnaireSchema(survey_json)
        questions = schema.get_questions('question1')

        self.assertEqual(questions[0]['title'], 'Question 1')

    def test_schema_answers(self):
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
                            'question': {
                                'id': 'question1',
                                'title': 'Question 1',
                                'answers': [
                                    {
                                        'id': 'answer1',
                                        'label': 'Answer 1'
                                    }
                                ]
                            }
                        }
                    ]
                }]
            }]
        }

        schema = QuestionnaireSchema(survey_json)
        answers = schema.answers
        self.assertEqual(len(answers), 1)


    def test_get_answers_with_variants(self):
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
                            'question_variants': [
                                {
                                    'when': [{}],
                                    'question': {
                                        'id': 'question1',
                                        'title': 'Question 1',
                                        'answers': [
                                            {
                                                'id': 'answer1',
                                                'label': 'Answer 1'
                                            }
                                        ]
                                    }
                                },
                                {
                                    'when': [{}],
                                    'question': {
                                        'id': 'question1',
                                        'title': 'Question 1',
                                        'answers': [
                                            {
                                                'id': 'answer1',
                                                'label': 'Another Answer 1'
                                            }
                                        ]
                                    }
                                }
                            ]
                        }
                    ]
                }]
            }]
        }

        schema = QuestionnaireSchema(survey_json)
        answers = schema.get_answers('answer1')
        self.assertEqual(len(answers), 2)
        self.assertEqual(answers[0]['label'], 'Answer 1')
        self.assertEqual(answers[1]['label'], 'Another Answer 1')

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
                            'question': {
                                'id': 'question1',
                                'title': 'Question 1',
                                'answers': [
                                    {
                                        'id': 'answer1',
                                        'label': 'Answer 1'
                                    }
                                ]
                            }
                        }
                    ]
                }]
            }]
        }

        schema = QuestionnaireSchema(survey_json)
        answers = schema.get_answers('answer1')
        self.assertEqual(len(answers), 1)
        self.assertEqual(answers[0]['label'], 'Answer 1')

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

def test_get_all_questions_for_block_question():
    block = {
        'id': 'block1',
        'type': 'Question',
        'title': 'Block 1',
        'question': {
            'id': 'question1',
            'title': 'Question 1',
            'answers': [
                {
                    'id': 'answer1',
                    'label': 'Answer 1'
                }
            ]
        }
    }

    all_questions = QuestionnaireSchema.get_all_questions_for_block(block)

    assert len(all_questions) == 1

    assert all_questions[0]['answers'][0]['id'] == 'answer1'

def test_get_all_questions_for_block_question_variants():
    block = {
        'id': 'block1',
        'type': 'Question',
        'title': 'Block 1',
        'question_variants': [
            {
                'question': {
                    'id': 'question1',
                    'title': 'Question 1',
                    'answers': [
                        {
                            'id': 'answer1',
                            'label': 'Variant 1'
                        }
                    ]
                },
                'when': []
            }, {
                'question': {
                    'id': 'question1',
                    'title': 'Question 1',
                    'answers': [
                        {
                            'id': 'answer1',
                            'label': 'Variant 2'
                        }
                    ]
                },
                'when': []
            }
        ]
    }

    all_questions = QuestionnaireSchema.get_all_questions_for_block(block)

    assert len(all_questions) == 2

    assert all_questions[0]['answers'][0]['label'] == 'Variant 1'
    assert all_questions[1]['answers'][0]['label'] == 'Variant 2'

def test_get_all_questions_for_block_empty():
    block = {}

    all_questions = QuestionnaireSchema.get_all_questions_for_block(block)

    assert not all_questions
