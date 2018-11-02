from tests.integration.integration_test_case import IntegrationTestCase

class TestCookie(IntegrationTestCase):

    def test_cookie_contents(self):
        self.launchSurvey()
        cookie = self.getCookie()

        self.assertIsNotNone(cookie.get('_fresh'))
        self.assertIsNotNone(cookie.get('_permanent'))
        self.assertIsNotNone(cookie.get('csrf_token'))
        self.assertIsNotNone(cookie.get('eq-session-id'))
        self.assertIsNotNone(cookie.get('expires_in'))
        self.assertIsNotNone(cookie.get('survey_title'))
        self.assertIsNotNone(cookie.get('theme'))
        self.assertIsNotNone(cookie.get('user_ik'))
        self.assertEqual(len(cookie), 8)

        self.assertIsNone(cookie.get('user_id'))
