from .test_light_side_path import TestLightSidePath
from tests.integration.star_wars import star_wars_test_urls


class TestBackwardsNavigationAfterSubmission(TestLightSidePath):

    def test_backwards_navigation_star_wars(self):
        self.test_light_side_path()
        self.backwards_navigation()

    def backwards_navigation(self):

        resp = self.client.get(star_wars_test_urls.STAR_WARS_INTRODUCTION, follow_redirects=False)
        self.assertEquals(resp.status_code, 401)

        # Block Three
        resp = self.client.get(star_wars_test_urls.STAR_WARS_BLOCK3, follow_redirects=False)
        self.assertEquals(resp.status_code, 401)

        # Block Two
        resp = self.client.get(star_wars_test_urls.STAR_WARS_BLOCK2, follow_redirects=False)
        self.assertEquals(resp.status_code, 401)

        # Block One
        resp = self.client.get(star_wars_test_urls.STAR_WARS_BLOCK1, follow_redirects=False)
        self.assertEquals(resp.status_code, 401)

        resp = self.client.get(star_wars_test_urls.STAR_WARS_INTRODUCTION, follow_redirects=False)
        self.assertEquals(resp.status_code, 401)
