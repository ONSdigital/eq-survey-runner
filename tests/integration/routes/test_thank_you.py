from tests.integration.integration_test_case import IntegrationTestCase


class TestThankYou(IntegrationTestCase):
    example_payload = {
        'user_id': 'integration-test',
        'period_str': 'April 2016',
        'period_id': '201604',
        'collection_exercise_sid': '789',
        'questionnaire_id': '0123456789000000',
        'ru_ref': '123456789012A',
        'response_id': '1234567890123456',
        'ru_name': 'Integration Testing',
        'ref_p_start_date': '2016-04-01',
        'ref_p_end_date': '2016-04-30',
        'return_by': '2016-05-06',
        'employment_date': '1983-06-02',
        'region_code': 'GB-ENG',
        'language_code': 'en',
        'roles': [],
        'account_service_url': 'http://upstream.url',
    }

    def test_thank_you_page_sign_out(self):
        self.launchSurvey('test_currency')

        # We fill in our answers
        form_data = {
            'answer': '12',
            'answer-usd': '345',
            'answer-eur': '67.89',
            'answer-jpy': '0',
        }

        # We submit the form
        self.post(form_data)
        # Submit answers
        self.post(action=None)

        # check we're on the thank you page
        self.assertInUrl('thank-you')

        # sign out and check we're on the signed out page
        self.post(action='sign_out')
        self.assertEqualUrl('/signed-out')

    def test_can_switch_language_on_thank_you_page(self):
        self.launchSurvey('test_currency')

        # We fill in our answers
        form_data = {
            'answer': '12',
            'answer-usd': '345',
            'answer-eur': '67.89',
            'answer-jpy': '0',
        }

        # We submit the form
        self.post(form_data)

        # Submit answers
        self.post(action=None)

        # Ensure we're on the thank you page
        self.assertInUrl('thank-you')

        # Ensure translation is as expected using language toggle links
        # Toggle link text displays 'English' when in Welsh, and 'Cymraeg' when in English
        self.assertNotInBody('English')
        self.assertInBody('Cymraeg')

        # Switch language to Welsh
        self.get(f'{self.last_url}?language_code=cy')
        self.assertInUrl('?language_code=cy')

        # Ensure translation is now in Welsh
        self.assertInBody('English')
        self.assertNotInBody('Cymraeg')
