from .test_happy_path import TestHappyPath

class TestbackwardsNavigationAfterSubmission(TestHappyPath):

    def test_backwards_navigation_205(self):
        self.test_happy_path_205()
        self.backwards_navigation()

    def backwards_navigation(self):
        resp = self.client.get('/questionnaire/summary', follow_redirects=False)
        self.assertEquals(resp.status_code, 302)
        self.assertRegexpMatches(resp.headers['Location'], '\/thank-you$')

        resp = self.client.get('/questionnaire/cd3b74d1-b687-4051-9634-a8f9ce10a27d', follow_redirects=False)
        self.assertEquals(resp.status_code, 302)
        self.assertRegexpMatches(resp.headers['Location'], '\/thank-you$')

        resp = self.client.get('/questionnaire/introduction', follow_redirects=False)
        self.assertEquals(resp.status_code, 302)
        self.assertRegexpMatches(resp.headers['Location'], '\/thank-you$')
