from app.questionnaire.questionnaire_schema import QuestionnaireSchema
from tests.app.app_context_test_case import AppContextTestCase


# pylint: disable=too-many-public-methods
class TestQuestionnaireSchema(AppContextTestCase):
    def test_get_sections(self):
        survey_json = {
            'sections': [
                {
                    'id': 'section1',
                    'groups': [
                        {
                            'id': 'group1',
                            'blocks': [{'id': 'block1', 'type': 'Question'}],
                        }
                    ],
                }
            ]
        }

        schema = QuestionnaireSchema(survey_json)
        self.assertEqual(len(schema.get_sections()), 1)

    def test_get_section(self):
        survey_json = {
            'sections': [
                {
                    'id': 'section1',
                    'title': 'Section 1',
                    'groups': [
                        {
                            'id': 'group1',
                            'blocks': [{'id': 'block1', 'type': 'Question'}],
                        }
                    ],
                }
            ]
        }

        schema = QuestionnaireSchema(survey_json)
        section = schema.get_section('section1')
        self.assertEqual(section['title'], 'Section 1')

    def test_get_blocks(self):
        survey_json = {
            'sections': [
                {
                    'id': 'section1',
                    'groups': [
                        {
                            'id': 'group1',
                            'blocks': [{'id': 'block1', 'type': 'Question'}],
                        }
                    ],
                }
            ]
        }

        schema = QuestionnaireSchema(survey_json)
        self.assertEqual(len(schema.get_blocks()), 1)

    def test_get_block(self):
        survey_json = {
            'sections': [
                {
                    'id': 'section1',
                    'groups': [
                        {
                            'id': 'group1',
                            'blocks': [{'id': 'block1', 'type': 'Question'}],
                        }
                    ],
                }
            ]
        }

        schema = QuestionnaireSchema(survey_json)
        block = schema.get_block('block1')

        self.assertEqual(block['id'], 'block1')

    def test_get_groups(self):
        survey_json = {
            'sections': [
                {
                    'id': 'section1',
                    'groups': [
                        {
                            'id': 'group1',
                            'blocks': [
                                {'id': 'block1', 'type': 'Question', 'title': 'Block 1'}
                            ],
                        }
                    ],
                }
            ]
        }

        schema = QuestionnaireSchema(survey_json)
        self.assertEqual(len(schema.get_groups()), 1)

    def test_get_group(self):
        survey_json = {
            'sections': [
                {
                    'id': 'section1',
                    'groups': [
                        {
                            'id': 'group1',
                            'title': 'Group 1',
                            'blocks': [
                                {'id': 'block1', 'type': 'Question', 'title': 'Block 1'}
                            ],
                        }
                    ],
                }
            ]
        }

        schema = QuestionnaireSchema(survey_json)
        group = schema.get_group('group1')

        self.assertEqual(group['title'], 'Group 1')

    def test_get_questions_with_variants(self):
        survey_json = {
            'sections': [
                {
                    'id': 'section1',
                    'groups': [
                        {
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
                                                        'label': 'Answer 1',
                                                    }
                                                ],
                                            },
                                        },
                                        {
                                            'when': [{}],
                                            'question': {
                                                'id': 'question1',
                                                'title': 'Another Question 1',
                                                'answers': [
                                                    {
                                                        'id': 'answer1',
                                                        'label': 'Answer 1',
                                                    }
                                                ],
                                            },
                                        },
                                    ],
                                }
                            ],
                        }
                    ],
                }
            ]
        }

        schema = QuestionnaireSchema(survey_json)
        questions = schema.get_questions('question1')

        self.assertEqual(len(questions), 2)
        self.assertEqual(questions[0]['title'], 'Question 1')
        self.assertEqual(questions[1]['title'], 'Another Question 1')

    def test_get_questions(self):
        survey_json = {
            'sections': [
                {
                    'id': 'section1',
                    'groups': [
                        {
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
                                            {'id': 'answer1', 'label': 'Answer 1'}
                                        ],
                                    },
                                }
                            ],
                        }
                    ],
                }
            ]
        }

        schema = QuestionnaireSchema(survey_json)
        questions = schema.get_questions('question1')

        self.assertEqual(questions[0]['title'], 'Question 1')

    def test_schema_answers(self):
        survey_json = {
            'sections': [
                {
                    'id': 'section1',
                    'groups': [
                        {
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
                                            {'id': 'answer1', 'label': 'Answer 1'}
                                        ],
                                    },
                                }
                            ],
                        }
                    ],
                }
            ]
        }

        schema = QuestionnaireSchema(survey_json)
        answers = schema.get_answer_ids()
        self.assertEqual(len(answers), 1)

    def test_get_answers_with_variants(self):
        survey_json = {
            'sections': [
                {
                    'id': 'section1',
                    'groups': [
                        {
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
                                                        'label': 'Answer 1',
                                                    }
                                                ],
                                            },
                                        },
                                        {
                                            'when': [{}],
                                            'question': {
                                                'id': 'question1',
                                                'title': 'Question 1',
                                                'answers': [
                                                    {
                                                        'id': 'answer1',
                                                        'label': 'Another Answer 1',
                                                    }
                                                ],
                                            },
                                        },
                                    ],
                                }
                            ],
                        }
                    ],
                }
            ]
        }

        schema = QuestionnaireSchema(survey_json)
        answers = schema.get_answers_by_answer_id('answer1')
        self.assertEqual(len(answers), 2)
        self.assertEqual(answers[0]['label'], 'Answer 1')
        self.assertEqual(answers[1]['label'], 'Another Answer 1')

    def test_get_answers(self):
        survey_json = {
            'sections': [
                {
                    'id': 'section1',
                    'groups': [
                        {
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
                                            {'id': 'answer1', 'label': 'Answer 1'}
                                        ],
                                    },
                                }
                            ],
                        }
                    ],
                }
            ]
        }

        schema = QuestionnaireSchema(survey_json)
        answers = schema.get_answers_by_answer_id('answer1')
        self.assertEqual(len(answers), 1)
        self.assertEqual(answers[0]['label'], 'Answer 1')

    def test_get_summary_and_confirmation_blocks_returns_only_summary(self):
        survey_json = {
            'sections': [
                {
                    'id': 'section1',
                    'groups': [
                        {
                            'id': 'group1',
                            'blocks': [
                                {'id': 'questionnaire-block', 'type': 'Question'},
                                {'id': 'summary-block', 'type': 'Summary'},
                                {'id': 'confirmation-block', 'type': 'Confirmation'},
                            ],
                        }
                    ],
                }
            ]
        }

        schema = QuestionnaireSchema(survey_json)

        summary_and_confirmation_blocks = schema.get_summary_and_confirmation_blocks()

        self.assertEqual(len(summary_and_confirmation_blocks), 2)
        self.assertTrue('summary-block' in summary_and_confirmation_blocks)
        self.assertTrue('confirmation-block' in summary_and_confirmation_blocks)

    def test_group_has_questions_returns_true_when_group_has_questionnaire_blocks(self):
        survey_json = {
            'sections': [
                {
                    'id': 'section1',
                    'groups': [
                        {
                            'id': 'question-group',
                            'blocks': [
                                {'id': 'introduction', 'type': 'Introduction'},
                                {'id': 'question', 'type': 'Question'},
                            ],
                        }
                    ],
                }
            ]
        }

        schema = QuestionnaireSchema(survey_json)

        has_questions = schema.group_has_questions('question-group')

        self.assertTrue(has_questions)

    def test_group_has_questions_returns_false_when_group_doesnt_have_questionnaire_blocks(
        self
    ):
        survey_json = {
            'sections': [
                {
                    'id': 'section1',
                    'groups': [
                        {
                            'id': 'non-question-group',
                            'blocks': [{'id': 'summary-block', 'type': 'Summary'}],
                        }
                    ],
                }
            ]
        }

        schema = QuestionnaireSchema(survey_json)

        has_questions = schema.group_has_questions('non-question-group')

        self.assertFalse(has_questions)

    def test_is_summary(self):
        survey_json = {
            'sections': [
                {
                    'id': 'section-1',
                    'groups': [
                        {
                            'id': 'group-1',
                            'blocks': [{'id': 'block-1', 'type': 'Summary'}],
                        }
                    ],
                }
            ]
        }

        schema = QuestionnaireSchema(survey_json)
        self.assertTrue(schema.is_summary_section(schema.get_section('section-1')))
        self.assertTrue(schema.is_summary_group(schema.get_group('group-1')))
        self.assertFalse(
            schema.is_confirmation_section(schema.get_section('section-1'))
        )
        self.assertFalse(schema.is_confirmation_group(schema.get_group('group-1')))

    def test_is_confirmation(self):
        survey_json = {
            'sections': [
                {
                    'id': 'section-1',
                    'groups': [
                        {
                            'id': 'group-1',
                            'blocks': [{'id': 'block-1', 'type': 'Confirmation'}],
                        }
                    ],
                }
            ]
        }

        schema = QuestionnaireSchema(survey_json)
        self.assertTrue(schema.is_confirmation_section(schema.get_section('section-1')))
        self.assertTrue(schema.is_confirmation_group(schema.get_group('group-1')))
        self.assertFalse(schema.is_summary_section(schema.get_section('section-1')))
        self.assertFalse(schema.is_summary_group(schema.get_group('group-1')))

    def test_get_group_for_list_collector_child_block(self):
        survey_json = {
            'sections': [
                {
                    'id': 'section1',
                    'groups': [
                        {
                            'id': 'group',
                            'blocks': [
                                {
                                    'id': 'list-collector',
                                    'type': 'ListCollector',
                                    'for_list': 'list',
                                    'question': {},
                                    'add_block': {
                                        'id': 'add-block',
                                        'type': 'ListAddQuestion',
                                        'question': {},
                                    },
                                    'edit_block': {
                                        'id': 'edit-block',
                                        'type': 'ListEditQuestion',
                                        'question': {},
                                    },
                                    'remove_block': {
                                        'id': 'remove-block',
                                        'type': 'ListRemoveQuestion',
                                        'question': {},
                                    },
                                }
                            ],
                        }
                    ],
                }
            ]
        }

        schema = QuestionnaireSchema(survey_json)

        group = schema.get_group_for_block_id('add-block')

        self.assertIsNotNone(group)
        self.assertEqual(group['id'], 'group')


