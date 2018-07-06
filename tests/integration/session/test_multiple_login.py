from tests.integration.integration_test_case import IntegrationTestCase


# pylint: disable=arguments-differ
class MultipleClientTestCase(IntegrationTestCase):
    def setUp(self):
        super().setUp()

        self.cache = {}

    def launchSurvey(self, client, eq_id='test', form_type_id='textfield', **payload_kwargs):
        token = self.token_generator.create_token(form_type_id=form_type_id, eq_id=eq_id, **payload_kwargs)
        self.get(client, '/session?token=' + token)

    def get(self, client, url, **kwargs):
        environ, response = client.get(
            url,
            as_tuple=True,
            follow_redirects=True,
            **kwargs
        )

        self._cache_response(client, environ, response)

    def post(self, client, post_data=None, url=None, action='save_continue', action_value='', **kwargs):
        cache = self.cache[client]

        if url is None:
            url = cache.get('last_url')

        self.assertIsNotNone(url)

        _post_data = (post_data.copy() or {}) if post_data else {}
        last_csrf_token = cache.get('last_csrf_token')
        if last_csrf_token is not None:
            _post_data.update({'csrf_token': last_csrf_token})

        if action:
            _post_data.update({'action[{action}]'.format(action=action): action_value})

        environ, response = client.post(
            url,
            data=_post_data,
            as_tuple=True,
            follow_redirects=True,
            **kwargs
        )

        self._cache_response(client, environ, response)

    def _cache_response(self, client, environ, response):
        cache = self.cache[client]

        cache['last_csrf_token'] = self._extract_csrf_token(response.get_data(True))
        cache['last_response'] = response
        cache['last_url'] = environ['PATH_INFO']
        if environ['QUERY_STRING']:
            cache['last_url'] += '?' + environ['QUERY_STRING']


class TestMultipleLogin(MultipleClientTestCase):

    def setUp(self):
        super().setUp()

        self.client_a = self._application.test_client()
        self.client_b = self._application.test_client()

        self.cache = {
            self.client_a: {},
            self.client_b: {}
        }

    def test_multiple_users_same_survey(self):
        """Tests that multiple sessions can be created which work on the same
        survey
        """
        input_data = 'foo bar'

        # user A inputs an answer
        self.launchSurvey(self.client_a, 'test', 'textfield')
        self.post(self.client_a, {'answer': input_data})

        # user B gets taken straight to summary as survey is complete
        self.launchSurvey(self.client_b, 'test', 'textfield')
        last_url_b = self.cache[self.client_b]['last_url']
        self.assertIn('/questionnaire/test/textfield/789/group/0/summary', last_url_b)

        # user B manually navigates to answer and can view the value that user A entered
        self.get(self.client_b, '/questionnaire/test/textfield/789/group/0/block')
        last_response_b = self.cache[self.client_b]['last_response']
        self.assertEqual(last_response_b.status_code, 200)
        self.assertIn(input_data, last_response_b.get_data(True))

        # user A continues through playback page and submits
        self.post(self.client_a, {})
        self.post(self.client_a, action=None)

        # user B tries to submit value
        self.post(self.client_b, {'answer': 'bar baz'})
        last_response_b = self.cache[self.client_b]['last_response']
        self.assertEqual(last_response_b.status_code, 401)
