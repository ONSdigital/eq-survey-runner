import unittest

from app.utilities.cookies import analytics_allowed


class MockRequest:

    def __init__(self, value):
        self.cookies = dict(ons_cookie_policy=value)


class TestAnalyticsAllowed(unittest.TestCase):

    def test_with_cookie_usage_false(self):
        request = MockRequest("{'essential': true, 'usage': false}")
        self.assertFalse(analytics_allowed(request))

    def test_with_cookie_usage_true(self):
        request = MockRequest("{'essential': true, 'usage': true}")
        self.assertTrue(analytics_allowed(request))

    def test_with_cookie_usage_true_double_quotes(self):
        request = MockRequest('{"essential": true, "usage": true}')
        self.assertTrue(analytics_allowed(request))
