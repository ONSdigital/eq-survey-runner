import os
import unittest

from app import create_app
from app import settings
from app.data_model.database import QuestionnaireState


class IntegrationTestCase(unittest.TestCase):

    def setUp(self):
        settings.EQ_SERVER_SIDE_STORAGE_DATABASE_URL = "sqlite://"

        for key_name, dev_location in settings._KEYS.items():  # pylint: disable=protected-access
            path = os.getenv(key_name, dev_location)
            vars(settings)[key_name] = settings.get_key(path)  # assigns attribute to this module

        for password_name, dev_default in settings._PASSWORDS.items():  # pylint: disable=protected-access
            password = os.getenv(password_name, dev_default)
            vars(settings)[password_name] = password  # assigns attribute to this module

        self.application = create_app()
        self.client = self.application.test_client()

    def tearDown(self):
        # Clear storage after test ends
        # pylint: disable=maybe-no-member
        # SQLAlchemy doing declarative magic which makes session scope query property available
        QuestionnaireState.query.delete()

    def postRedirectGet(self, url, post_data):
        """
        POSTs to the specified URL with post_data and performs a GET
        with the URL from the re-direct, returning the re-direct URL and
        response object.

        :param url: the URL to POST to
        :param post_data: the data to POST
        :return: tuple of the re-direct URL and response object from the GET
        """
        resp = self.client.post(url, data=post_data, follow_redirects=False)
        self.assertEqual(resp.status_code, 302)
        resp_url = resp.location
        resp = self.client.get(resp_url, follow_redirects=False)
        self.assertEqual(resp.status_code, 200)
        return resp_url, resp
