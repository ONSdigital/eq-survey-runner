from mock import patch

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

    def test_thank_you_page_shows_trading_as_if_present(self):
        self.launchSurvey('test_currency')

        # check we're on first page
        self.assertInBody('Currency Input Test')

        # We fill in our answers
        form_data = {
            # Food choice
            'answer': '12',
            'answer-usd': '345',
            'answer-eur': '67.89',
            'answer-jpy': '0',
        }

        # We submit the form
        self.post(form_data)

        # There are no validation errors
        self.assertInUrl('summary')

        # Submit answers
        self.post(action=None)

        # check we're on the thank you page and that the trading as is displayed
        self.assertInUrl('thank-you')
        self.assertInBody('(Integration Tests)')

    def test_thank_you_page_does_not_show_empty_parenthesis_if_trading_as_if_not_present(
        self
    ):

        with patch('tests.integration.create_token.PAYLOAD', self.example_payload):
            self.launchSurvey('test_currency')

            # check we're on first page
            self.assertInBody('Currency Input Test')

            # We fill in our answers
            form_data = {
                # Food choice
                'answer': '12',
                'answer-usd': '345',
                'answer-eur': '67.89',
                'answer-jpy': '0',
            }

            # We submit the form
            self.post(form_data)

            # There are no validation errors
            self.assertInUrl('summary')

            # Submit answers
            self.post(action=None)

            # check we're on the thank you page and that the trading as parenthesis are not displayed
            self.assertInUrl('thank-you')
            self.assertNotInBody('(Integration Tests)')

    def test_thank_you_page_does_not_show_empty_parenthesis_if_trading_as_is_empty(
        self
    ):
        empty_trading_as_payload = self.example_payload.copy()
        empty_trading_as_payload['trad_as'] = ''

        with patch('tests.integration.create_token.PAYLOAD', empty_trading_as_payload):
            self.launchSurvey('test_currency')

            # check we're on first page
            self.assertInBody('Currency Input Test')

            # We fill in our answers
            form_data = {
                # Food choice
                'answer': '12',
                'answer-usd': '345',
                'answer-eur': '67.89',
                'answer-jpy': '0',
            }

            # We submit the form
            self.post(form_data)

            # There are no validation errors
            self.assertInUrl('summary')

            # Submit answers
            self.post(action=None)

            # check we're on the thank you page and that the trading as parenthesis are not displayed
            self.assertInUrl('thank-you')
            self.assertNotInBody('(Integration Tests)')

    def test_thank_you_page_my_account_link_uses_url_from_payload(self):
        account_service_url_supplied = self.example_payload.copy()
        account_service_url_supplied['account_service_url'] = 'http://correct.place'

        with patch(
            'tests.integration.create_token.PAYLOAD', account_service_url_supplied
        ):
            self.launchSurvey('test_currency')

            # check we're on first page
            self.assertInBody('Currency Input Test')

            # We fill in our answers
            form_data = {
                # Food choice
                'answer': '12',
                'answer-usd': '345',
                'answer-eur': '67.89',
                'answer-jpy': '0',
            }

            # We submit the form
            self.post(form_data)

            # There are no validation errors
            self.assertInUrl('summary')

            # Submit answers
            self.post(action=None)

            # check the 'My account' link is on the thank you page with the correct url
            self.assertInUrl('thank-you')
            self.assertInBody('My account</a>')
            self.assertInBody('href="http://correct.place"')

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
