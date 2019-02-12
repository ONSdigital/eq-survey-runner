from app.setup import cache
from tests.integration.integration_test_case import IntegrationTestCase


class TestApplicationVariables(IntegrationTestCase):

    def test_schema_is_cached(self):
        cache.init_app(self._application, config={'CACHE_TYPE': 'simple'})
        with self._application.app_context():
            self.assertEqual(len(cache.cache._cache), 0)  # pylint: disable=protected-access

            self.launchSurvey('test', 'textfield')
            self.assertStatusOK()
            self.assertNotEqual(cache.get('app.utilities.schema.load_schema_from_params_memver'), None)

            self.launchSurvey('test', 'textfield')
            self.assertStatusOK()
            self.assertNotEqual(cache.get('app.utilities.schema.load_schema_from_params_memver'), None)
