import re
import unittest
import json

from bs4 import BeautifulSoup

from app.setup import create_app

from tests.integration.create_token import TokenGenerator


class IntegrationTestCase(unittest.TestCase):  # pylint: disable=too-many-public-methods

    def setUp(self):
        # Cache for requests
        self.last_url = None
        self.last_response = None
        self.last_csrf_token = None

        # Perform setup steps
        self._setUpApp()

    def _setUpApp(self):
        setting_overrides = {
            "EQ_SERVER_SIDE_STORAGE_DATABASE_DRIVER": "sqlite",
            "EQ_SERVER_SIDE_STORAGE_DATABASE_NAME": ""
        }
        self._application = create_app(setting_overrides)
        self.token_generator = TokenGenerator(
            self._application.config['EQ_USER_AUTHENTICATION_RRM_PRIVATE_KEY'],
            self._application.config['EQ_USER_AUTHENTICATION_RRM_PRIVATE_KEY_PASSWORD'],
            self._application.config['EQ_USER_AUTHENTICATION_SR_PUBLIC_KEY'],
        )

        self._client = self._application.test_client()

    def launchSurvey(self, eq_id='test', form_type_id='radio', **payload_kwargs):
        """
        Launch a survey as an authenticated user and follow re-directs
        :param eq_id: The id of the survey to launch e.g. 'census', 'test' etc.
        :param form_type_id: The form type of the survey e.g. 'household', 'radio' etc.
        """
        token = self.token_generator.create_token(form_type_id=form_type_id, eq_id=eq_id, **payload_kwargs)
        self.get('/session?token=' + token.decode())

    def dumpAnswers(self):

        self.get('/dump/answers')

        # Then I get a 200 OK response
        self.assertStatusOK()

        # And the JSON response contains the data I submitted
        dump_answers = json.loads(self.getResponseData())
        return dump_answers

    def dumpSubmission(self):

        self.get('/dump/submission')

        # Then I get a 200 OK response
        self.assertStatusOK()

        # And the JSON response contains the data I submitted
        dump_submission = json.loads(self.getResponseData())
        return dump_submission

    def get(self, url):
        """
        GETs the specified URL, following any redirects.

        If the response contains a CSRF token; it is cached to be use on
        the next POST.

        The URL will be cached for future POST requests.

        :param url: the URL to GET
        """
        environ, response = self._client.get(url, as_tuple=True, follow_redirects=True)

        self._cache_response(environ, response)

    def post(self, post_data=None, url=None, action='save_continue', action_value=''):
        """
        POSTs to the specified URL with post_data and performs a GET
        with the URL from the re-direct.

        Will add the last received CSRF token to the post_data automatically.

        :param url: the URL to POST to; use None to use the last received URL
        :param post_data: the data to POST
        :param action: The button action to post
        """
        if url is None:
            url = self.last_url

        self.assertIsNotNone(url)

        _post_data = post_data and post_data.copy() or {}
        if self.last_csrf_token is not None:
            _post_data.update({'csrf_token': self.last_csrf_token})

        if action:
            _post_data.update({'action[{action}]'.format(action=action): action_value})

        environ, response = self._client.post(url, data=_post_data, as_tuple=True, follow_redirects=True)

        self._cache_response(environ, response)

    def _cache_response(self, environ, response):
        self.last_csrf_token = self._extract_csrf_token(response.get_data(True))
        self.last_response = response
        self.last_url = environ['PATH_INFO']
        if environ['QUERY_STRING']:
            self.last_url += "?" + environ['QUERY_STRING']

    @staticmethod
    def _extract_csrf_token(html):
        match = re.search('<input id="csrf_token" name="csrf_token" type="hidden" value="(.+?)">', html)
        return match and match.group(1) or None

    def getResponseData(self):
        """
        Returns the last received response data
        """
        return self.last_response.get_data(True)

    def getHtmlSoup(self):
        """
        Returns the last received response data as a BeautifulSoup HTML object
        See https://www.crummy.com/software/BeautifulSoup/bs4/doc/
        :return: a BeautifulSoup object for the response data
        """
        return BeautifulSoup(self.getResponseData(), 'html.parser')

    # Extra Helper Assertions
    def assertInPage(self, content, message=None):
        self.assertIn(member=content, container=self.getResponseData(), msg=message)

    def assertNotInPage(self, content, message=None):
        self.assertNotIn(member=content, container=self.getResponseData(), msg=message)

    def assertRegexPage(self, regex, message=None):
        self.assertRegex(text=self.getResponseData(), expected_regex=regex, msg=message)

    def assertEqualPageTitle(self, title):
        self.assertEqual(self.getHtmlSoup().title.string, title)   # pylint: disable=no-member

    def assertStatusOK(self):
        self.assertStatusCode(200)

    def assertStatusUnauthorised(self):
        self.assertStatusCode(401)

    def assertStatusForbidden(self):
        self.assertStatusCode(403)

    def assertStatusNotFound(self):
        self.assertStatusCode(404)

    def assertStatusCode(self, status_code):
        if self.last_response is not None:
            self.assertEqual(self.last_response.status_code, status_code)
        else:
            self.fail('last_response is invalid')

    def assertEqualUrl(self, url):
        if self.last_url:
            self.assertEqual(url, self.last_url)
        else:
            self.fail('last_url is invalid')

    def assertInUrl(self, content):
        if self.last_url:
            self.assertIn(content, self.last_url)
        else:
            self.fail('last_url is invalid')

    def assertNotInUrl(self, content):
        if self.last_url:
            self.assertNotIn(content, self.last_url)
        else:
            self.fail('last_url is invalid')

    def assertRegexUrl(self, regex):
        if self.last_url:
            self.assertRegex(text=self.last_url, expected_regex=regex)
        else:
            self.fail('last_url is invalid')
