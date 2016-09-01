from .test_light_side_path import TestLightSidePath


class TestBackwardsNavigationAfterSubmission(TestLightSidePath):

    def test_backwards_navigation_star_wars(self):
        self.test_light_side_path()
        self.backwards_navigation()

    def backwards_navigation(self):
        eq_id = "0"
        resp = self.client.get('/questionnaire/' + eq_id + '/star_wars/201604/789/summary', follow_redirects=False)
        self.assertEquals(resp.status_code, 401)

        # Block Three
        resp = self.client.get('/questionnaire/' + eq_id + '/star_wars/201604/789/0e41e80a-f45a-2dfd-9fe0-55cc2c7807d0', follow_redirects=False)
        self.assertEquals(resp.status_code, 401)

        # Block Two
        resp = self.client.get('/questionnaire/' + eq_id + '/star_wars/201604/789/0e41e80a-f45a-2dfd-9fe0-55cc2c7807d9', follow_redirects=False)
        self.assertEquals(resp.status_code, 401)

        # Block One
        resp = self.client.get('/questionnaire/' + eq_id + '/star_wars/201604/789/0e41e80a-f45a-4dfd-9ae0-55cc2c7807d9', follow_redirects=False)
        self.assertEquals(resp.status_code, 401)

        resp = self.client.get('/questionnaire/' + eq_id + '/star_wars/201604/789/introduction', follow_redirects=False)
        self.assertEquals(resp.status_code, 401)

