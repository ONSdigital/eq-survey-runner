from tests.integration.mci import mci_test_urls
from .test_happy_path import TestHappyPath


class TestBackwardsNavigationAfterSubmission(TestHappyPath):

    def test_backwards_navigation_205(self):
        self.test_happy_path_205()
        self.backwards_navigation()

    def backwards_navigation(self):

        resp = self.client.get(mci_test_urls.MCI_0205_SUMMARY, follow_redirects=False)
        self.assertEqual(resp.status_code, 401)

        resp = self.client.get(mci_test_urls.MCI_0205_BLOCK1, follow_redirects=False)
        self.assertEqual(resp.status_code, 401)

        resp = self.client.get(mci_test_urls.MCI_0205_INTRODUCTION, follow_redirects=False)
        self.assertEqual(resp.status_code, 401)
