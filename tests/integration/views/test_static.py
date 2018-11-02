import mock
from flask import json

from tests.integration.integration_test_case import IntegrationTestCase

with open('data/en/1_0205.json') as json_data:
    data = json.load(json_data)


class TestStatic(IntegrationTestCase):
    @mock.patch('app.utilities.schema.load_schema_from_session_data')
    def test_contact(self, mock_contact):
        mock_contact.return_value = data
        self.launchSurvey('test', '0205')
        self.get('/contact-us')
        self.assertInBody('123456789012A')

    def test_contact_with_no_session(self):
        self.get('/contact-us')
        self.assertNotInBody('Please quote the reference')
        self.assertInBody('Opening hours')

    def test_cookies_and_privacy(self):
        self.get('/cookies-privacy')
        self.assertInBody('We can only use your information for research and statistical purposes. ')
