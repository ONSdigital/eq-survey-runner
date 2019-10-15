from unittest.mock import patch

from tests.integration.integration_test_case import IntegrationTestCase


class TestErrors(IntegrationTestCase):

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
        'account_service_url': 'http://correct.place',
        'roles': [],
    }

    def test_errors_404(self):
        self.get('/hfjdskahfjdkashfsa')
        self.assertStatusNotFound()

        # Test that my account link does not show
        self.assertNotInBody('My account')
        self.assertNotInBody('http://correct.place')

    def test_errors_404_with_payload(self):
        with patch('tests.integration.create_token.PAYLOAD', self.example_payload):
            self.launchSurvey('test_percentage')
            self.get('/hfjdskahfjdkashfsa')
            self.assertStatusNotFound()

    def test_errors_500(self):
        # Given
        self.launchSurvey('test_percentage')

        # When / Then
        # Patch out a class in post to raise an exception so that the application error handler
        # gets called
        with patch(
            'app.routes.questionnaire.get_block_handler',
            side_effect=Exception('You broked it'),
        ):
            self.post({'answer': '5000000'})
            self.assertStatusCode(500)

    def test_errors_500_with_payload(self):
        # Given
        with patch('tests.integration.create_token.PAYLOAD', self.example_payload):
            self.launchSurvey('test_percentage')
            # When / Then
            # Patch out a class in post to raise an exception so that the application error handler
            # gets called
            with patch(
                'app.routes.questionnaire.get_block_handler',
                side_effect=Exception('You broked it'),
            ):
                self.post({'answer': '5000000'})
                self.assertStatusCode(500)

    def test_errors_500_exception_during_error_handling(self):
        # Given
        with patch('tests.integration.create_token.PAYLOAD', self.example_payload):
            self.launchSurvey('test_percentage')
            # When

            # Patch out a class in post to raise an exception so that the application error handler
            # gets called
            with patch(
                'app.routes.questionnaire.get_block_handler',
                side_effect=Exception('You broked it'),
            ):
                # Another exception occurs during exception handling
                with patch(
                    'app.routes.errors.log_exception',
                    side_effect=Exception('You broked it again'),
                ):
                    self.post({'answer': '5000000'})

                    self.assertStatusCode(500)
                    self.assertInBody('Sorry, there is a problem with this service')
