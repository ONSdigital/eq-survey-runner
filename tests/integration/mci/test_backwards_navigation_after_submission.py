from .test_happy_path import TestHappyPath
from tests.integration import test_urls

class TestBackwardsNavigationAfterSubmission(TestHappyPath):

    def test_backwards_navigation_205(self):
        self.test_happy_path_205()
        self.backwards_navigation()

    def backwards_navigation(self):

        resp = self.client.get(test_urls.SUMMARY_0205, follow_redirects=False)
        self.assertEquals(resp.status_code, 401)

        resp = self.client.get(test_urls.BLOCK1_0205, follow_redirects=False)
        self.assertEquals(resp.status_code, 401)

        resp = self.client.get(test_urls.INTRODUCTION_0205, follow_redirects=False)
        self.assertEquals(resp.status_code, 401)
