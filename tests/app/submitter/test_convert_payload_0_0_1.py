from app.data_model.answer_store import AnswerStore
from app.questionnaire.location import Location
from app.questionnaire.questionnaire_schema import QuestionnaireSchema
from app.submitter.convert_payload_0_0_1 import convert_answers_to_payload_0_0_1
from app.submitter.converter import convert_answers
from tests.app.submitter.schema import make_schema
from tests.app.submitter.test_converter import TestConverter, create_answer


class TestConvertPayload001(TestConverter):  # pylint: disable=too-many-public-methods

    def test_convert_answers_to_payload_0_0_1_with_key_error(self):
        with self._app.test_request_context():
            user_answer = [create_answer('ABC', '2016-01-01', group_id='group-1', block_id='block-1'),
                           create_answer('DEF', '2016-03-30', group_id='group-1', block_id='block-1'),
                           create_answer('GHI', '2016-05-30', group_id='group-1', block_id='block-1')]

            questionnaire = make_schema('0.0.1', 'section-1', 'group-1', 'block-1', [
                {
                    'id': 'question-1',
                    'answers': [
                        {
                            'id': 'LMN',
                            'type': 'TextField',
                            'q_code': '001'
                        },
                        {
                            'id': 'DEF',
                            'type': 'TextField',
                            'q_code': '002'
                        },
                        {
                            'id': 'JKL',
                            'type': 'TextField',
                            'q_code': '003'
                        }
                    ]
                }
            ])

            routing_path = [Location(group_id='group-1', group_instance=0, block_id='block-1')]
            answer_object = (convert_answers_to_payload_0_0_1(AnswerStore(user_answer), QuestionnaireSchema(questionnaire), routing_path))
            self.assertEqual(answer_object['002'], '2016-03-30')
            self.assertEqual(len(answer_object), 1)

    def test_answer_with_zero(self):
        with self._app.test_request_context():
            user_answer = [create_answer('GHI', 0, group_id='group-1', block_id='block-1')]

            questionnaire = make_schema('0.0.1', 'section-1', 'group-1', 'block-1', [
                {
                    'id': 'question-2',
                    'answers': [
                        {
                            'id': 'GHI',
                            'type': 'TextField',
                            'q_code': '003'
                        }
                    ]
                }
            ])

            routing_path = [Location(group_id='group-1', group_instance=0, block_id='block-1')]

            answer_object = convert_answers(self.metadata, self.collection_metadata, QuestionnaireSchema(questionnaire), AnswerStore(user_answer), routing_path)

            # Check the converter correctly
            self.assertEqual('0', answer_object['data']['003'])

    def test_answer_with_float(self):
        with self._app.test_request_context():
            user_answer = [create_answer('GHI', 10.02, group_id='group-1', block_id='block-1')]

            questionnaire = make_schema('0.0.1', 'section-1', 'group-1', 'block-1', [
                {
                    'id': 'question-2',
                    'answers': [
                        {
                            'id': 'GHI',
                            'type': 'TextField',
                            'q_code': '003'
                        }
                    ]
                }
            ])

            routing_path = [Location(group_id='group-1', group_instance=0, block_id='block-1')]

            answer_object = convert_answers(self.metadata, self.collection_metadata, QuestionnaireSchema(questionnaire), AnswerStore(user_answer), routing_path)

            # Check the converter correctly
            self.assertEqual('10.02', answer_object['data']['003'])

    def test_answer_with_string(self):
        with self._app.test_request_context():
            user_answer = [create_answer('GHI', 'String test + !', group_id='group-1', block_id='block-1')]

            questionnaire = make_schema('0.0.1', 'section-1', 'group-1', 'block-1', [
                {
                    'id': 'question-2',
                    'answers': [
                        {
                            'id': 'GHI',
                            'type': 'TextField',
                            'q_code': '003'
                        }
                    ]
                }
            ])

            routing_path = [Location(group_id='group-1', group_instance=0, block_id='block-1')]

            answer_object = convert_answers(self.metadata, self.collection_metadata, QuestionnaireSchema(questionnaire), AnswerStore(user_answer), routing_path)

            # Check the converter correctly
            self.assertEqual('String test + !', answer_object['data']['003'])

    def test_answer_with_multiple_instances(self):
        with self._app.test_request_context():
            user_answer = [create_answer('GHI', 0, group_id='group-1', block_id='block-1'),
                           create_answer('GHI', value=1, answer_instance=1, group_id='group-1', block_id='block-1'),
                           create_answer('GHI', value=2, answer_instance=2, group_id='group-1', block_id='block-1')]

            questionnaire = make_schema('0.0.1', 'section-1', 'group-1', 'block-1', [
                {
                    'id': 'question-2',
                    'answers': [
                        {
                            'id': 'GHI',
                            'type': 'TextField',
                            'q_code': '003'
                        }
                    ]
                }
            ])

            routing_path = [Location(group_id='group-1', group_instance=0, block_id='block-1')]

            answer_object = convert_answers(self.metadata, self.collection_metadata, QuestionnaireSchema(questionnaire), AnswerStore(user_answer), routing_path)

            # Check the converter correctly
            self.assertEqual(answer_object['data']['003'], ['0', '1', '2'])

    def test_answer_without_qcode(self):
        with self._app.test_request_context():
            user_answer = [create_answer('GHI', 'String test + !', group_id='group-1', block_id='block-1')]

            questionnaire = make_schema('0.0.1', 'section-1', 'group-1', 'block-1', [
                {
                    'id': 'question-2',
                    'answers': [
                        {
                            'id': 'GHI',
                            'type': 'TextField'
                        }
                    ]
                }
            ])

            routing_path = [Location(group_id='group-1', group_instance=0, block_id='block-1')]

            answer_object = convert_answers(self.metadata, self.collection_metadata, QuestionnaireSchema(questionnaire), AnswerStore(user_answer), routing_path)

            self.assertEqual(len(answer_object['data']), 0)

    def test_get_checkbox_answer_with_duplicate_child_answer_ids(self):
        with self._app.test_request_context():
            routing_path = [Location(group_id='favourite-food', group_instance=0, block_id='crisps')]
            answers = [create_answer('crisps-answer', [
                'Ready salted',
                'Other'
            ], group_id='favourite-food', block_id='crisps')]

            answers += [create_answer('other-answer-mandatory', 'Other', group_id='favourite-food', block_id='crisps',
                                      group_instance=1)]
            answers += [create_answer('other-answer-mandatory', 'Other', group_id='favourite-food', block_id='crisps',
                                      group_instance=1)]

            questionnaire = make_schema('0.0.1', 'section-1', 'favourite-food', 'crisps', [
                {
                    'id': 'crisps-question',
                    'answers': [
                        {
                            'id': 'crisps-answer',
                            'type': 'Checkbox',
                            'options': [
                                {
                                    'label': 'Other',
                                    'q_code': '4',
                                    'description': 'Choose any other flavour',
                                    'value': 'Other',
                                    'child_answer_id': 'other-answer-mandatory'
                                }
                            ]
                        }
                    ]
                }
            ])

        with self.assertRaises(Exception) as err:
            convert_answers(self.metadata, self.collection_metadata, QuestionnaireSchema(questionnaire), AnswerStore(answers), routing_path)
        self.assertEqual('Multiple answers found for {}'.format('other-answer-mandatory'), str(err.exception))

    def test_converter_checkboxes_with_q_codes(self):
        with self._app.test_request_context():
            routing_path = [Location(group_id='favourite-food', group_instance=0, block_id='crisps')]
            answers = [create_answer('crisps-answer', [
                'Ready salted',
                'Sweet chilli'
            ], group_id='favourite-food', block_id='crisps')]

            questionnaire = make_schema('0.0.1', 'section-1', 'favourite-food', 'crisps', [
                {
                    'id': 'crisps-question',
                    'answers': [
                        {
                            'id': 'crisps-answer',
                            'type': 'Checkbox',
                            'options': [
                                {
                                    'label': 'Ready salted',
                                    'value': 'Ready salted',
                                    'q_code': '1'
                                },
                                {
                                    'label': 'Sweet chilli',
                                    'value': 'Sweet chilli',
                                    'q_code': '2'
                                },
                                {
                                    'label': 'Cheese and onion',
                                    'value': 'Cheese and onion',
                                    'q_code': '3'
                                },
                                {
                                    'label': 'Other',
                                    'q_code': '4',
                                    'description': 'Choose any other flavour',
                                    'value': 'Other',
                                    'child_answer_id': 'other-answer-mandatory'
                                }
                            ]
                        },
                        {
                            'parent_answer_id': 'crisps-answer',
                            'mandatory': True,
                            'id': 'other-answer-mandatory',
                            'label': 'Please specify other',
                            'type': 'TextField'
                        }
                    ]
                }
            ])

            # When
            answer_object = convert_answers(self.metadata, self.collection_metadata, QuestionnaireSchema(questionnaire), AnswerStore(answers), routing_path)

            # Then
            self.assertEqual(len(answer_object['data']), 2)
            self.assertEqual(answer_object['data']['1'], 'Ready salted')
            self.assertEqual(answer_object['data']['2'], 'Sweet chilli')

    def test_converter_checkboxes_with_q_codes_and_other_value(self):
        with self._app.test_request_context():
            routing_path = [Location(group_id='favourite-food', group_instance=0, block_id='crisps')]
            answers = [create_answer('crisps-answer', [
                'Ready salted',
                'Other'
            ], group_id='favourite-food', block_id='crisps')]

            answers += [create_answer('other-answer-mandatory', 'Bacon', group_id='favourite-food', block_id='crisps')]

            questionnaire = make_schema('0.0.1', 'section-1', 'favourite-food', 'crisps', [
                {
                    'id': 'crisps-question',
                    'answers': [
                        {
                            'id': 'crisps-answer',
                            'type': 'Checkbox',
                            'options': [
                                {
                                    'label': 'Ready salted',
                                    'value': 'Ready salted',
                                    'q_code': '1'
                                },
                                {
                                    'label': 'Sweet chilli',
                                    'value': 'Sweet chilli',
                                    'q_code': '2'
                                },
                                {
                                    'label': 'Cheese and onion',
                                    'value': 'Cheese and onion',
                                    'q_code': '3'
                                },
                                {
                                    'label': 'Other',
                                    'q_code': '4',
                                    'description': 'Choose any other flavour',
                                    'value': 'Other',
                                    'child_answer_id': 'other-answer-mandatory'
                                }
                            ]
                        },
                        {
                            'parent_answer_id': 'crisps-answer',
                            'mandatory': True,
                            'id': 'other-answer-mandatory',
                            'label': 'Please specify other',
                            'type': 'TextField'
                        }
                    ]
                }
            ])

            # When
            answer_object = convert_answers(self.metadata, self.collection_metadata, QuestionnaireSchema(questionnaire), AnswerStore(answers), routing_path)

            # Then
            self.assertEqual(len(answer_object['data']), 2)
            self.assertEqual(answer_object['data']['1'], 'Ready salted')
            self.assertEqual(answer_object['data']['4'], 'Bacon')

    def test_converter_checkboxes_with_q_codes_and_empty_other_value(self):
        with self._app.test_request_context():
            routing_path = [Location(group_id='favourite-food', group_instance=0, block_id='crisps')]
            answers = [create_answer('crisps-answer', [
                'Ready salted',
                'Other'
            ], group_id='favourite-food', block_id='crisps')]

            answers += [create_answer('other-answer-mandatory', '', group_id='favourite-food', block_id='crisps')]

            questionnaire = make_schema('0.0.1', 'section-1', 'favourite-food', 'crisps', [
                {
                    'id': 'crisps-question',
                    'answers': [
                        {
                            'id': 'crisps-answer',
                            'type': 'Checkbox',
                            'options': [
                                {
                                    'label': 'Ready salted',
                                    'value': 'Ready salted',
                                    'q_code': '1'
                                },
                                {
                                    'label': 'Sweet chilli',
                                    'value': 'Sweet chilli',
                                    'q_code': '2'
                                },
                                {
                                    'label': 'Cheese and onion',
                                    'value': 'Cheese and onion',
                                    'q_code': '3'
                                },
                                {
                                    'label': 'Other',
                                    'q_code': '4',
                                    'description': 'Choose any other flavour',
                                    'value': 'Other',
                                    'child_answer_id': 'other-answer-mandatory'
                                }
                            ]
                        },
                        {
                            'parent_answer_id': 'crisps-answer',
                            'mandatory': True,
                            'id': 'other-answer-mandatory',
                            'label': 'Please specify other',
                            'type': 'TextField'
                        }
                    ]
                }
            ])

            # When
            answer_object = convert_answers(self.metadata, self.collection_metadata, QuestionnaireSchema(questionnaire), AnswerStore(answers), routing_path)

            # Then
            self.assertEqual(len(answer_object['data']), 2)
            self.assertEqual(answer_object['data']['1'], 'Ready salted')
            self.assertEqual(answer_object['data']['4'], 'Other')

    def test_converter_q_codes_for_empty_strings(self):
        with self._app.test_request_context():
            routing_path = [Location(group_id='favourite-food', group_instance=0, block_id='crisps')]
            answers = [create_answer('crisps-answer', '', group_id='favourite-food', block_id='crisps')]
            answers += [
                create_answer('other-crisps-answer', 'Ready salted', group_id='favourite-food', block_id='crisps')]

            questionnaire = make_schema('0.0.1', 'section-1', 'favourite-food', 'crisps', [
                {
                    'id': 'crisps-question',
                    'answers': [
                        {
                            'id': 'crisps-answer',
                            'type': 'TextArea',
                            'options': [],
                            'q_code': '1'
                        },
                        {
                            'id': 'other-crisps-answer',
                            'type': 'TextArea',
                            'options': [],
                            'q_code': '2'
                        }
                    ]
                }
            ])

            # When
            answer_object = convert_answers(self.metadata, self.collection_metadata, QuestionnaireSchema(questionnaire), AnswerStore(answers), routing_path)

            # Then
            self.assertEqual(len(answer_object['data']), 1)
            self.assertEqual(answer_object['data']['2'], 'Ready salted')

    def test_radio_answer(self):
        with self._app.test_request_context():
            routing_path = [Location(group_id='radio-group', group_instance=0, block_id='radio-block')]
            user_answer = [create_answer('radio-answer', 'Coffee', group_id='radio-group', block_id='radio-block')]

            questionnaire = make_schema('0.0.1', 'section-1', 'radio-block', 'radio-block', [
                {
                    'id': 'radio-question',
                    'answers': [
                        {
                            'type': 'Radio',
                            'id': 'radio-answer',
                            'q_code': '1',
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
            answer_object = convert_answers(self.metadata, self.collection_metadata, QuestionnaireSchema(questionnaire), AnswerStore(user_answer), routing_path)

            # Then
            self.assertEqual(len(answer_object['data']), 1)
            self.assertEqual(answer_object['data']['1'], 'Coffee')

    def test_number_answer(self):
        with self._app.test_request_context():
            routing_path = [Location(group_id='number-group', group_instance=0, block_id='number-block')]
            user_answer = [create_answer('number-answer', 0.9999, group_id='number-block', block_id='number-block')]

            questionnaire = make_schema('0.0.1', 'section-1', 'number-block', 'number-block', [
                {
                    'id': 'number-question',
                    'answers': [
                        {
                            'id': 'number-answer',
                            'type': 'Number',
                            'q_code': '1'
                        }
                    ]
                }
            ])

            # When
            answer_object = convert_answers(self.metadata, self.collection_metadata, QuestionnaireSchema(questionnaire), AnswerStore(user_answer), routing_path)

            # Then
            self.assertEqual(len(answer_object['data']), 1)
            self.assertEqual(answer_object['data']['1'], '0.9999')

    def test_percentage_answer(self):
        with self._app.test_request_context():
            routing_path = [Location(group_id='percentage-group', group_instance=0, block_id='percentage-block')]
            user_answer = [create_answer('percentage-answer', 100, group_id='percentage-group', block_id='percentage-block')]

            questionnaire = make_schema('0.0.1', 'section-1', 'percentage-block', 'percentage-block', [
                {
                    'id': 'percentage-question',
                    'answers': [
                        {
                            'id': 'percentage-answer',
                            'type': 'Percentage',
                            'q_code': '1'
                        }
                    ]
                }
            ])

            # When
            answer_object = convert_answers(self.metadata, self.collection_metadata, QuestionnaireSchema(questionnaire), AnswerStore(user_answer), routing_path)

            # Then
            self.assertEqual(len(answer_object['data']), 1)
            self.assertEqual(answer_object['data']['1'], '100')

    def test_textarea_answer(self):
        with self._app.test_request_context():
            routing_path = [Location(group_id='textarea-group', group_instance=0, block_id='textarea-block')]
            user_answer = [create_answer('textarea-answer', 'example text.', group_id='textarea-group', block_id='textarea-block')]

            questionnaire = make_schema('0.0.1', 'section-1', 'textarea-block', 'textarea-block', [
                {
                    'id': 'textarea-question',
                    'answers': [
                        {
                            'id': 'textarea-answer',
                            'q_code': '1',
                            'type': 'TextArea'
                        }
                    ]
                }
            ])

            # When
            answer_object = convert_answers(self.metadata, self.collection_metadata, QuestionnaireSchema(questionnaire), AnswerStore(user_answer), routing_path)

            # Then
            self.assertEqual(len(answer_object['data']), 1)
            self.assertEqual(answer_object['data']['1'], 'example text.')

    def test_currency_answer(self):
        with self._app.test_request_context():
            routing_path = [Location(group_id='currency-group', group_instance=0, block_id='currency-block')]
            user_answer = [create_answer('currency-answer', 99.99, group_id='currency-group', block_id='currency-block')]

            questionnaire = make_schema('0.0.1', 'section-1', 'currency-block', 'currency-block', [
                {
                    'id': 'currency-question',
                    'answers': [
                        {
                            'id': 'currency-answer',
                            'type': 'Currency',
                            'q_code': '1'
                        }
                    ]
                }
            ])

            # When
            answer_object = convert_answers(self.metadata, self.collection_metadata, QuestionnaireSchema(questionnaire), AnswerStore(user_answer), routing_path)

            # Then
            self.assertEqual(len(answer_object['data']), 1)
            self.assertEqual(answer_object['data']['1'], '99.99')

    def test_dropdown_answer(self):
        with self._app.test_request_context():
            routing_path = [Location(group_id='dropdown-group', group_instance=0, block_id='dropdown-block')]
            user_answer = [create_answer('dropdown-answer', 'Liverpool', group_id='dropdown-group', block_id='dropdown-block')]

            questionnaire = make_schema('0.0.1', 'section-1', 'dropdown-block', 'dropdown-block', [
                {
                    'id': 'dropdown-question',
                    'answers': [
                        {
                            'id': 'dropdown-answer',
                            'type': 'Dropdown',
                            'q_code': '1',
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
            answer_object = convert_answers(self.metadata, self.collection_metadata, QuestionnaireSchema(questionnaire), AnswerStore(user_answer), routing_path)

            # Then
            self.assertEqual(len(answer_object['data']), 1)
            self.assertEqual(answer_object['data']['1'], 'Liverpool')

    def test_date_answer(self):
        with self._app.test_request_context():
            routing_path = [Location(group_id='date-group', group_instance=0, block_id='date-block')]
            user_answer = [create_answer('single-date-answer', '1990-02-01', group_id='date-group', block_id='date-block'),
                           create_answer('month-year-answer', '1990-01', group_id='date-group', block_id='date-block')]

            questionnaire = make_schema('0.0.1', 'section-1', 'date-block', 'date-block', [
                {
                    'id': 'single-date-question',
                    'answers': [
                        {
                            'id': 'single-date-answer',
                            'type': 'Date',
                            'q_code': '1'
                        }
                    ]
                },
                {
                    'id': 'month-year-question',
                    'answers': [
                        {
                            'id': 'month-year-answer',
                            'type': 'MonthYearDate',
                            'q_code': '2'
                        }
                    ]
                }
            ])
            # When
            answer_object = convert_answers(self.metadata, self.collection_metadata, QuestionnaireSchema(questionnaire), AnswerStore(user_answer), routing_path)

            # Then
            self.assertEqual(len(answer_object['data']), 2)
            self.assertEqual(answer_object['data']['1'], '01/02/1990')
            self.assertEqual(answer_object['data']['2'], '01/1990')

    def test_unit_answer(self):
        with self._app.test_request_context():
            routing_path = [Location(group_id='unit-group', group_instance=0, block_id='unit-block')]
            user_answer = [create_answer('unit-answer', 10, group_id='unit-group', block_id='unit-block')]

            questionnaire = make_schema('0.0.1', 'section-1', 'unit-block', 'unit-block', [
                {
                    'id': 'unit-question',
                    'answers': [
                        {
                            'id': 'unit-answer',
                            'type': 'Unit',
                            'q_code': '1'
                        }
                    ]
                }
            ])

            # When
            answer_object = convert_answers(self.metadata, self.collection_metadata, QuestionnaireSchema(questionnaire), AnswerStore(user_answer), routing_path)

            # Then
            self.assertEqual(len(answer_object['data']), 1)
            self.assertEqual(answer_object['data']['1'], '10')

    def test_relationship_answer(self):
        with self._app.test_request_context():
            routing_path = [Location(group_id='relationship-group', group_instance=0, block_id='relationship-block')]
            user_answer = [create_answer('relationship-answer', 'Unrelated', group_id='relationship-group', block_id='relationship-block'),
                           create_answer('relationship-answer', 'Partner', group_id='relationship-group', block_id='relationship-block',
                                         answer_instance=1),
                           create_answer('relationship-answer', 'Husband or wife', group_id='relationship-group', block_id='relationship-block',
                                         answer_instance=2)]

            questionnaire = make_schema('0.0.1', 'section-1', 'relationship-block', 'relationship-block', [
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
            answer_object = convert_answers(self.metadata, self.collection_metadata, QuestionnaireSchema(questionnaire), AnswerStore(user_answer), routing_path)

            # Then
            self.assertEqual(len(answer_object['data']), 1)
            self.assertEqual(answer_object['data']['1'], ['Unrelated', 'Partner', 'Husband or wife'])
