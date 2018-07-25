from app.data_model.answer_store import AnswerStore
from app.questionnaire.questionnaire_schema import QuestionnaireSchema
from app.questionnaire.location import Location
from app.submitter.converter import convert_answers
from tests.app.submitter.schema import make_schema
from tests.app.submitter.test_converter import TestConverter, create_answer


class TestConvertPayload002(TestConverter):  # pylint: disable=too-many-public-methods

    def test_convert_answers_to_payload_0_0_2(self):
        with self._app.test_request_context():
            routing_path = [Location(group_id='personal details', group_instance=0, block_id='about you'),
                            Location(group_id='household', group_instance=0, block_id='where you live'),
                            Location(group_id='household', group_instance=1, block_id='where you live')]
            answers = [create_answer('name', 'Joe Bloggs', group_id='personal details', block_id='about you'),
                       create_answer('name', 'Fred Bloggs', group_id='personal details', block_id='about you',
                                     answer_instance=1),
                       create_answer('address', '62 Somewhere', group_id='household', block_id='where you live'),
                       create_answer('address', '63 Somewhere', group_id='household', block_id='where you live',
                                     group_instance=1)]

            questionnaire = {
                'survey_id': '021',
                'data_version': '0.0.2',
                'sections': [
                    {
                        'id': 'household-section',
                        'groups': [
                            {
                                'id': 'personal details',
                                'blocks': [
                                    {
                                        'id': 'about you',
                                        'questions': [
                                            {
                                                'id': 'crisps-question',
                                                'answers': [
                                                    {
                                                        'id': 'name',
                                                        'type': 'TextField'
                                                    }
                                                ]
                                            }
                                        ]
                                    }
                                ]
                            },
                            {
                                'id': 'household',
                                'blocks': [
                                    {
                                        'id': 'where you live',
                                        'questions': [
                                            {
                                                'id': 'crisps-question',
                                                'answers': [
                                                    {
                                                        'id': 'address',
                                                        'type': 'TextField'
                                                    }
                                                ]
                                            }
                                        ]
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }

            # When
            answer_object = convert_answers(self.metadata, QuestionnaireSchema(questionnaire), AnswerStore(answers), routing_path)

            # Then
            self.assertEqual(len(answer_object['data']), 4)
            self.assertEqual(answer_object['data'][0]['group_instance'], 0)
            self.assertEqual(answer_object['data'][0]['answer_instance'], 0)
            self.assertEqual(answer_object['data'][0]['value'], 'Joe Bloggs')

            self.assertEqual(answer_object['data'][1]['group_instance'], 0)
            self.assertEqual(answer_object['data'][1]['answer_instance'], 1)
            self.assertEqual(answer_object['data'][1]['value'], 'Fred Bloggs')

            self.assertEqual(answer_object['data'][2]['group_instance'], 0)
            self.assertEqual(answer_object['data'][2]['answer_instance'], 0)
            self.assertEqual(answer_object['data'][2]['value'], '62 Somewhere')

            self.assertEqual(answer_object['data'][3]['group_instance'], 1)
            self.assertEqual(answer_object['data'][3]['answer_instance'], 0)
            self.assertEqual(answer_object['data'][3]['value'], '63 Somewhere')

    def test_convert_payload_0_0_2_multiple_answers(self):
        with self._app.test_request_context():
            routing_path = [Location(group_id='favourite-food', group_instance=0, block_id='crisps')]
            answers = [
                create_answer('crisps-answer', ['Ready salted', 'Sweet chilli'], group_id='favourite-food', block_id='crisps')]

            questionnaire = make_schema('0.0.2', 'section-1', 'favourite-food', 'crisps', [
                {
                    'id': 'crisps-question',
                    'answers': [
                        {
                            'id': 'crisps-answer',
                            'type': 'Checkbox',
                            'options': [
                                {
                                    'label': 'Ready salted',
                                    'value': 'Ready salted'
                                },
                                {
                                    'label': 'Sweet chilli',
                                    'value': 'Sweet chilli'
                                },
                                {
                                    'label': 'Cheese and onion',
                                    'value': 'Cheese and onion'
                                }
                            ]
                        }
                    ]
                }
            ])

            # When
            answer_object = convert_answers(self.metadata, QuestionnaireSchema(questionnaire), AnswerStore(answers), routing_path)

            # Then
            self.assertEqual(len(answer_object['data']), 1)
            self.assertEqual(answer_object['data'][0]['group_instance'], 0)
            self.assertEqual(answer_object['data'][0]['answer_instance'], 0)
            self.assertEqual(answer_object['data'][0]['value'], ['Ready salted', 'Sweet chilli'])

    def test_radio_answer(self):
        with self._app.test_request_context():
            routing_path = [Location(group_id='radio-group', group_instance=0, block_id='radio-block')]
            user_answer = [create_answer('radio-answer', 'Coffee', group_id='radio-group', block_id='radio-block')]

            questionnaire = make_schema('0.0.2', 'section-1', 'radio-group', 'radio-block', [
                {
                    'id': 'radio-question',
                    'answers': [
                        {
                            'type': 'Radio',
                            'id': 'radio-answer',
                            'options': [
                                {
                                    'label': 'Coffee',
                                    'value': 'Coffee'
                                },
                                {
                                    'label': 'Tea',
                                    'value': 'Tea'
                                }
                            ]
                        }
                    ]
                }
            ])

            # When
            answer_object = convert_answers(self.metadata, QuestionnaireSchema(questionnaire), AnswerStore(user_answer), routing_path)

            # Then
            self.assertEqual(len(answer_object['data']), 1)
            self.assertEqual(answer_object['data'][0]['value'], 'Coffee')
            self.assertEqual(answer_object['data'][0]['group_instance'], 0)
            self.assertEqual(answer_object['data'][0]['answer_instance'], 0)

    def test_number_answer(self):
        with self._app.test_request_context():
            routing_path = [Location(group_id='number-group', group_instance=0, block_id='number-block')]
            user_answer = [create_answer('number-answer', 1.755, group_id='number-group', block_id='number-block')]

            questionnaire = make_schema('0.0.2', 'section-1', 'number-group', 'number-block', [
                {
                    'id': 'number-question',
                    'answers': [
                        {
                            'id': 'number-answer',
                            'type': 'Number'
                        }
                    ]
                }
            ])

            # When
            answer_object = convert_answers(self.metadata, QuestionnaireSchema(questionnaire), AnswerStore(user_answer), routing_path)

            # Then
            self.assertEqual(len(answer_object['data']), 1)
            self.assertEqual(answer_object['data'][0]['value'], 1.755)
            self.assertEqual(answer_object['data'][0]['group_instance'], 0)
            self.assertEqual(answer_object['data'][0]['answer_instance'], 0)

    def test_percentage_answer(self):
        with self._app.test_request_context():
            routing_path = [Location(group_id='percentage-group', group_instance=0, block_id='percentage-block')]
            user_answer = [create_answer('percentage-answer', 99, group_id='percentage-group', block_id='percentage-block')]

            questionnaire = make_schema('0.0.2', 'section-1', 'percentage-group', 'percentage-block', [
                {
                    'id': 'percentage-question',
                    'answers': [
                        {
                            'id': 'percentage-answer',
                            'type': 'Percentage'
                        }
                    ]
                }
            ])

            # When
            answer_object = convert_answers(self.metadata, QuestionnaireSchema(questionnaire), AnswerStore(user_answer), routing_path)

            # Then
            self.assertEqual(len(answer_object['data']), 1)
            self.assertEqual(answer_object['data'][0]['value'], 99)
            self.assertEqual(answer_object['data'][0]['group_instance'], 0)
            self.assertEqual(answer_object['data'][0]['answer_instance'], 0)

    def test_textarea_answer(self):
        with self._app.test_request_context():
            routing_path = [Location(group_id='textarea-group', group_instance=0, block_id='textarea-block')]
            user_answer = [create_answer('textarea-answer', 'This is an example text!', group_id='textarea-group', block_id='textarea-block')]

            questionnaire = make_schema('0.0.2', 'section-1', 'textarea-group', 'textarea-block', [
                {
                    'id': 'textarea-question',
                    'answers': [
                        {
                            'id': 'textarea-answer',
                            'type': 'TextArea'
                        }
                    ]
                }
            ])

            # When
            answer_object = convert_answers(self.metadata, QuestionnaireSchema(questionnaire), AnswerStore(user_answer), routing_path)

            # Then
            self.assertEqual(len(answer_object['data']), 1)
            self.assertEqual(answer_object['data'][0]['value'], 'This is an example text!')
            self.assertEqual(answer_object['data'][0]['group_instance'], 0)
            self.assertEqual(answer_object['data'][0]['answer_instance'], 0)

    def test_currency_answer(self):
        with self._app.test_request_context():
            routing_path = [Location(group_id='currency-group', group_instance=0, block_id='currency-block')]
            user_answer = [create_answer('currency-answer', 100, group_id='currency-group', block_id='currency-block')]

            questionnaire = make_schema('0.0.2', 'section-1', 'currency-group', 'currency-block', [
                {
                    'id': 'currency-question',
                    'answers': [
                        {
                            'id': 'currency-answer',
                            'type': 'Currency'
                        }
                    ]
                }
            ])

            # When
            answer_object = convert_answers(self.metadata, QuestionnaireSchema(questionnaire), AnswerStore(user_answer), routing_path)

            # Then
            self.assertEqual(len(answer_object['data']), 1)
            self.assertEqual(answer_object['data'][0]['value'], 100)
            self.assertEqual(answer_object['data'][0]['group_instance'], 0)
            self.assertEqual(answer_object['data'][0]['answer_instance'], 0)

    def test_dropdown_answer(self):
        with self._app.test_request_context():
            routing_path = [Location(group_id='dropdown-group', group_instance=0, block_id='dropdown-block')]
            user_answer = [create_answer('dropdown-answer', 'Rugby is better!', group_id='dropdown-group', block_id='dropdown-block')]

            questionnaire = make_schema('0.0.2', 'section-1', 'dropdown-group', 'dropdown-block', [
                {
                    'id': 'dropdown-question',
                    'answers': [
                        {
                            'id': 'dropdown-answer',
                            'type': 'Dropdown',
                            'options': [
                                {
                                    'label': 'Liverpool',
                                    'value': 'Liverpool'
                                },
                                {
                                    'label': 'Chelsea',
                                    'value': 'Chelsea'
                                },
                                {
                                    'label': 'Rugby is better!',
                                    'value': 'Rugby is better!'
                                }
                            ]
                        }
                    ]
                }
            ])

            # When
            answer_object = convert_answers(self.metadata, QuestionnaireSchema(questionnaire), AnswerStore(user_answer), routing_path)

            # Then
            self.assertEqual(len(answer_object['data']), 1)
            self.assertEqual(answer_object['data'][0]['value'], 'Rugby is better!')
            self.assertEqual(answer_object['data'][0]['group_instance'], 0)
            self.assertEqual(answer_object['data'][0]['answer_instance'], 0)

    def test_date_answer(self):
        with self._app.test_request_context():
            routing_path = [Location(group_id='date-group', group_instance=0, block_id='date-block')]
            user_answer = [create_answer('single-date-answer', '01-01-1990', group_id='date-group', block_id='date-block'),
                           create_answer('month-year-answer', '01-1990', group_id='date-group', block_id='date-block')]

            questionnaire = make_schema('0.0.2', 'section-1', 'date-group', 'date-block', [
                {
                    'id': 'single-date-question',
                    'answers': [
                        {
                            'id': 'single-date-answer',
                            'type': 'Date'
                        }
                    ]
                },
                {
                    'id': 'month-year-question',
                    'answers': [
                        {
                            'id': 'month-year-answer',
                            'type': 'MonthYearDate'
                        }
                    ]
                }
            ])

            # When
            answer_object = convert_answers(self.metadata, QuestionnaireSchema(questionnaire), AnswerStore(user_answer), routing_path)

            # Then
            self.assertEqual(len(answer_object['data']), 2)
            self.assertEqual(answer_object['data'][0]['value'], '01-01-1990')
            self.assertEqual(answer_object['data'][0]['group_instance'], 0)
            self.assertEqual(answer_object['data'][0]['answer_instance'], 0)

            self.assertEqual(answer_object['data'][1]['value'], '01-1990')
            self.assertEqual(answer_object['data'][1]['group_instance'], 0)
            self.assertEqual(answer_object['data'][1]['answer_instance'], 0)

    def test_unit_answer(self):
        with self._app.test_request_context():
            routing_path = [Location(group_id='unit-group', group_instance=0, block_id='unit-block')]
            user_answer = [create_answer('unit-answer', 10, group_id='unit-group', block_id='unit-block')]

            questionnaire = make_schema('0.0.2', 'section-1', 'unit-group', 'unit-block', [
                {
                    'id': 'unit-question',
                    'answers': [
                        {
                            'id': 'unit-answer',
                            'type': 'Unit'
                        }
                    ]
                }
            ])

            # When
            answer_object = convert_answers(self.metadata, QuestionnaireSchema(questionnaire), AnswerStore(user_answer), routing_path)

            # Then
            self.assertEqual(len(answer_object['data']), 1)
            self.assertEqual(answer_object['data'][0]['value'], 10)
            self.assertEqual(answer_object['data'][0]['group_instance'], 0)
            self.assertEqual(answer_object['data'][0]['answer_instance'], 0)

    def test_relationship_answer(self):
        with self._app.test_request_context():
            routing_path = [Location(group_id='relationship-group', group_instance=0, block_id='relationship-block')]
            user_answer = [create_answer('relationship-answer', 'Unrelated', group_id='relationship-group', block_id='relationship-block'),
                           create_answer('relationship-answer', 'Partner', group_id='relationship-group', block_id='relationship-block',
                                         answer_instance=1),
                           create_answer('relationship-answer', 'Husband or wife', group_id='relationship-group', block_id='relationship-block',
                                         answer_instance=2)]

            questionnaire = make_schema('0.0.2', 'section-1', 'relationship-group', 'relationship-block', [
                {
                    'id': 'relationship-question',
                    'type': 'Relationship',
                    'answers': [
                        {
                            'id': 'relationship-answer',
                            'q_code': '1',
                            'type': 'Relationship',
                            'options': [
                                {
                                    'label': 'Husband or wife',
                                    'value': 'Husband or wife'
                                },
                                {
                                    'label': 'Partner',
                                    'value': 'Partner'
                                },
                                {
                                    'label': 'Unrelated',
                                    'value': 'Unrelated'
                                }
                            ]
                        }
                    ]
                }
            ])

            # When
            answer_object = convert_answers(self.metadata, QuestionnaireSchema(questionnaire), AnswerStore(user_answer), routing_path)

            # Then
            self.assertEqual(len(answer_object['data']), 3)
            self.assertEqual(answer_object['data'][0]['value'], 'Unrelated')

            self.assertEqual(answer_object['data'][0]['group_instance'], 0)
            self.assertEqual(answer_object['data'][0]['answer_instance'], 0)

            self.assertEqual(answer_object['data'][1]['value'], 'Partner')
            self.assertEqual(answer_object['data'][1]['group_instance'], 0)
            self.assertEqual(answer_object['data'][1]['answer_instance'], 1)

            self.assertEqual(answer_object['data'][2]['value'], 'Husband or wife')
            self.assertEqual(answer_object['data'][2]['group_instance'], 0)
            self.assertEqual(answer_object['data'][2]['answer_instance'], 2)
