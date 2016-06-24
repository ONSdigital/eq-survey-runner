import unittest
from app import create_app
from app import settings
from app.storage.storage_factory import StorageFactory


class IntegrationTestCase(unittest.TestCase):

    def setUp(self):
        # Use an in memory database
        settings.EQ_SERVER_SIDE_STORAGE_DATABASE_URL = "sqlite://"

        self.application = create_app('development')
        self.client = self.application.test_client()

    def tearDown(self):
        storage = StorageFactory.get_storage_mechanism()
        storage.clear()