def test_get_all_questions_for_block_question():
    block = {
        'id': 'block1',
        'type': 'Question',
        'title': 'Block 1',
        'question': {
            'id': 'question1',
            'title': 'Question 1',
            'answers': [{'id': 'answer1', 'label': 'Answer 1'}],
        },
    }

    all_questions = QuestionnaireSchema.get_all_questions_for_block(block)

    assert len(all_questions) == 1

    assert all_questions[0]['answers'][0]['id'] == 'answer1'


def test_get_all_when_rules_by_list_name():
    survey_json = {
        'sections': [
            {
                'id': 'section1',
                'groups': [
                    {
                        'id': 'group1',
                        'blocks': [
                            {
                                'id': 'list-collector',
                                'type': 'ListCollector',
                                'for_list': 'list',
                                'question': {},
                                'add_block': {
                                    'id': 'add-block',
                                    'type': 'ListAddQuestion',
                                    'question': {},
                                },
                                'edit_block': {
                                    'id': 'edit-block',
                                    'type': 'ListEditQuestion',
                                    'question': {},
                                },
                                'remove_block': {
                                    'id': 'remove-block',
                                    'type': 'ListRemoveQuestion',
                                    'question': {},
                                },
                            }
                        ],
                    }
                ],
            },
            {
                'id': 'section2',
                'groups': [
                    {
                        'id': 'group2',
                        'blocks': [
                            {
                                'type': 'Question',
                                'id': 'block2',
                                'question': {
                                    'answers': [
                                        {
                                            'id': 'answer1',
                                            'mandatory': True,
                                            'type': 'General',
                                        }
                                    ],
                                    'id': 'question1',
                                    'title': {'text': 'Does anyone else live here?'},
                                    'type': 'General',
                                },
                                'when': [
                                    {
                                        'condition': 'greater than',
                                        'list': 'list',
                                        'value': 0,
                                    }
                                ],
                            }
                        ],
                    }
                ],
            },
            {
                'id': 'section3',
                'groups': [
                    {
                        'id': 'group3',
                        'blocks': [
                            {
                                'type': 'Question',
                                'id': 'block3',
                                'question': {
                                    'answers': [
                                        {
                                            'id': 'answer1',
                                            'mandatory': True,
                                            'type': 'General',
                                        }
                                    ],
                                    'id': 'question1',
                                    'title': {'text': 'Does anyone else live here?'},
                                    'type': 'General',
                                },
                                'when': [
                                    {
                                        'condition': 'greater than',
                                        'list': 'not-the-list',
                                        'value': 0,
                                    }
                                ],
                            }
                        ],
                    }
                ],
            },
        ]
    }

    schema = QuestionnaireSchema(survey_json)
    when_blocks = schema.get_sections_associated_to_list_name('list')

    assert len(when_blocks) == 1
    assert 'section2' in when_blocks


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
                    'answers': [{'id': 'answer1', 'label': 'Variant 1'}],
                },
                'when': [],
            },
            {
                'question': {
                    'id': 'question1',
                    'title': 'Question 1',
                    'answers': [{'id': 'answer1', 'label': 'Variant 2'}],
                },
                'when': [],
            },
        ],
    }

    all_questions = QuestionnaireSchema.get_all_questions_for_block(block)

    assert len(all_questions) == 2

    assert all_questions[0]['answers'][0]['label'] == 'Variant 1'
    assert all_questions[1]['answers'][0]['label'] == 'Variant 2'


