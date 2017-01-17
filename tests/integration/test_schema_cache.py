from app import cache
from tests.integration.create_token import create_token
from tests.integration.integration_test_case import IntegrationTestCase


class TestApplicationVariables(IntegrationTestCase):

    def test_schema_is_cached(self):
        with self.application.app_context():

            self.assertEqual(len(cache.cache._cache), 0)  # pylint: disable=protected-access

            token = create_token('star_wars', '0')
            resp = self.client.get('/session?token=' + token.decode(), follow_redirects=True)

            self.assertEqual(resp.status_code, 200)

            self.assertNotEqual(cache.get('app.utilities.schema.load_and_parse_schema_memver'), None)

            resp = self.client.get('/session?token=' + token.decode(), follow_redirects=True)

            self.assertEqual(resp.status_code, 200)

            self.assertNotEqual(cache.get('app.utilities.schema.load_and_parse_schema_memver'), None)
