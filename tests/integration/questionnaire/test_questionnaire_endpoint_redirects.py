import json

from tests.integration.integration_test_case import IntegrationTestCase


class TestQuestionnaireEndpointRedirects(IntegrationTestCase):

    def test_get_invalid_questionnaire_location_redirects_to_latest(self):
        # Given
        self.launchSurvey('test', 'introduction')

        base_url = '/questionnaire/'

        # When
        self.get(base_url + 'test')

        # Then
        self.assertInUrl(base_url + 'introduction')

    def test_post_invalid_questionnaire_location_redirects_to_latest(self):
        # Given
        self.launchSurvey('test', 'introduction')

        base_url = '/questionnaire/'

        # When
        self.post(url=base_url + 'test')

        # Then
        self.assertInUrl(base_url + 'introduction')

    def test_submit_answers_for_invalid_questionnaire_location_redirects_to_first_incomplete_location(self):
        # Given
        self.launchSurvey('test', 'textfield')

        base_url = '/questionnaire/'

        # When
        self.post(url=base_url + 'min-max-block')

        # Then
        self.assertInUrl(base_url + 'name-block')

    def test_given_not_complete_questionnaire_when_get_thank_you_then_data_not_deleted(self):
        # Given we start a survey
        self.launchSurvey('test', 'percentage', roles=['dumper'])
        self.post({'answer': '99'})

        # When we request the thank you page (without submitting the survey)
        self.get('submitted/thank-you')

        # Then the answers are not deleted
        self.get('/dump/answers')
        answers = json.loads(self.getResponseData())
        self.assertEqual(1, len(answers['answers']))

    def test_given_not_complete_questionnaire_when_get_thank_you_then_redirected_to_latest_location(self):
        # Given we start a survey
        self.launchSurvey('test', 'percentage', roles=['dumper'])

        # When we request the thank you page (without submitting the survey)
        self.get('submitted/thank-you')

        # Then we should be redirected back to the latest location
        self.assertInUrl('block')

    def test_given_complete_questionnaire_when_submitted_then_data_is_deleted(self):
        # Given we submit a survey
        self.launchSurvey('test', 'percentage', roles=['dumper'])
        self.post({'answer': '99'})
        self.post(action=None)

        # When we start the survey again
        self.launchSurvey('test', 'percentage', roles=['dumper'])

        # Then no answers should have persisted
        self.get('/dump/answers')
        answers = json.loads(self.getResponseData())
        self.assertEqual(0, len(answers['answers']))

    def test_when_on_thank_you_get_summary_returns_unauthorised(self):
        # Given we complete the test_percentage survey and are on the thank you page
        self.launchSurvey('test', 'percentage', roles=['dumper'])
        self.post({'answer': '99'})
        self.post(action=None)

        # When we try to get the summary
        self.get('questionnaire/summary')

        # Then we get the unauthorised page
        self.assertStatusUnauthorised()

    def test_when_on_thank_you_get_thank_you_returns_thank_you(self):
        # Given we complete the test_percentage survey and are on the thank you page
        self.launchSurvey('test', 'percentage', roles=['dumper'])
        self.post({'answer': '99'})
        self.post(action=None)

        # When we try to get the thank-you page
        self.get('submitted/thank-you')

        # Then we get the thank-you page
        self.assertInUrl('submitted/thank-you')

    def test_when_survey_submitted_re_submitting_returns_unauthorised(self):
        # Given we have submitted the test_percentage survey
        self.launchSurvey('test', 'percentage', roles=['dumper'])
        self.post({'answer': '99'})
        self.post(action=None)

        # When we try to submit the survey again
        self.get(url='/questionnaire/summary')

        # Then we get the unauthorised page
        self.assertStatusUnauthorised()

    def test_when_no_session_thank_you_returns_unauthorised(self):
        # When we try to request the thank-you page with no session
        self.get(url='submitted/thank-you')

        # Then we get the unauthorised page
        self.assertStatusUnauthorised()
