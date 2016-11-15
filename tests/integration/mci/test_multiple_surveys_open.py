from tests.integration.create_token import create_token
from tests.integration.integration_test_case import IntegrationTestCase


class MultipleSurveysOpen(IntegrationTestCase):

    def test_multiple_surveys_open(self):

        # We start the first survey
        first_survey_token = create_token('0205', '1')
        self.client.get('/session?token=' + first_survey_token.decode(), follow_redirects=True)

        post_data = {
            'action[start_questionnaire]': 'Start Questionnaire'
        }

        first_survey_resp = self.client.post('/questionnaire/1/0205/789/introduction', data=post_data, follow_redirects=False)
        self.assertRegexpMatches(first_survey_resp.headers['Location'], r'\/questionnaire\/1\/0205\/789\/14ba4707-321d-441d-8d21-b8367366e766\/0\/cd3b74d1-b687-4051-9634-a8f9ce10a27d$')

        # We start the second survey
        second_survey_token = create_token('0203', '1')
        self.client.get('/session?token=' + second_survey_token.decode(), follow_redirects=True)

        post_data = {
            'action[start_questionnaire]': 'Start Questionnaire'
        }

        second_survey_resp = self.client.post('/questionnaire/1/0203/789/introduction', data=post_data, follow_redirects=False)
        self.assertRegexpMatches(second_survey_resp.headers['Location'], r'\/questionnaire\/1\/0203\/789\/14ba4707-321d-441d-8d21-b8367366e766\/0\/cd3b74d1-b687-4051-9634-a8f9ce10a27d$')

        # We now try to post to the first survey, which is out of date
        form_data = {
            "6fd644b0-798e-4a58-a393-a438b32fe637-day": "01",
            "6fd644b0-798e-4a58-a393-a438b32fe637-month": "4",
            "6fd644b0-798e-4a58-a393-a438b32fe637-year": "2016",
            "06a6a4b7-6ce4-4687-879d-3443cd8e2ff0-day": "30",
            "06a6a4b7-6ce4-4687-879d-3443cd8e2ff0-month": "04",
            "06a6a4b7-6ce4-4687-879d-3443cd8e2ff0-year": "2016",
            "e81adc6d-6fb0-4155-969c-d0d646f15345": "100000",
            "action[save_continue]": "Save &amp; Continue"
        }

        first_survey_resp = self.client.post(first_survey_resp.headers['Location'], data=form_data, follow_redirects=False)

        # We get redirected to the information page with the multiple surveys message
        self.assertRegexpMatches(first_survey_resp.headers['Location'], r'\/information\/multiple-surveys')
        first_survey_resp = self.client.get(first_survey_resp.headers['Location'], follow_redirects=True)
        content = first_survey_resp.get_data(True)
        self.assertRegexpMatches(content, 'Information')
        self.assertRegexpMatches(content, 'Unfortunately you can only complete one survey at a time.')
        self.assertRegexpMatches(content, 'Close this window to continue with your current survey.')
