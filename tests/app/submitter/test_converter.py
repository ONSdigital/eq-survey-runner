from datetime import datetime, timedelta, timezone

import dateutil.parser

from app.data_model.answer_store import AnswerStore
from app.questionnaire.location import Location
from app.storage.metadata_parser import parse_metadata
from app.submitter.converter import convert_answers, DataVersionError
from tests.app.framework.survey_runner_test_case import SurveyRunnerTestCase

metadata = parse_metadata({
    "user_id": "789473423",
    "form_type": "0205",
    "collection_exercise_sid": "test-sid",
    "eq_id": "1",
    "period_id": "2016-02-01",
    "period_str": "2016-01-01",
    "ref_p_start_date": "2016-02-02",
    "ref_p_end_date": "2016-03-03",
    "ru_ref": "432423423423",
    "ru_name": "Apple",
    "return_by": "2016-07-07"
})


class TestConverter(SurveyRunnerTestCase):
    def test_convert_answers_flushed_flag_default_is_false(self):
        with self.application.test_request_context():
            user_answer = [create_answer('GHI', 0)]

            questionnaire = {
                "survey_id": "021",
                "data_version": "0.0.2"
            }

            answer_object = convert_answers(metadata, questionnaire, AnswerStore(user_answer), {})

            self.assertFalse(answer_object['flushed'])

    def test_convert_answers_flushed_flag_overriden_to_true(self):
        with self.application.test_request_context():
            user_answer = [create_answer('GHI', 0)]

            questionnaire = {
                "survey_id": "021",
                "data_version": "0.0.2"
            }

            answer_object = convert_answers(metadata, questionnaire, AnswerStore(user_answer), {}, flushed=True)

            self.assertTrue(answer_object['flushed'])

    def test_convert_answers(self):
        with self.application.test_request_context():
            user_answer = [create_answer('ABC', '2016-01-01', group_id='group-1', block_id='block-1'),
                           create_answer('DEF', '2016-03-30', group_id='group-1', block_id='block-1')]

            questionnaire = {
                "survey_id": "021",
                "data_version": "0.0.1",
                "groups": [
                    {
                        "id": "group-1",
                        "blocks": [
                            {
                                "id": "block-1",
                                "sections": [
                                    {
                                        "questions": [{
                                            "id": 'question-1',
                                            "answers": [
                                                {
                                                    "id": "ABC",
                                                    "type": "TextField",
                                                    "q_code": "001"
                                                }, {
                                                    "id": "DEF",
                                                    "type": "TextField",
                                                    "q_code": "002"
                                                }
                                            ]
                                        }]
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }

            routing_path = [Location(group_id='group-1', group_instance=0, block_id='block-1')]
            answer_object = convert_answers(metadata, questionnaire, AnswerStore(user_answer), routing_path)

            self.assertEqual(answer_object['type'], 'uk.gov.ons.edc.eq:surveyresponse')
            self.assertEqual(answer_object['version'], '0.0.1')
            self.assertEqual(answer_object['origin'], 'uk.gov.ons.edc.eq')
            self.assertEqual(answer_object['survey_id'], '021')
            self.assertEqual(answer_object['collection']['exercise_sid'], metadata['collection_exercise_sid'])
            self.assertEqual(answer_object['collection']['instrument_id'], metadata['form_type'])
            self.assertEqual(answer_object['collection']['period'], metadata['period_id'])
            self.assertEqual(answer_object['metadata']['user_id'], metadata['user_id'])
            self.assertEqual(answer_object['metadata']['ru_ref'], metadata['ru_ref'])
            self.assertEqual(answer_object['data']['001'], '2016-01-01')
            self.assertEqual(answer_object['data']['002'], '2016-03-30')

    def test_submitted_at_should_be_set_in_payload(self):
        with self.application.test_request_context():
            user_answer = [create_answer('GHI', 0)]

            questionnaire = {
                "survey_id": "021",
                "data_version": "0.0.2"
            }

            answer_object = convert_answers(metadata, questionnaire, AnswerStore(user_answer), {})

            self.assertLess(datetime.now(timezone.utc) - dateutil.parser.parse(answer_object['submitted_at']), timedelta(seconds=5))

    def test_answer_with_zero(self):
        with self.application.test_request_context():
            user_answer = [create_answer('GHI', 0, group_id='group-1', block_id='block-1')]

            questionnaire = {
                "survey_id": "021",
                "data_version": "0.0.1",
                "groups": [
                    {
                        "id": "group-1",
                        "blocks": [
                            {
                                "id": "block-1",
                                "sections": [
                                    {
                                        "questions": [{
                                            "id": 'question-2',
                                            "answers": [
                                                {
                                                    "id": "GHI",
                                                    "type": "TextField",
                                                    "q_code": "003"
                                                }
                                            ]
                                        }]
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }

            routing_path = [Location(group_id='group-1', group_instance=0, block_id='block-1')]

            answer_object = convert_answers(metadata, questionnaire, AnswerStore(user_answer), routing_path)

            # Check the converter correctly
            self.assertEqual("0", answer_object["data"]["003"])

    def test_answer_with_multiple_instances(self):
        with self.application.test_request_context():
            user_answer = [create_answer('GHI', 0, group_id='group-1', block_id='block-1'),
                           create_answer('GHI', value=1, answer_instance=1, group_id='group-1', block_id='block-1'),
                           create_answer('GHI', value=2, answer_instance=2, group_id='group-1', block_id='block-1')]

            questionnaire = {
                "survey_id": "021",
                "data_version": "0.0.1",
                "groups": [
                    {
                        "id": "group-1",
                        "blocks": [
                            {
                                "id": "block-1",
                                "sections": [
                                    {
                                        "questions": [{
                                            "id": 'question-2',
                                            "answers": [
                                                {
                                                    "id": "GHI",
                                                    "type": "TextField",
                                                    "q_code": "003"
                                                }
                                            ]
                                        }]
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }

            routing_path = [Location(group_id='group-1', group_instance=0, block_id='block-1')]

            answer_object = convert_answers(metadata, questionnaire, AnswerStore(user_answer), routing_path)

            # Check the converter correctly
            self.assertEqual(answer_object["data"]["003"], ['0', '1', '2'])

    def test_convert_census_answers(self):
        with self.application.test_request_context():
            routing_path = [Location(group_id='personal details', group_instance=0, block_id='about you'),
                            Location(group_id='household', group_instance=0, block_id='where you live'),
                            Location(group_id='household', group_instance=1, block_id='where you live')]
            answers = [create_answer('name', 'Joe Bloggs', group_id='personal details', block_id='about you'),
                       create_answer('name', 'Fred Bloggs', group_id='personal details', block_id='about you', answer_instance=1),
                       create_answer('address', '62 Somewhere', group_id='household', block_id='where you live'),
                       create_answer('address', '63 Somewhere', group_id='household', block_id='where you live', group_instance=1)]

            questionnaire = {
                "survey_id": "021",
                "data_version": "0.0.2"
            }

            # When
            answer_object = convert_answers(metadata, questionnaire, AnswerStore(answers), routing_path)

            # Then
            self.assertEqual(len(answer_object['data']), 4)
            self.assertEqual(answer_object['data'][0]['group_id'], 'personal details')
            self.assertEqual(answer_object['data'][0]['group_instance'], 0)
            self.assertEqual(answer_object['data'][0]['block_id'], 'about you')
            self.assertEqual(answer_object['data'][0]['answer_instance'], 0)
            self.assertEqual(answer_object['data'][0]['value'], 'Joe Bloggs')
            self.assertEqual(answer_object['data'][1]['group_id'], 'personal details')
            self.assertEqual(answer_object['data'][1]['group_instance'], 0)
            self.assertEqual(answer_object['data'][1]['block_id'], 'about you')
            self.assertEqual(answer_object['data'][1]['answer_instance'], 1)
            self.assertEqual(answer_object['data'][1]['value'], 'Fred Bloggs')
            self.assertEqual(answer_object['data'][2]['group_id'], 'household')
            self.assertEqual(answer_object['data'][2]['group_instance'], 0)
            self.assertEqual(answer_object['data'][2]['block_id'], 'where you live')
            self.assertEqual(answer_object['data'][2]['answer_instance'], 0)
            self.assertEqual(answer_object['data'][2]['value'], '62 Somewhere')
            self.assertEqual(answer_object['data'][3]['group_id'], 'household')
            self.assertEqual(answer_object['data'][3]['group_instance'], 1)
            self.assertEqual(answer_object['data'][3]['block_id'], 'where you live')
            self.assertEqual(answer_object['data'][3]['answer_instance'], 0)
            self.assertEqual(answer_object['data'][3]['value'], '63 Somewhere')

    def test_convert_census_answers_multiple_answers(self):
        with self.application.test_request_context():
            routing_path = [Location(group_id='favourite-food', group_instance=0, block_id='crisps')]
            answers = [create_answer('name', ['Ready salted', 'Sweet chilli'], group_id='favourite-food', block_id='crisps')]

            questionnaire = {
                "survey_id": "021",
                "data_version": "0.0.2"
            }

            # When
            answer_object = convert_answers(metadata, questionnaire, AnswerStore(answers), routing_path)

            # Then
            self.assertEqual(len(answer_object['data']), 1)
            self.assertEqual(answer_object['data'][0]['group_id'], 'favourite-food')
            self.assertEqual(answer_object['data'][0]['group_instance'], 0)
            self.assertEqual(answer_object['data'][0]['block_id'], 'crisps')
            self.assertEqual(answer_object['data'][0]['answer_instance'], 0)
            self.assertEqual(answer_object['data'][0]['value'], ['Ready salted', 'Sweet chilli'])

    def test_converter_raises_runtime_error_for_unsupported_version(self):
        with self.application.test_request_context():

            questionnaire = {
                "survey_id": "021",
                "data_version": "-0.0.1"
            }

            with self.assertRaises(DataVersionError) as err:
                convert_answers(metadata, questionnaire, AnswerStore(), {})

            self.assertEqual(str(err.exception), 'Data version -0.0.1 not supported')

    def test_converter_checkboxes_with_q_codes(self):
        with self.application.test_request_context():
            routing_path = [Location(group_id='favourite-food', group_instance=0, block_id='crisps')]
            answers = [create_answer('crisps-answer', [
                'Ready salted',
                'Sweet chilli'
            ], group_id='favourite-food', block_id='crisps')]

            questionnaire = {
                "survey_id": "999",
                "data_version": "0.0.1",
                "groups": [
                    {
                        "id": "favourite-food",
                        "blocks": [
                            {
                                "id": "crisps",
                                "sections": [
                                    {
                                        "questions": [{
                                            "id": 'crisps-question',
                                            "answers": [
                                                {
                                                    "id": "crisps-answer",
                                                    "type": "Checkbox",
                                                    "options": [
                                                        {
                                                            "label": "Ready salted",
                                                            "value": "Ready salted",
                                                            "q_code": "1"
                                                        },
                                                        {
                                                            "label": "Sweet chilli",
                                                            "value": "Sweet chilli",
                                                            "q_code": "2"
                                                        },
                                                        {
                                                            "label": "Cheese and onion",
                                                            "value": "Cheese and onion",
                                                            "q_code": "3"
                                                        },
                                                        {
                                                            "label": "Other",
                                                            "q_code": "4",
                                                            "description": "Choose any other flavour",
                                                            "value": "Other",
                                                            "child_answer_id": "other-answer-mandatory"
                                                        }
                                                    ]
                                                },
                                                {
                                                    "parent_answer_id": "crisps-answer",
                                                    "mandatory": True,
                                                    "id": "other-answer-mandatory",
                                                    "label": "Please specify other",
                                                    "type": "TextField"
                                                }
                                            ]
                                        }]
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }

            # When
            answer_object = convert_answers(metadata, questionnaire, AnswerStore(answers), routing_path)

            # Then
            self.assertEqual(len(answer_object['data']), 2)
            self.assertEqual(answer_object['data']['1'], 'Ready salted')
            self.assertEqual(answer_object['data']['2'], 'Sweet chilli')

    def test_converter_checkboxes_with_q_codes_and_other_value(self):
        with self.application.test_request_context():
            routing_path = [Location(group_id='favourite-food', group_instance=0, block_id='crisps')]
            answers = [create_answer('crisps-answer', [
                'Ready salted',
                'Other'
            ], group_id='favourite-food', block_id='crisps')]

            answers += [create_answer('other-answer-mandatory', 'Bacon', group_id='favourite-food', block_id='crisps')]

            questionnaire = {
                "survey_id": "999",
                "data_version": "0.0.1",
                "groups": [
                    {
                        "id": "favourite-food",
                        "blocks": [
                            {
                                "id": "crisps",
                                "sections": [
                                    {
                                        "questions": [{
                                            "id": 'crisps-question',
                                            "answers": [
                                                {
                                                    "id": "crisps-answer",
                                                    "type": "Checkbox",
                                                    "options": [
                                                        {
                                                            "label": "Ready salted",
                                                            "value": "Ready salted",
                                                            "q_code": "1"
                                                        },
                                                        {
                                                            "label": "Sweet chilli",
                                                            "value": "Sweet chilli",
                                                            "q_code": "2"
                                                        },
                                                        {
                                                            "label": "Cheese and onion",
                                                            "value": "Cheese and onion",
                                                            "q_code": "3"
                                                        },
                                                        {
                                                            "label": "Other",
                                                            "q_code": "4",
                                                            "description": "Choose any other flavour",
                                                            "value": "Other",
                                                            "child_answer_id": "other-answer-mandatory"
                                                        }
                                                    ]
                                                },
                                                {
                                                    "parent_answer_id": "crisps-answer",
                                                    "mandatory": True,
                                                    "id": "other-answer-mandatory",
                                                    "label": "Please specify other",
                                                    "type": "TextField"
                                                }
                                            ]
                                        }]
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }

            # When
            answer_object = convert_answers(metadata, questionnaire, AnswerStore(answers), routing_path)

            # Then
            self.assertEqual(len(answer_object['data']), 2)
            self.assertEqual(answer_object['data']['1'], 'Ready salted')
            self.assertEqual(answer_object['data']['4'], 'Bacon')

    def test_converter_q_codes_for_empty_strings(self):
        with self.application.test_request_context():
            routing_path = [Location(group_id='favourite-food', group_instance=0, block_id='crisps')]
            answers = [create_answer('crisps-answer', '', group_id='favourite-food', block_id='crisps')]
            answers += [create_answer('other-crisps-answer', 'Ready salted', group_id='favourite-food', block_id='crisps')]

            questionnaire = {
                "survey_id": "999",
                "data_version": "0.0.1",
                "groups": [
                    {
                        "id": "favourite-food",
                        "blocks": [
                            {
                                "id": "crisps",
                                "sections": [
                                    {
                                        "questions": [{
                                            "id": 'crisps-question',
                                            "answers": [
                                                {
                                                    "id": "crisps-answer",
                                                    "type": "TextArea",
                                                    "options": [],
                                                    "q_code": "1"
                                                },
                                                {
                                                    "id": "other-crisps-answer",
                                                    "type": "TextArea",
                                                    "options": [],
                                                    "q_code": "2"
                                                }
                                            ]
                                        }]
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }

            # When
            answer_object = convert_answers(metadata, questionnaire, AnswerStore(answers), routing_path)

            # Then
            self.assertEqual(len(answer_object['data']), 1)
            self.assertEqual(answer_object['data']['2'], 'Ready salted')


def create_answer(answer_id, value, group_id=None, block_id=None, answer_instance=0, group_instance=0):
    return {
        'group_id': group_id,
        'block_id': block_id,
        'answer_id': answer_id,
        'answer_instance': answer_instance,
        'group_instance': group_instance,
        'value': value,
    }
