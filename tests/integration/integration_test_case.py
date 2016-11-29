import unittest
from app import create_app
from app import settings
from app.storage.storage_factory import get_storage


class IntegrationTestCase(unittest.TestCase):

    def setUp(self):
        # Use an in memory database
        settings.EQ_SERVER_SIDE_STORAGE_TYPE = "DATABASE"
        settings.EQ_SERVER_SIDE_STORAGE_DATABASE_URL = "sqlite://"

        self.application = create_app()
        self.client = self.application.test_client()

        # Clear storage before starting test
        storage = get_storage()
        storage.clear()

    def tearDown(self):
        # Clear storage after test ends
        storage = get_storage()
        storage.clear()

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
        self.assertEquals(resp.status_code, 302)
        resp_url = resp.headers['Location']
        resp = self.client.get(resp_url, follow_redirects=False)
        self.assertEquals(resp.status_code, 200)
        return resp_url, resp

