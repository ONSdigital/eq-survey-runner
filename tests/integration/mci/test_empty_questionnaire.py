from tests.integration.integration_test_case import IntegrationTestCase
from tests.integration.mci import mci_test_urls


class TestEmptyQuestionnaire(IntegrationTestCase):

    def test_empty_questionnaire(self):
        self.launchSurvey('1', '0205')

        # We are on the landing page
        self.assertInPage('>Start survey<')

        # Submit the Introduction page to get the first question page
        self.post(action='start_questionnaire')
        self.assertInUrl(mci_test_urls.MCI_0205_BLOCK1)
        first_question_page_url = self.last_url

        # We try to access the submission page without entering anything
        self.get(mci_test_urls.MCI_0205_SUMMARY)

        # Check we are redirected back to the questionnaire
        self.assertEqualUrl(first_question_page_url)

        # We try posting to the submission page without our answers
        self.post(url=mci_test_urls.MCI_0205_SUMMARY)

        # Check we are redirected back to the questionnaire
        self.assertEqualUrl(first_question_page_url)
