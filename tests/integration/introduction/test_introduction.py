from datetime import datetime
from tests.integration.integration_test_case import IntegrationTestCase


class TestIntroduction(IntegrationTestCase):

    def test_mail_link_contains_ru_ref_in_subject(self):
        # Given a business survey
        self.launchSurvey('1', '0203')

        # When on the landing page
        # Then the email link is present with the ru_ref in the subject
        self.assertRegexPage(r'\"mailto\:.+\?subject\=.+123456789012A\"')

    def test_intro_description_displayed(self):
        # Given survey containing intro description
        self.launchSurvey('1', '0112')

        # When on the introduction page
        # Then description should be displayed
        self.assertInPage('qa-intro-description')

    def test_intro_description_not_displayed(self):
        # Given survey without introduction description
        self.launchSurvey('test', 'textfield')

        # When on the introduction page
        # Then description should not be displayed
        self.assertNotInPage('qa-intro-description')

    def test_intro_basis_for_completion_displayed(self):
        # Given survey with basis for completion
        self.launchSurvey('2', '0001')

        # When on the introduction page
        # Then basis for completion should be displayed
        self.assertInPage('Information you need')

    def test_intro_basis_for_completion_not_displayed(self):
        # Given survey without basis for completion
        self.launchSurvey('1', '0112')

        # When on the introduction page
        # Then basis for completion should not be displayed
        self.assertNotInPage('basis-for-completion')

    def test_start_survey_sets_started_at(self):
        # Given survey with a start survey button
        self.launchSurvey('1', '0112', roles=['dumper'])

        self.post(action='start_questionnaire')

        # When start survey button is pressed,
        # Then started_at should be set in collection_metadata (and payload)
        actual = self.dumpSubmission()['submission']

        started_at_datetime = datetime.strptime(actual['started_at'], '%Y-%m-%dT%H:%M:%S.%f')

        self.assertIsNotNone(started_at_datetime)
