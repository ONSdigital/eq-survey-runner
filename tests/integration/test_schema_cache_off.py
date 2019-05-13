from flask_caching.backends.null import NullCache

from app.setup import cache
from tests.integration.integration_test_case import IntegrationTestCase


class TestApplicationVariables(IntegrationTestCase):
    def setUp(self, setting_overrides=None):
        super().setUp({
            'EQ_ENABLE_CACHE': False
        })

    def test_schema_is_cached(self):
        with self._application.app_context():
            self.assertTrue(isinstance(cache.cache, NullCache))
