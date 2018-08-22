import unittest
from app.questionnaire.answer_dependencies import AnswerDependencies
from app.questionnaire.answer_dependencies import get_answer_dependencies
from app.questionnaire.questionnaire_schema import QuestionnaireSchema


class TestDependencies(unittest.TestCase):
    def test_length_returns_number_answer_ids_added(self):
        sut = AnswerDependencies()

        sut.add('answer1', 'dependency_id')
        sut.add('answer2', 'dependency_id')
        sut.add('answer3', 'dependency_id')

        self.assertEqual(len(sut), 3)
        self.assertEqual(sut['answer1'], {'dependency_id'})

    def test_duplicate_dependencies_do_not_duplicate(self):
        sut = AnswerDependencies()

        sut.add('answer1', 'dependency_id')
        sut.add('answer1', 'dependency_id')

        self.assertEqual(sut['answer1'], {'dependency_id'})

    def test_multiple_adds_are_added_to_correct_answer(self):
        sut = AnswerDependencies()

        sut.add('answer1', 'dependency_id1')
        sut.add('answer2', 'dependency_id2')
        sut.add('answer2', 'dependency_id4')
        sut.add('answer3', 'dependency_id3')
        sut.add('answer3', 'dependency_id5')
        sut.add('answer3', 'dependency_id6')

        self.assertEqual(sut['answer1'], {'dependency_id1'})
        self.assertEqual(sut['answer2'], {'dependency_id2', 'dependency_id4'})
        self.assertEqual(sut['answer3'], {'dependency_id3', 'dependency_id5', 'dependency_id6'})

    def test_dependencies_can_be_added_with_update(self):

        sut_a = AnswerDependencies()
        sut_a.add('answer1', 'dependency_id1')

        sut_b = AnswerDependencies()
        sut_b.add('answer2', 'dependency_id2')
        sut_b.add('answer2', 'dependency_id4')
        sut_b.add('answer3', 'dependency_id3')
        sut_b.add('answer3', 'dependency_id5')
        sut_b.add('answer3', 'dependency_id6')

        sut_a.update(sut_b)

        self.assertEqual(sut_a['answer1'], {'dependency_id1'})
        self.assertEqual(sut_a['answer2'], {'dependency_id2', 'dependency_id4'})
        self.assertEqual(sut_a['answer3'], {'dependency_id3', 'dependency_id5', 'dependency_id6'})


