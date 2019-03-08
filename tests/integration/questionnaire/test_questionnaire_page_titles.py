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
        self.assertEqualPageTitle("We\'ve received your answers - Final confirmation to submit")

    def test_session_expired_page_title(self):
        # Given
        self.launchSurvey('test', 'final_confirmation')
        # When
        self.get('/session-expired')
        # Then
        self.assertEqualPageTitle('Session expired')

    def test_should_have_group_title_in_page_title_when_interstitial(self):
        # Given
        self.launchSurvey('test', 'interstitial_page')
        self.post(action='start_questionnaire')
        # When
        self.post({'favourite-breakfast': ''})
        # Then
        self.assertEqualPageTitle('Favourite food - Interstitial Pages')

    def test_html_stripped_from_page_titles(self):
        """
        Checks for https://github.com/ONSdigital/eq-survey-runner/issues/1036
        """
        # Given
        self.launchSurvey('test', 'markup')
        # When
        # Then
        self.assertEqualPageTitle('This is a title with emphasis - Markup test')
