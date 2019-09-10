from flask import json

from tests.integration.integration_test_case import IntegrationTestCase

with open('data/en/test_checkbox.json') as json_data:
    data = json.load(json_data)


class TestStatic(IntegrationTestCase):

    def test_contact(self):
        self.get('/contact-us')
        self.assertInBody('Contact us if you have any questions')

    def test_contact_with_no_session(self):
        self.get('/contact-us')
        self.assertInBody('Opening hours')

    def test_cookies_and_privacy(self):
        self.get('/cookies-privacy')
        self.assertInBody(
            'We can only use your information for research and statistical purposes. '
        )

    def test_privacy(self):
        self.get('/privacy')
        self.assertInBody('Who can access the information?')

