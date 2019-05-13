from unittest.mock import patch

from tests.integration.integration_test_case import IntegrationTestCase


class TestApplicationProfiling(IntegrationTestCase):
    def setUp(self, setting_overrides=None):
        super().setUp({'EQ_DEV_MODE': True, 'EQ_PROFILING': True})

    def test_profiling_is_enabled(self):
        self.assertEqual(True, self._application.config['PROFILE'])


class TestApplicationProfilingDir(IntegrationTestCase):
    def setUp(self, setting_overrides=None):
        pass

    def test_profiling_directory_created(self):
        """
        Ensure that we try to create a profiling directory on startup (if enabled)
        :return:
        """
        with patch('app.setup.settings.EQ_PROFILING', True), patch(
            'app.setup.os.makedirs'
        ) as mkdir_mock, patch('app.setup.os.path.exists', return_value=False):
            super().setUp()
            self.assertEqual(mkdir_mock.called, True)
