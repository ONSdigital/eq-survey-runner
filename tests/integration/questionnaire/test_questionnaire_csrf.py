import json

from tests.integration.integration_test_case import IntegrationTestCase


class TestQuestionnaireCsrf(IntegrationTestCase):

    def test_given_on_interstitial_page_when_submit_with_no_csrf_token_then_forbidden(self):
        # Given
        self.launchSurvey('test', 'interstitial_page')
        self.last_csrf_token = None

        # When
        self.post(action='start_questionnaire')

        # Then
        self.assertStatusForbidden()
        self.assertEqualUrl(self.last_url)

    def test_given_on_interstitial_page_when_submit_with_invalid_csrf_token_then_forbidden(self):
        # Given
        self.launchSurvey('test', 'interstitial_page')
        self.last_csrf_token = 'made-up-token'

        # When
        self.post(action='start_questionnaire')

        # Then
        self.assertStatusForbidden()
        self.assertEqualUrl(self.last_url)

    def test_given_on_introduction_page_when_submit_valid_token_then_redirect_to_next_page(self):
        # Given
        self.launchSurvey('test', 'interstitial_page')

        # When
        self.post(action='start_questionnaire')

        # Then
        self.assertStatusOK()
        self.assertInPage('What is your favourite breakfast food')

    def test_given_answered_question_when_change_answer_with_invalid_csrf_token_then_answers_not_saved(self):
        # Given
        self.launchSurvey('test', 'interstitial_page', roles=['dumper'])
        self.post()
        self.post({'favourite-breakfast': 'Muesli'})

        # When
        self.last_csrf_token = 'made-up-token'
        self.post({'favourite-breakfast': 'Pancakes'})

        # Then
        self.assertStatusForbidden()
        self.get('/dump/answers')
        answers = json.loads(self.getResponseData())
        self.assertEqual('Muesli', answers['answers'][0]['value'])

    def test_given_valid_answers_on_household_composition_when_answer_with_invalid_csrf_token_then_answers_not_saved(self):
        # Given
        self.launchSurvey('census', 'household', roles=['dumper'])
        post_data = {'first_name': 'Joe'}

        # When
        self.last_csrf_token = 'made-up-token'
        self.post(url='/questionnaire/census/household/789/who-lives-here/0/household-composition', post_data=post_data)

        # Then
        self.assertStatusForbidden()
        self.get('/dump/answers')
        answers = json.loads(self.getResponseData())
        self.assertEqual(0, len(answers['answers']))

    def test_given_valid_answers_when_save_and_sign_out_with_invalid_csrf_token_then_answers_not_saved(self):
        # Given
        self.launchSurvey('test', 'interstitial_page', roles=['dumper'])
        self.post()
        post_data = {'favourite-breakfast': 'Muesli'}

        # When
        self.last_csrf_token = 'made-up-token'
        self.post(post_data=post_data, action='save_sign_out')

        # Then
        self.assertStatusForbidden()
        self.get('/dump/answers')
        answers = json.loads(self.getResponseData())
        self.assertEqual(0, len(answers['answers']))

    def test_given_csrf_attack_when_refresh_then_on_question(self):
        # Given
        self.launchSurvey('test', 'interstitial_page', roles=['dumper'])
        self.post()
        self.last_csrf_token = 'made-up-token'
        self.post({'favourite-breakfast': 'Pancakes'})

        # When
        self.get(self.last_url)

        # Then
        self.assertEqual(self.last_response.status_code, 200)
        self.get('/dump/answers')
        answers = json.loads(self.getResponseData())
        self.assertEqual(0, len(answers['answers']))

    def test_given_csrf_attack_when_submit_new_answers_then_answers_saved(self):
        # Given
        self.launchSurvey('test', 'interstitial_page', roles=['dumper'])
        self.post()
        self.last_csrf_token = 'made-up-token'
        self.post({'favourite-breakfast': 'Muesli'})

        # When
        self.get(self.last_url)
        self.post({'favourite-breakfast': 'Pancakes'})

        # Then
        self.assertStatusOK()
        self.get('/dump/answers')
        answers = json.loads(self.getResponseData())
        self.assertEqual('Pancakes', answers['answers'][0]['value'])
