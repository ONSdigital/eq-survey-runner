from mock import patch

from tests.integration.integration_test_case import IntegrationTestCase


class TestThankYou(IntegrationTestCase):

    def setUp(self):
        super().SetUpWithDynamoDB()

    def test_thank_you_page_shows_trading_as_if_present(self):
        self.launchSurvey('test', 'currency')

        # check we're on first page
        self.assertInPage('Currency Input Test')

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
        self.assertInPage('(Integration Tests)')

    def test_thank_you_page_does_not_show_empty_parenthesis_if_trading_as_if_not_present(self):
        no_trading_as_payload = {
            'user_id': 'integration-test',
            'period_str': 'April 2016',
            'period_id': '201604',
            'collection_exercise_sid': '789',
            'ru_ref': '123456789012A',
            'ru_name': 'Integration Testing',
            'ref_p_start_date': '2016-04-01',
            'ref_p_end_date': '2016-04-30',
            'return_by': '2016-05-06',
            'employment_date': '1983-06-02',
            'variant_flags': None,
            'region_code': 'GB-ENG',
            'language_code': 'en',
            'roles': []
        }
        with patch('tests.integration.create_token.PAYLOAD', no_trading_as_payload):
            self.launchSurvey('test', 'currency')

            # check we're on first page
            self.assertInPage('Currency Input Test')

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
            self.assertNotInPage('(Integration Tests)')
            self.assertNotInPage('()')

    def test_thank_you_page_does_not_show_empty_parenthesis_if_trading_as_is_empty(self):
        empty_trading_as_payload = {
            'user_id': 'integration-test',
            'period_str': 'April 2016',
            'period_id': '201604',
            'collection_exercise_sid': '789',
            'ru_ref': '123456789012A',
            'ru_name': 'Integration Testing',
            'ref_p_start_date': '2016-04-01',
            'ref_p_end_date': '2016-04-30',
            'return_by': '2016-05-06',
            'employment_date': '1983-06-02',
            'variant_flags': None,
            'region_code': 'GB-ENG',
            'language_code': 'en',
            'trad_as': '',
            'roles': []
        }
        with patch('tests.integration.create_token.PAYLOAD', empty_trading_as_payload):
            self.launchSurvey('test', 'currency')

            # check we're on first page
            self.assertInPage('Currency Input Test')

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
            self.assertNotInPage('(Integration Tests)')
            self.assertNotInPage('()')
