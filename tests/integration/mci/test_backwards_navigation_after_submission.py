from .test_happy_path import TestHappyPath

class TestbackwardsNavigationAfterSubmission(TestHappyPath):

    def test_backwards_navigation(self):
        self.test_happy_path()

        resp = self.client.get('/submission', follow_redirects=False)
        self.assertEquals(resp.status_code, 302)
        self.assertRegexpMatches(resp.headers['Location'], '\/thank-you$')

        resp = self.client.get('/questionnaire', follow_redirects=False)
        self.assertEquals(resp.status_code, 302)
        self.assertRegexpMatches(resp.headers['Location'], '\/thank-you$')

        resp = self.client.get('/landing-page', follow_redirects=False)
        self.assertEquals(resp.status_code, 302)
        self.assertRegexpMatches(resp.headers['Location'], '\/thank-you$')
