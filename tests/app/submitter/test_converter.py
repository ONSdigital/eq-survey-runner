from datetime import datetime, timedelta, timezone

import dateutil.parser

from app.data_model.answer_store import AnswerStore
from app.questionnaire.questionnaire_schema import QuestionnaireSchema
from app.questionnaire.location import Location
from app.storage.metadata_parser import parse_metadata
from app.submitter.converter import convert_answers, DataVersionError
from tests.app.app_context_test_case import AppContextTestCase


class TestConverter(AppContextTestCase):  # pylint: disable=too-many-public-methods
    def setUp(self):
        super().setUp()
        self.metadata = parse_metadata({
            'user_id': '789473423',
            'form_type': '0205',
            'collection_exercise_sid': 'test-sid',
            'eq_id': '1',
            'period_id': '2016-02-01',
            'period_str': '2016-01-01',
            'ref_p_start_date': '2016-02-02',
            'ref_p_end_date': '2016-03-03',
            'ru_ref': '432423423423',
            'ru_name': 'Apple',
            'return_by': '2016-07-07',
            'case_id': '1234567890',
            'case_ref': '1000000000000001'
        }, schema_metadata={})

    def test_convert_answers_flushed_flag_default_is_false(self):
        with self._app.test_request_context():
            user_answer = [create_answer('GHI', 0)]

            questionnaire = {
                'survey_id': '021',
                'data_version': '0.0.2'
            }

            answer_object = convert_answers(self.metadata, QuestionnaireSchema(questionnaire), AnswerStore(user_answer), {})

            self.assertFalse(answer_object['flushed'])

    def test_ref_period_end_date_is_not_in_output(self):
        with self._app.test_request_context():
            user_answer = [create_answer('GHI', 0)]

            questionnaire = {
                'survey_id': '021',
                'data_version': '0.0.2'
            }
            self.metadata['ref_p_end_date'] = None
            answer_object = convert_answers(self.metadata, QuestionnaireSchema(questionnaire), AnswerStore(user_answer), {})
            self.assertFalse('ref_period_end_date' in answer_object['metadata'])

            del self.metadata['ref_p_end_date']
            answer_object = convert_answers(self.metadata, QuestionnaireSchema(questionnaire), AnswerStore(user_answer), {})
            self.assertFalse('ref_period_end_date' in answer_object['metadata'])

    def test_ref_period_start_and_end_date_is_in_output(self):
        with self._app.test_request_context():
            user_answer = [create_answer('GHI', 0)]

            questionnaire = {
                'survey_id': '021',
                'data_version': '0.0.2'
            }

            answer_object = convert_answers(self.metadata, QuestionnaireSchema(questionnaire), AnswerStore(user_answer), {})
            self.assertEqual(answer_object['metadata']['ref_period_start_date'], '2016-02-02')
            self.assertEqual(answer_object['metadata']['ref_period_end_date'], '2016-03-03')

    def test_convert_answers_flushed_flag_overriden_to_true(self):
        with self._app.test_request_context():
            user_answer = [create_answer('GHI', 0)]

            questionnaire = {
                'survey_id': '021',
                'data_version': '0.0.2'
            }

            answer_object = convert_answers(self.metadata, QuestionnaireSchema(questionnaire), AnswerStore(user_answer), {}, flushed=True)

            self.assertTrue(answer_object['flushed'])

    def test_submitted_at_should_be_set_in_payload(self):
        with self._app.test_request_context():
            user_answer = [create_answer('GHI', 0)]

            questionnaire = {
                'survey_id': '021',
                'data_version': '0.0.2'
            }

            answer_object = convert_answers(self.metadata, QuestionnaireSchema(questionnaire), AnswerStore(user_answer), {})

            self.assertLess(datetime.now(timezone.utc) - dateutil.parser.parse(answer_object['submitted_at']),
                            timedelta(seconds=5))

    def test_case_id_should_be_set_in_payload(self):
        with self._app.test_request_context():

            questionnaire = {
                'survey_id': '021',
                'data_version': '0.0.2'
            }

            answer_object = convert_answers(self.metadata, QuestionnaireSchema(questionnaire), AnswerStore(), {})

            self.assertEqual(answer_object['case_id'], self.metadata['case_id'])

    def test_case_ref_should_be_set_in_payload(self):
        with self._app.test_request_context():

            questionnaire = {
                'survey_id': '021',
                'data_version': '0.0.2'
            }

            answer_object = convert_answers(self.metadata, QuestionnaireSchema(questionnaire), AnswerStore(), {})

            self.assertEqual(answer_object['case_ref'], self.metadata['case_ref'])

    def test_converter_raises_runtime_error_for_unsupported_version(self):
        with self._app.test_request_context():
            questionnaire = {
                'survey_id': '021',
                'data_version': '-0.0.1'
            }

            with self.assertRaises(DataVersionError) as err:
                convert_answers(self.metadata, QuestionnaireSchema(questionnaire), AnswerStore(), {})

            self.assertEqual(str(err.exception), 'Data version -0.0.1 not supported')

    def test_convert_answers(self):
        with self._app.test_request_context():
            user_answer = [create_answer('ABC', '2016-01-01', group_id='group-1', block_id='block-1'),
                           create_answer('DEF', '2016-03-30', group_id='group-1', block_id='block-1')]

            questionnaire = {
                'survey_id': '021',
                'data_version': '0.0.1',
                'sections': [
                    {
                        'id': 'section-1',
                        'groups': [
                            {
                                'id': 'group-1',
                                'blocks': [
                                    {
                                        'id': 'block-1',
                                        'questions': [
                                            {
                                                'id': 'question-1',
                                                'answers': [
                                                    {
                                                        'id': 'ABC',
                                                        'type': 'TextField',
                                                        'q_code': '001'
                                                    },
                                                    {
                                                        'id': 'DEF',
                                                        'type': 'TextField',
                                                        'q_code': '002'
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

            routing_path = [Location(group_id='group-1', group_instance=0, block_id='block-1')]
            answer_object = convert_answers(self.metadata, QuestionnaireSchema(questionnaire), AnswerStore(user_answer), routing_path)

            self.assertEqual(answer_object['type'], 'uk.gov.ons.edc.eq:surveyresponse')
            self.assertEqual(answer_object['version'], '0.0.1')
            self.assertEqual(answer_object['origin'], 'uk.gov.ons.edc.eq')
            self.assertEqual(answer_object['survey_id'], '021')
            self.assertEqual(answer_object['collection']['exercise_sid'], self.metadata['collection_exercise_sid'])
            self.assertEqual(answer_object['collection']['instrument_id'], self.metadata['form_type'])
            self.assertEqual(answer_object['collection']['period'], self.metadata['period_id'])
            self.assertEqual(answer_object['metadata']['user_id'], self.metadata['user_id'])
            self.assertEqual(answer_object['metadata']['ru_ref'], self.metadata['ru_ref'])
            self.assertEqual(answer_object['data']['001'], '2016-01-01')
            self.assertEqual(answer_object['data']['002'], '2016-03-30')


def create_answer(answer_id, value, group_id=None, block_id=None, answer_instance=0, group_instance=0):
    return {
        'group_id': group_id,
        'block_id': block_id,
        'answer_id': answer_id,
        'answer_instance': answer_instance,
        'group_instance': group_instance,
        'value': value,
    }
