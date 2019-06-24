from app.setup import cache
from tests.integration.integration_test_case import IntegrationTestCase


class TestApplicationVariables(IntegrationTestCase):
    def test_schema_is_cached(self):
        cache.init_app(self._application, config={'CACHE_TYPE': 'simple'})
        with self._application.app_context():
            cache_length = len(cache.cache._cache)  # pylint: disable=protected-access
            self.assertEqual(cache_length, 0)

            self.launchSurvey('test_textfield')
            self.assertStatusOK()
            self.assertNotEqual(
                cache.get('app.utilities.schema.load_schema_from_name_memver'), None
            )

            self.launchSurvey('test_textfield')
            self.assertStatusOK()
            self.assertNotEqual(
                cache.get('app.utilities.schema.load_schema_from_name_memver'), None
            )
