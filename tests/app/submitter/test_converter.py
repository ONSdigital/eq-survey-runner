import copy
import uuid
from datetime import datetime, timedelta

import dateutil.parser

from app.data_model.answer_store import AnswerStore
from app.questionnaire.questionnaire_schema import QuestionnaireSchema
from app.storage.metadata_parser import validate_metadata, parse_runner_claims
from app.submitter.converter import convert_answers, DataVersionError
from tests.app.app_context_test_case import AppContextTestCase


class TestConverter(AppContextTestCase):  # pylint: disable=too-many-public-methods
    def setUp(self):
        super().setUp()

        def parse_metadata(claims, schema_metadata):
            validated_claims = parse_runner_claims(claims)
            validate_metadata(validated_claims, schema_metadata)
            return validated_claims

        self.schema_metadata = [
            {
                'name': 'user_id',
                'validator': 'string'
            },
            {
                'name': 'period_id',
                'validator': 'string'
            }
        ]

        self.metadata = parse_metadata({
            'tx_id': str(uuid.uuid4()),
            'user_id': '789473423',
            'form_type': '0000',
            'collection_exercise_sid': 'test-sid',
            'eq_id': '1',
            'period_id': '2016-02-01',
            'period_str': '2016-01-01',
            'ref_p_start_date': '2016-02-02',
            'ref_p_end_date': '2016-03-03',
            'ru_ref': '432423423423',
            'ru_name': 'Apple',
            'return_by': '2016-07-07',
            'started_at': '2018-07-04T14:49:33.448608+00:00',
            'case_id': str(uuid.uuid4()),
            'case_ref': '1000000000000001'
        }, self.schema_metadata)

        self.collection_metadata = {
            'started_at': '2018-07-04T14:49:33.448608+00:00',
        }

    def test_convert_answers_flushed_flag_default_is_false(self):
        with self._app.test_request_context():
            user_answer = [create_answer('GHI', 0)]

            questionnaire = {
                'survey_id': '021',
                'data_version': '0.0.2'
            }

            answer_object = convert_answers(self.metadata, self.collection_metadata, QuestionnaireSchema(questionnaire), AnswerStore(user_answer), {})

            self.assertFalse(answer_object['flushed'])

    def test_ref_period_end_date_is_not_in_output(self):
        with self._app.test_request_context():
            user_answer = [create_answer('GHI', 0)]

            questionnaire = {
                'survey_id': '021',
                'data_version': '0.0.2'
            }
            self.metadata['ref_p_end_date'] = None
            answer_object = convert_answers(self.metadata, self.collection_metadata, QuestionnaireSchema(questionnaire), AnswerStore(user_answer), {})
            self.assertFalse('ref_period_end_date' in answer_object['metadata'])

            del self.metadata['ref_p_end_date']
            answer_object = convert_answers(self.metadata, self.collection_metadata, QuestionnaireSchema(questionnaire), AnswerStore(user_answer), {})
            self.assertFalse('ref_period_end_date' in answer_object['metadata'])

    def test_ref_period_start_and_end_date_is_in_output(self):
        with self._app.test_request_context():
            user_answer = [create_answer('GHI', 0)]

            questionnaire = {
                'survey_id': '021',
                'data_version': '0.0.2'
            }

            answer_object = convert_answers(self.metadata, self.collection_metadata, QuestionnaireSchema(questionnaire), AnswerStore(user_answer), {})
            self.assertEqual(answer_object['metadata']['ref_period_start_date'], '2016-02-02')
            self.assertEqual(answer_object['metadata']['ref_period_end_date'], '2016-03-03')

    def test_convert_answers_flushed_flag_overriden_to_true(self):
        with self._app.test_request_context():
            user_answer = [create_answer('GHI', 0)]

            questionnaire = {
                'survey_id': '021',
                'data_version': '0.0.2'
            }

            answer_object = convert_answers(
                self.metadata, self.collection_metadata, QuestionnaireSchema(questionnaire), AnswerStore(user_answer), {}, flushed=True
            )

            self.assertTrue(answer_object['flushed'])

    def test_started_at_should_be_set_in_payload_if_present_in_collection_metadata(self):
        with self._app.test_request_context():

            questionnaire = {
                'survey_id': '021',
                'data_version': '0.0.2'
            }

            answer_object = convert_answers(
                self.metadata, self.collection_metadata, QuestionnaireSchema(questionnaire), AnswerStore(), {}
            )

            self.assertEqual(answer_object['started_at'], self.collection_metadata['started_at'])

    def test_started_at_should_not_be_set_in_payload_if_absent_in_metadata(self):
        with self._app.test_request_context():

            questionnaire = {
                'survey_id': '021',
                'data_version': '0.0.2'
            }
            collection_metadata_copy = copy.copy(self.collection_metadata)
            metadata = self.metadata.copy()
            metadata.pop('started_at', None)

            del collection_metadata_copy['started_at']

            answer_object = convert_answers(metadata, collection_metadata_copy, QuestionnaireSchema(questionnaire), AnswerStore(), {})

            self.assertFalse('started_at' in answer_object)

    def test_submitted_at_should_be_set_in_payload(self):
        with self._app.test_request_context():
            user_answer = [create_answer('GHI', 0)]

            questionnaire = {
                'survey_id': '021',
                'data_version': '0.0.2'
            }

            answer_object = convert_answers(self.metadata, self.collection_metadata, QuestionnaireSchema(questionnaire), AnswerStore(user_answer), {})

            self.assertLess(datetime.utcnow() - dateutil.parser.parse(answer_object['submitted_at']),
                            timedelta(seconds=5))

    def test_case_id_should_be_set_in_payload(self):
        with self._app.test_request_context():

            questionnaire = {
                'survey_id': '021',
                'data_version': '0.0.2'
            }

            answer_object = convert_answers(self.metadata, self.collection_metadata, QuestionnaireSchema(questionnaire), AnswerStore(), {})

            self.assertEqual(answer_object['case_id'], self.metadata['case_id'])

    def test_case_ref_should_be_set_in_payload(self):
        with self._app.test_request_context():

            questionnaire = {
                'survey_id': '021',
                'data_version': '0.0.2'
            }

            answer_object = convert_answers(self.metadata, self.collection_metadata, QuestionnaireSchema(questionnaire), AnswerStore(), {})

            self.assertEqual(answer_object['case_ref'], self.metadata['case_ref'])

    def test_converter_raises_runtime_error_for_unsupported_version(self):
        with self._app.test_request_context():
            questionnaire = {
                'survey_id': '021',
                'data_version': '-0.0.1'
            }

            with self.assertRaises(DataVersionError) as err:
                convert_answers(self.metadata, self.collection_metadata, QuestionnaireSchema(questionnaire), AnswerStore(), {})

            self.assertEqual(str(err.exception), 'Data version -0.0.1 not supported')


def create_answer(answer_id, value):
    return {
        'answer_id': answer_id,
        'value': value,
    }
