from .test_happy_path import TestHappyPath

class TestbackwardsNavigationAfterSubmission(TestHappyPath):

    def test_backwards_navigation_205(self):
        self.test_happy_path()
        self.backwards_navigation()

    def backwards_navigation(self):
        resp = self.client.get('/questionnaire/summary', follow_redirects=False)
        self.assertEquals(resp.status_code, 302)
        self.assertRegexpMatches(resp.headers['Location'], '\/thank-you$')

        # Block Three
        resp = self.client.get('/questionnaire/0e41e80a-f45a-2dfd-9fe0-55cc2c7807d0', follow_redirects=False)
        self.assertEquals(resp.status_code, 302)
        self.assertRegexpMatches(resp.headers['Location'], '\/thank-you$')

        # Block Two
        resp = self.client.get('/questionnaire/0e41e80a-f45a-2dfd-9fe0-55cc2c7807d9', follow_redirects=False)
        self.assertEquals(resp.status_code, 302)
        self.assertRegexpMatches(resp.headers['Location'], '\/thank-you$')

        # Block One
        resp = self.client.get('/questionnaire/0e41e80a-f45a-4dfd-9ae0-55cc2c7807d9', follow_redirects=False)
        self.assertEquals(resp.status_code, 302)
        self.assertRegexpMatches(resp.headers['Location'], '\/thank-you$')

        resp = self.client.get('/questionnaire/introduction', follow_redirects=False)
        self.assertEquals(resp.status_code, 302)
        self.assertRegexpMatches(resp.headers['Location'], '\/thank-you$')
