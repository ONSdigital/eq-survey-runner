from tests.integration.integration_test_case import IntegrationTestCase
from tests.integration.mci import mci_test_urls


class TestQuestionnaireEndpointRedirects(IntegrationTestCase):

    def test_get_invalid_questionnaire_location_redirects_to_latest(self):
        # Given
        self.launchSurvey('1', '0205')

        # When
        self.get(mci_test_urls.MCI_0205_BASE + 'test')

        # Then
        self.assertInUrl(mci_test_urls.MCI_0205_INTRODUCTION)

    def test_post_invalid_questionnaire_location_redirects_to_latest(self):
        # Given
        self.launchSurvey('1', '0205')

        # When
        self.post(url=mci_test_urls.MCI_0205_BASE + 'test')

        # Then
        self.assertInUrl(mci_test_urls.MCI_0205_INTRODUCTION)

    def test_submit_answers_for_invalid_questionnaire_location_redirects_to_first_incomplete_location(self):
        # Given
        self.launchSurvey('1', '0205')

        # When
        self.post(url=mci_test_urls.MCI_0205_SUMMARY)

        # Then
        self.assertInUrl(mci_test_urls.MCI_0205_INTRODUCTION)
