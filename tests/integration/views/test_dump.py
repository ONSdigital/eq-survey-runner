import json

from tests.integration.integration_test_case import IntegrationTestCase


class TestDumpAnswers(IntegrationTestCase):

    def test_dump_answers_not_authenticated(self):
        # Given I am not an authenticated user
        # When I attempt to dump the answer store
        self.get('/dump/answers')

        # Then I receive a 401 Unauthorised response code
        self.assertStatusUnauthorised()

    def test_dump_answers_authenticated_missing_role(self):
        # Given I am an authenticated user who has launched a survey
        # but does not have the 'dumper' role in my metadata
        self.launchSurvey('test', 'radio')

        # When I attempt to dump the answer store
        self.get('/dump/answers')

        # Then I receive a 403 Forbidden response code
        self.assertStatusForbidden()

        # And the response data contains Forbidden
        self.assertInPage('Error 403')

    def test_dump_answers_authenticated_with_role_no_answers(self):
        # Given I am an authenticated user who has launched a survey
        # and does have the 'dumper' role in my metadata
        self.launchSurvey('test', 'radio', roles=['dumper'])

        # When I haven't submitted any answers
        # And I attempt to dump the answer store
        self.get('/dump/answers')

        # Then I get a 200 OK response
        self.assertStatusOK()

        # And the JSON response contains an empty array
        actual = json.loads(self.getResponseData())
        expected = {'answers': []}

        self.assertDictEqual(actual, expected)

    def test_dump_answers_authenticated_with_role_with_answers(self):
        # Given I am an authenticated user who has launched a survey
        # and does have the 'dumper' role in my metadata
        self.launchSurvey('test', 'radio', roles=['dumper'])

        # When I submit an answer
        self.post(post_data={'radio-mandatory-answer': 'Bacon'})

        # And I attempt to dump the answer store
        self.get('/dump/answers')

        # Then I get a 200 OK response
        self.assertStatusOK()

        # And the JSON response contains the data I submitted
        actual = json.loads(self.getResponseData())
        expected = {
            'answers': [
                {
                    'value': '', 'answer_instance': 0,
                    'block_id': 'radio-mandatory',
                    'group_instance': 0,
                    'group_id': 'radio',
                    'answer_id': 'other-answer-mandatory'
                },
                {
                    'value': 'Bacon',
                    'answer_instance': 0,
                    'block_id': 'radio-mandatory',
                    'group_instance': 0,
                    'group_id': 'radio',
                    'answer_id': 'radio-mandatory-answer'
                }
            ]
        }

        # Enable full dictionary diffs on test failure
        self.maxDiff = None

        # Data in the answer store doesn't seem to be in a consistent order
        # between test runs so we have to compare like this.
        self.assertCountEqual(actual['answers'], expected['answers'])


class TestDumpSubmission(IntegrationTestCase):

    def test_dump_submission_not_authenticated(self):
        # Given I am not an authenticated user
        # When I attempt to dump the submission payload
        self.get('/dump/submission')

        # Then I receive a 401 Unauthorised response code
        self.assertStatusUnauthorised()

    def test_dump_submission_authenticated_missing_role(self):
        # Given I am an authenticated user who has launched a survey
        # but does not have the 'dumper' role in my metadata
        self.launchSurvey('test', 'radio')

        # When I attempt to dump the submission payload
        self.get('/dump/submission')

        # Then I receive a 403 Forbidden response code
        self.assertStatusForbidden()

        # And the response data contains Forbidden
        self.assertInPage('Error 403')

    def test_dump_submission_authenticated_with_role_no_answers(self):
        # Given I am an authenticated user who has launched a survey
        # and does have the 'dumper' role in my metadata
        self.launchSurvey('test', 'radio', roles=['dumper'])

        # When I haven't submitted any answers
        # And I attempt to dump the submission payload
        self.get('/dump/submission')

        # Then I get a 200 OK response
        self.assertStatusOK()

        # And the JSON response contains the data I submitted
        actual = json.loads(self.getResponseData())

        # tx_id and submitted_at are dynamic; so copy them over
        expected = {
            'submission': {
                'version': '0.0.1',
                'survey_id': '0',
                'flushed': False,
                'origin': 'uk.gov.ons.edc.eq',
                'type': 'uk.gov.ons.edc.eq:surveyresponse',
                'tx_id': actual['submission']['tx_id'],
                'submitted_at': actual['submission']['submitted_at'],
                'collection': {
                    'period': '201604',
                    'exercise_sid': '789',
                    'instrument_id': 'radio'
                },
                'data': {},
                'metadata': {
                    'ru_ref': '123456789012A',
                    'user_id': 'integration-test'
                }
            }
        }

        # Enable full dictionary diffs on test failure
        self.maxDiff = None
        self.assertDictEqual(actual, expected)

    def test_dump_submission_authenticated_with_role_with_answers(self):
        # Given I am an authenticated user who has launched a survey
        # and does have the 'dumper' role in my metadata
        self.launchSurvey('test', 'radio', roles=['dumper'])

        # When I submit an answer
        self.post(post_data={'radio-mandatory-answer': 'Bacon'})

        # And I attempt to dump the submission payload
        self.get('/dump/submission')

        # Then I get a 200 OK response
        self.assertStatusOK()

        # And the JSON response contains the data I submitted
        actual = json.loads(self.getResponseData())

        # tx_id and submitted_at are dynamic; so copy them over
        expected = {
            'submission': {
                'version': '0.0.1',
                'survey_id': '0',
                'flushed': False,
                'origin': 'uk.gov.ons.edc.eq',
                'type': 'uk.gov.ons.edc.eq:surveyresponse',
                'tx_id': actual['submission']['tx_id'],
                'submitted_at': actual['submission']['submitted_at'],
                'collection': {
                    'period': '201604',
                    'exercise_sid': '789',
                    'instrument_id': 'radio'
                },
                'data': {
                    '20': 'Bacon'
                },
                'metadata': {
                    'ru_ref': '123456789012A',
                    'user_id': 'integration-test'
                }
            }
        }

        # Enable full dictionary diffs on test failure
        self.maxDiff = None
        self.assertDictEqual(actual, expected)
