from tests.integration.mci import mci_test_urls
from tests.integration.integration_test_case import IntegrationTestCase

from .test_happy_path import HappyPathHelperMixin


class TestBackwardsNavigationAfterSubmission(IntegrationTestCase, HappyPathHelperMixin):

    def test_backwards_navigation_205(self):
        self._happy_path('0205', 'test')
        self.backwards_navigation()

    def backwards_navigation(self):
        self.get(mci_test_urls.MCI_0205_SUMMARY)
        self.assertStatusUnauthorised()

        self.get(mci_test_urls.MCI_0205_BLOCK1)
        self.assertStatusUnauthorised()

        self.get(mci_test_urls.MCI_0205_INTRODUCTION)
        self.assertStatusUnauthorised()
