from .test_happy_path import TestHappyPath


class TestBackwardsNavigationAfterSubmission(TestHappyPath):

    def test_backwards_navigation_205(self):
        self.test_happy_path_205()
        self.backwards_navigation()

    def backwards_navigation(self):
        eq_id = "1"
        resp = self.client.get('/questionnaire/' + eq_id + '/0205/201604/789/summary', follow_redirects=False)
        self.assertEquals(resp.status_code, 401)

        resp = self.client.get('/questionnaire/' + eq_id + '/0205/201604/789/cd3b74d1-b687-4051-9634-a8f9ce10a27d', follow_redirects=False)
        self.assertEquals(resp.status_code, 401)

        resp = self.client.get('/questionnaire/' + eq_id + '/0205/201604/789/introduction', follow_redirects=False)
        self.assertEquals(resp.status_code, 401)
