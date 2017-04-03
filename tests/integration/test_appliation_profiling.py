from app import settings
from tests.integration.integration_test_case import IntegrationTestCase


class TestApplicationProfiling(IntegrationTestCase):

    def setUp(self):
        settings.EQ_PROFILING = True
        super().setUp()

    def tearDown(self):
        settings.EQ_PROFILING = False
        super().tearDown()

    def test_profiling_is_enabled(self):
        self.assertEqual(True, self._application.config['PROFILE'])