def test_get_all_questions_for_block_empty():
    block = {}

    all_questions = QuestionnaireSchema.get_all_questions_for_block(block)

    assert not all_questions


def test_get_default_answer_no_answer_in_answer_store(question_variant_schema):
    schema = QuestionnaireSchema(question_variant_schema)
    assert schema.get_default_answer('test') is None


def test_get_default_answer_no_default_in_schema(question_variant_schema):
    schema = QuestionnaireSchema(question_variant_schema)
    assert schema.get_default_answer('answer1') is None


def test_get_default_answer_single_question(single_question_schema):
    schema = QuestionnaireSchema(single_question_schema)
    answer = schema.get_default_answer('answer1')

    assert answer.answer_id == 'answer1'
    assert answer.value == 'test'


def test_get_relationship_collectors(relationship_collector_schema):
    schema = QuestionnaireSchema(relationship_collector_schema)
    answer = schema.get_relationship_collectors()

    assert len(answer) == 2
    assert answer[0]['id'] == 'relationships'
    assert answer[1]['id'] == 'relationships-that-dont-point-to-list-collector'


def test_get_relationship_collectors_by_list_name(relationship_collector_schema):
    schema = QuestionnaireSchema(relationship_collector_schema)
    answer = schema.get_relationship_collectors_by_list_name('people')

    assert len(answer) == 1
    assert answer[0]['id'] == 'relationships'


