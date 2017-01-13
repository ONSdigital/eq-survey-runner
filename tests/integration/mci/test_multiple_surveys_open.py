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
        self.assertRegex(first_survey_resp.location, r'\/questionnaire\/1\/0205\/789\/mci\/0\/reporting-period$')

        # We start the second survey
        second_survey_token = create_token('0203', '1')
        self.client.get('/session?token=' + second_survey_token.decode(), follow_redirects=True)

        post_data = {
            'action[start_questionnaire]': 'Start Questionnaire'
        }

        second_survey_resp = self.client.post('/questionnaire/1/0203/789/introduction', data=post_data, follow_redirects=False)
        self.assertRegex(second_survey_resp.location, r'\/questionnaire\/1\/0203\/789\/mci\/0\/reporting-period')

        # We now try to post to the first survey, which is out of date
        form_data = {
            "period-from-day": "01",
            "period-from-month": "4",
            "period-from-year": "2016",
            "period-to-day": "30",
            "period-to-month": "04",
            "period-to-year": "2016",
            "total-retail-turnover": "100000",
            "action[save_continue]": "Save &amp; Continue"
        }

        multiple_survey_resp = self.client.post(first_survey_resp.location, data=form_data, follow_redirects=False)
        content = multiple_survey_resp.get_data(True)
        self.assertRegex(content, 'Information')
        self.assertRegex(content, 'Unfortunately you can only complete one survey at a time.')
        self.assertRegex(content, 'Close this window to continue with your current survey.')
