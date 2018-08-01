from unittest.mock import patch
from tests.integration.integration_test_case import IntegrationTestCase


class TestErrors(IntegrationTestCase):

    def test_errors_404(self):
        self.get('/hfjdskahfjdkashfsa')
        self.assertStatusNotFound()
        self.assertInPage('Error 404')


    def test_errors_500(self):
        # Given
        self.launchSurvey('test', 'percentage')
        # When / Then
        # Patch out a class in post to raise an exception so that the application error handler
        # gets called
        with patch('app.views.questionnaire.Router', side_effect=Exception('You broked it')):
            self.post({'answer': '5000000'})
            self.assertStatusCode(500)
            self.assertInPage('500')