class TestGetDependencies(unittest.TestCase):

    def test_min_values_from_answer_ids_are_added_to_dependencies(self):
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
                                'id': 'set-min-question',
                                'title': 'Please set the minimum and maximum used for future questions',
                                'type': 'General',
                                'answers': [
                                    {
                                        'id': 'set-minimum',
                                        'label': 'Minimum Value',
                                        'mandatory': True,
                                        'type': 'Number',
                                        'decimal_places': 2,
                                        'min_value': {
                                            'answer_id': 'dependency1'
                                        },
                                        'max_value': {
                                            'value': 1000
                                        }
                                    },
                                    {
                                        'id': 'set-maximum',
                                        'label': 'Maximum Value',
                                        'mandatory': True,
                                        'type': 'Number',
                                        'decimal_places': 2,
                                        'min_value': {
                                            'answer_id': 'dependency2'
                                        },
                                        'max_value': {
                                            'value': 10000
                                        }
                                    }
                                ]
                            }],
                        }
                    ]
                }]
            }]
        }

        schema = QuestionnaireSchema(survey_json)   # schema uses a dependencies builder, using an external one to make tests obvious

        dependencies = get_answer_dependencies(schema)

        self.assertEqual(len(dependencies), 2)
        self.assertEqual(dependencies['dependency1'], {'set-minimum'})
        self.assertEqual(dependencies['dependency2'], {'set-maximum'})

    def test_max_values_from_answer_ids_are_added_to_dependencies(self):

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
                                'id': 'set-min-question',
                                'title': 'Please set the minimum and maximum used for future questions',
                                'type': 'General',
                                'answers': [
                                    {
                                        'id': 'set-minimum',
                                        'label': 'Minimum Value',
                                        'mandatory': True,
                                        'type': 'Number',
                                        'decimal_places': 2,
                                        'max_value': {
                                            'answer_id': 'dependency1'
                                        },
                                        'min_value': {
                                            'value': 1000
                                        }
                                    },
                                    {
                                        'id': 'set-maximum',
                                        'label': 'Maximum Value',
                                        'mandatory': True,
                                        'type': 'Number',
                                        'decimal_places': 2,
                                        'max_value': {
                                            'answer_id': 'dependency2'
                                        },
                                        'min_value': {
                                            'value': 10000
                                        }
                                    }
                                ]
                            }],
                        }
                    ]
                }]
            }]
        }

        schema = QuestionnaireSchema(survey_json)

        dependencies = get_answer_dependencies(schema)

        self.assertEqual(len(dependencies), 2)
        self.assertEqual(dependencies['dependency1'], {'set-minimum'})
        self.assertEqual(dependencies['dependency2'], {'set-maximum'})

    def test_calculation_ids_are_added_to_dependencies(self):
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
                                'id': 'breakdown-question',
                                'title': 'Breakdown',
                                'type': 'Calculated',
                                'calculations': [{
                                    'calculation_type': 'sum',
                                    'answer_id': 'total-answer',
                                    'answers_to_calculate': [
                                        'breakdown-1',
                                        'breakdown-2',
                                        'breakdown-3',
                                        'breakdown-4'
                                    ],
                                    'conditions': [
                                        'less than',
                                        'equals'
                                    ]
                                }],
                                'answers': [
                                    {
                                        'id': 'breakdown-1',
                                        'label': 'Breakdown 1',
                                        'mandatory': False,
                                        'decimal_places': 2,
                                        'type': 'Number'
                                    },
                                    {
                                        'id': 'breakdown-2',
                                        'label': 'Breakdown 2',
                                        'mandatory': False,
                                        'decimal_places': 2,
                                        'type': 'Number'
                                    },
                                    {
                                        'id': 'breakdown-3',
                                        'label': 'Breakdown 3',
                                        'mandatory': False,
                                        'decimal_places': 2,
                                        'type': 'Number'
                                    },
                                    {
                                        'id': 'breakdown-4',
                                        'label': 'Breakdown 4',
                                        'mandatory': False,
                                        'decimal_places': 2,
                                        'type': 'Number'
                                    }
                                ]
                            }]
                        }
                    ]
                }]
            }]
        }
        schema = QuestionnaireSchema(survey_json)

        dependencies = get_answer_dependencies(schema)

        self.assertEqual(len(dependencies), 1)
        self.assertEqual(dependencies['total-answer'], {'breakdown-1', 'breakdown-2', 'breakdown-3', 'breakdown-4'})

    def test_question_titles_when_dependencies_are_added_to_dependencies(self):
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
                                'id': 'what-gender-question',
                                'titles': [
                                    {
                                        'value': 'Some Title',
                                        'when': [{
                                            'id': 'behalf-of-answer1',
                                            'condition': 'equals',
                                            'value': 'chad'
                                        }]
                                    },
                                    {
                                        'value': 'Another Title',
                                        'when': [{
                                            'id': 'behalf-of-answer2',
                                            'condition': 'equals',
                                            'value': 'kelly'
                                        }]
                                    },
                                    {
                                        'value': 'What is their gender?',
                                        'when': [{
                                            'id': 'behalf-of-answer3',
                                            'condition': 'equals',
                                            'value': 'else'
                                        }]
                                    }
                                ],
                                'type': 'General',
                                'answers': [{
                                    'type': 'Radio',
                                    'id': 'gender-answer',
                                    'mandatory': True,
                                    'options': [
                                        {
                                            'label': 'Male',
                                            'value': 'male'
                                        },
                                        {
                                            'label': 'Female',
                                            'value': 'female'
                                        }
                                    ]
                                }]
                            }],
                        }
                    ]
                }]
            }]
        }

        schema = QuestionnaireSchema(survey_json)

        dependencies = get_answer_dependencies(schema)

        self.assertEqual(len(dependencies), 3)
        self.assertEqual(dependencies['behalf-of-answer1'], {'gender-answer'})
        self.assertEqual(dependencies['behalf-of-answer2'], {'gender-answer'})
        self.assertEqual(dependencies['behalf-of-answer3'], {'gender-answer'})
