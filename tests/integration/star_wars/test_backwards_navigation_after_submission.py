from .test_light_side_path import TestLightSidePath

class TestbackwardsNavigationAfterSubmission(TestLightSidePath):

    def test_backwards_navigation_star_wars(self):
        self.test_light_side_path()
        self.backwards_navigation()

    def backwards_navigation(self):
        eq_id = "0"
        resp = self.client.get('/questionnaire/' + eq_id + '/789/summary', follow_redirects=False)
        self.assertEquals(resp.status_code, 302)
        self.assertRegexpMatches(resp.headers['Location'], '\/thank-you$')

        # Block Two
        resp = self.client.get('/questionnaire/' + eq_id + '/789/an3b74d1-b687-4051-9634-a8f9ce10ard', follow_redirects=False)
        self.assertEquals(resp.status_code, 302)
        self.assertRegexpMatches(resp.headers['Location'], '\/thank-you$')

        # Block One
        resp = self.client.get('/questionnaire/' + eq_id + '/789/cd3b74d1-b687-4051-9634-a8f9ce10a27d', follow_redirects=False)
        self.assertEquals(resp.status_code, 302)
        self.assertRegexpMatches(resp.headers['Location'], '\/thank-you$')

        resp = self.client.get('/questionnaire/' + eq_id + '/789/introduction', follow_redirects=False)
        self.assertEquals(resp.status_code, 302)
        self.assertRegexpMatches(resp.headers['Location'], '\/thank-you$')