def test_get_relationship_collectors_by_list_name_no_collectors(
    relationship_collector_schema
):
    schema = QuestionnaireSchema(relationship_collector_schema)
    answer = schema.get_relationship_collectors_by_list_name('not-a-list')

    assert not answer


def test_get_list_item_id_for_answer_id_without_list_item_id(
    section_with_repeating_list
):
    schema = QuestionnaireSchema(section_with_repeating_list)

    expected_list_item_id = None

    list_item_id = schema.get_list_item_id_for_answer_id(
        answer_id='answer1', list_item_id=expected_list_item_id
    )

    assert list_item_id == expected_list_item_id


def test_get_list_item_id_for_answer_id_without_repeat_or_list_collector(
    question_schema
):
    schema = QuestionnaireSchema(question_schema)

    list_item_id = schema.get_list_item_id_for_answer_id(
        answer_id='answer1', list_item_id='abc123'
    )

    assert list_item_id is None


def test_get_answer_within_repeat_with_list_item_id(section_with_repeating_list):
    schema = QuestionnaireSchema(section_with_repeating_list)

    expected_list_item_id = 'abc123'

    list_item_id = schema.get_list_item_id_for_answer_id(
        answer_id='proxy-answer', list_item_id=expected_list_item_id
    )

    assert list_item_id == expected_list_item_id


def test_get_answer_within_list_collector_with_list_item_id(
    list_collector_variant_schema
):
    schema = QuestionnaireSchema(list_collector_variant_schema)

    expected_list_item_id = 'abc123'

    list_item_id = schema.get_list_item_id_for_answer_id(
        answer_id='answer1', list_item_id=expected_list_item_id
    )

    assert list_item_id == expected_list_item_id
