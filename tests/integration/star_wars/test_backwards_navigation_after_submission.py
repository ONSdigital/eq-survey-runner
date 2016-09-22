from .test_light_side_path import TestLightSidePath
from tests.integration import test_urls

class TestBackwardsNavigationAfterSubmission(TestLightSidePath):

    def test_backwards_navigation_star_wars(self):
        self.test_light_side_path()
        self.backwards_navigation()

    def backwards_navigation(self):

        resp = self.client.get(test_urls.INTRODUCTION_STAR_WARS, follow_redirects=False)
        self.assertEquals(resp.status_code, 401)

        # Block Three
        resp = self.client.get(test_urls.BLOCK3_STAR_WARS, follow_redirects=False)
        self.assertEquals(resp.status_code, 401)

        # Block Two
        resp = self.client.get(test_urls.BLOCK2_STAR_WARS, follow_redirects=False)
        self.assertEquals(resp.status_code, 401)

        # Block One
        resp = self.client.get(test_urls.BLOCK1_STAR_WARS, follow_redirects=False)
        self.assertEquals(resp.status_code, 401)

        resp = self.client.get(test_urls.INTRODUCTION_STAR_WARS, follow_redirects=False)
        self.assertEquals(resp.status_code, 401)
