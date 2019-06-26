import json

from tests.integration.integration_test_case import IntegrationTestCase


class TestDumpDebug(IntegrationTestCase):
    def test_dump_debug_not_authenticated(self):
        # Given I am not an authenticated user
        # When I attempt to dump the questionnaire store
        self.get('/dump/debug')

        # Then I receive a 401 Unauthorised response code
        self.assertStatusUnauthorised()

    def test_dump_debug_authenticated_missing_role(self):
        # Given I am an authenticated user who has launched a survey
        # but does not have the 'dumper' role in my metadata
        self.launchSurvey('test_radio_mandatory_with_mandatory_other')

        # When I attempt to dump the questionnaire store
        self.get('/dump/debug')

        # Then I receive a 403 Forbidden response code
        self.assertStatusForbidden()

        # And the response data contains Forbidden
        self.assertInBody('Error 403')

    def test_dump_debug_authenticated_with_role(self):
        # Given I am an authenticated user who has launched a survey
        # and does have the 'dumper' role in my metadata
        self.launchSurvey('test_radio_mandatory_with_mandatory_other', roles=['dumper'])

        # And I attempt to dump the questionnaire store
        self.get('/dump/debug')

        # Then I get a 200 OK response
        self.assertStatusOK()


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
        self.launchSurvey('test_radio_mandatory_with_mandatory_other')

        # When I attempt to dump the submission payload
        self.get('/dump/submission')

        # Then I receive a 403 Forbidden response code
        self.assertStatusForbidden()

        # And the response data contains Forbidden
        self.assertInBody('Error 403')

    def test_dump_submission_authenticated_with_role_no_answers(self):
        # Given I am an authenticated user who has launched a survey
        # and does have the 'dumper' role in my metadata
        self.launchSurvey('test_radio_mandatory_with_mandatory_other', roles=['dumper'])

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
                'version': '0.0.3',
                'survey_id': '0',
                'flushed': False,
                'origin': 'uk.gov.ons.edc.eq',
                'type': 'uk.gov.ons.edc.eq:surveyresponse',
                'tx_id': actual['submission']['tx_id'],
                'submitted_at': actual['submission']['submitted_at'],
                'case_id': actual['submission']['case_id'],
                'response_id': '1234567890123456',
                'questionnaire_id': actual['submission']['questionnaire_id'],
                'collection': {
                    'period': '201604',
                    'exercise_sid': '789',
                    'schema_name': 'test_radio_mandatory_with_mandatory_other',
                },
                'data': [],
                'metadata': {'ru_ref': '123456789012A', 'user_id': 'integration-test'},
            }
        }

        assert actual == expected

    def test_dump_submission_authenticated_with_role_with_answers(self):
        # Given I am an authenticated user who has launched a survey
        # and does have the 'dumper' role in my metadata
        self.launchSurvey('test_radio_mandatory', roles=['dumper'])

        # When I submit an answer
        self.post(post_data={'radio-mandatory-answer': 'Coffee'})

        # And I attempt to dump the submission payload
        self.get('/dump/submission')

        # Then I get a 200 OK response
        self.assertStatusOK()

        # And the JSON response contains the data I submitted
        actual = json.loads(self.getResponseData())

        # tx_id and submitted_at are dynamic; so copy them over
        expected = {
            'submission': {
                'version': '0.0.3',
                'survey_id': '0',
                'flushed': False,
                'origin': 'uk.gov.ons.edc.eq',
                'type': 'uk.gov.ons.edc.eq:surveyresponse',
                'tx_id': actual['submission']['tx_id'],
                'started_at': actual['submission']['started_at'],
                'submitted_at': actual['submission']['submitted_at'],
                'case_id': actual['submission']['case_id'],
                'response_id': '1234567890123456',
                'questionnaire_id': actual['submission']['questionnaire_id'],
                'collection': {
                    'period': '201604',
                    'exercise_sid': '789',
                    'schema_name': 'test_radio_mandatory',
                },
                'data': [{'answer_id': 'radio-mandatory-answer', 'value': 'Coffee'}],
                'metadata': {'ru_ref': '123456789012A', 'user_id': 'integration-test'},
            }
        }
        assert actual == expected


class TestDumpRoute(IntegrationTestCase):
    def test_dump_route_not_authenticated(self):
        # Given I am not an authenticated user
        # When I attempt to dump the questionnaire store
        self.get('/dump/routing-path')

        # Then I receive a 401 Unauthorised response code
        self.assertStatusUnauthorised()

    def test_dump_route_authenticated_missing_role(self):
        # Given I am an authenticated user who has launched a survey
        # but does not have the 'dumper' role in my metadata
        self.launchSurvey('test_radio_mandatory_with_mandatory_other')

        # When I attempt to dump the questionnaire store
        self.get('/dump/routing-path')

        # Then I receive a 403 Forbidden response code
        self.assertStatusForbidden()

        # And the response data contains Forbidden
        self.assertInBody('Error 403')

    def test_dump_route_authenticated_with_role(self):
        # Given I am an authenticated user who has launched a survey
        # and does have the 'dumper' role in my metadata
        self.launchSurvey('test_radio_mandatory_with_mandatory_other', roles=['dumper'])

        # And I attempt to dump the questionnaire store
        self.get('/dump/routing-path')

        # Then I get a 200 OK response
        self.assertStatusOK()

    def test_dump_route_authenticated_with_role_no_answers(self):
        # Given I am an authenticated user who has launched a survey
        # and does have the 'dumper' role in my metadata
        self.launchSurvey('test_radio_mandatory_with_mandatory_other', roles=['dumper'])

        # When I haven't submitted any answers
        # And I attempt to dump the submission payload
        self.get('/dump/routing-path')

        # Then I get a 200 OK response
        self.assertStatusOK()

        # And the JSON response contains the data I submitted
        actual = json.loads(self.getResponseData())
        # tx_id and submitted_at are dynamic; so copy them over
        expected = {
            'routing_path': [{'block_id': 'radio-mandatory'}, {'block_id': 'summary'}]
        }

        assert actual == expected

    def test_dump_submission_authenticated_with_role_with_answers(self):
        # Given I am an authenticated user who has launched a survey
        # and does have the 'dumper' role in my metadata
        self.launchSurvey('test_radio_mandatory', roles=['dumper'])

        # When I submit an answer
        self.post(post_data={'radio-mandatory-answer': 'Coffee'})

        # And I attempt to dump the submission payload
        self.get('/dump/routing-path')

        # Then I get a 200 OK response
        self.assertStatusOK()

        # And the JSON response contains the data I submitted
        actual = json.loads(self.getResponseData())

        # tx_id and submitted_at are dynamic; so copy them over
        expected = {
            'routing_path': [{'block_id': 'radio-mandatory'}, {'block_id': 'summary'}]
        }
        assert actual == expected
