import unittest
from tests.integration.integration_test_case import IntegrationTestCase


class TestQuestionnairePageTitles(IntegrationTestCase):

    def test_should_have_question_in_page_title_when_loading_introduction(self):
        # Given, When
        self.launchSurvey('test', 'final_confirmation')
        # Then
        self.assertEqualPageTitle('Final confirmation to submit')

    def test_should_have_question_in_page_title_when_loading_questionnaire(self):
        # Given
        self.launchSurvey('test', 'final_confirmation')
        # When
        self.post(action='start_questionnaire')
        # Then
        self.assertEqualPageTitle('What is your favourite breakfast food - Final confirmation to submit')

    def test_should_have_question_in_page_title_when_loading_confirmation(self):
        # Given
        self.launchSurvey('test', 'final_confirmation')
        # When
        self.post(action='start_questionnaire')
        self.post({'breakfast-answer': ''})
        # Then
        self.assertEqualPageTitle('Submit answers - Final confirmation to submit')

    def test_should_have_question_in_page_title_when_loading_summary(self):
        # Given
        self.launchSurvey('test', 'percentage')
        # When
        self.post({'answer': ''})
        # Then
        self.assertEqualPageTitle('Summary - Percentage Field Demo')

    def test_should_have_survey_in_page_title_when_thank_you(self):
        # Given
        self.launchSurvey('test', 'final_confirmation')
        self.post(action='start_questionnaire')
        self.post({'breakfast-answer': ''})
        # When submit
        self.post(action=None)
        # Then
        self.assertEqualPageTitle('We\'ve received your answers - Final confirmation to submit')

    def test_should_have_survey_in_page_title_when_sign_out(self):
        # Given
        self.launchSurvey('test', 'final_confirmation')
        # When
        self.get('/questionnaire/test/final_confirmation/789/signed-out')
        # Then
        self.assertEqualPageTitle('Signed out - Final confirmation to submit')

    def test_should_have_survey_in_page_title_when_session_expired(self):
        # Given
        self.launchSurvey('test', 'final_confirmation')
        # When
        self.get('/questionnaire/test/final_confirmation/789/session-expired')
        # Then
        self.assertEqualPageTitle('Session expired - Final confirmation to submit')

    @unittest.expectedFailure
    def test_should_have_clean_page_title_when_not_authenticated_session_expired(self):
        """
        This is a failing test due to https://github.com/ONSdigital/eq-survey-runner/issues/1032
        """
        # Given
        self.launchSurvey('test', 'final_confirmation')
        # When
        self.get('/questionnaire/test/final_confirmation/789/session-expired')
        # Get again now that we're expired
        self.get('/questionnaire/test/final_confirmation/789/session-expired')
        # Then
        self.assertEqualPageTitle('Session expired')

    def test_should_have_survey_in_page_title_when_error(self):
        # Given
        self.launchSurvey('test', 'final_confirmation')
        # When
        self.get('/questionnaire/test/final_confirmation/789/non-existent-block')
        # Then
        self.assertEqualPageTitle('Error 404')

    def test_should_have_group_title_in_page_title_when_interstitial(self):
        # Given
        self.launchSurvey('test', 'interstitial_page')
        self.post(action='start_questionnaire')
        # When
        self.post({'favourite-breakfast': ''})
        # Then
        self.assertEqualPageTitle('Favourite food - Interstitial Pages')
