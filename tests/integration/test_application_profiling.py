import os
from unittest.mock import patch

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

class TestApplicationProfilingDir(IntegrationTestCase):

    def setUp(self):
        pass

    def test_profiling_directory_created(self):
        # Given
        profiling_dir = 'profiling'
        os.rmdir(profiling_dir)
        # When - setup the app
        with patch('app.setup.settings.EQ_PROFILING', True):
            super().setUp()
        # Then
        self.assertTrue(os.path.exists(profiling_dir))
