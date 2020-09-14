from unittest.mock import patch, Mock
from app.helpers.template_helper import with_analytics
from tests.integration.integration_test_case import IntegrationTestCase

def argument_tester(*args, **kwargs):
    return (args, kwargs)

class TestDecorators(IntegrationTestCase):

    @patch('app.helpers.template_helper.request')
    def test_analytics(self, mock):
        mock.cookies.get = Mock(return_value='{"usage":true}')

        with self._application.app_context():
            cookie = with_analytics(argument_tester)()
            self.assertAnalyticsLength(cookie)

    @patch('app.helpers.template_helper.request')
    def test_no_analytics(self, mock):
        mock.cookies.get = Mock(return_value='{"usage":false}')

        with self._application.app_context():
            cookie = with_analytics(argument_tester)()
            self.assertNotAnalyticsLength(cookie)
