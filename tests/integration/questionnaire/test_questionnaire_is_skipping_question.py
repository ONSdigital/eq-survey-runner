from tests.integration.integration_test_case import IntegrationTestCase


class TestQuestionnaireChangeAnswer(IntegrationTestCase):

    def test_section_summary_not_available_if_section_incomplete(self):

        # Given I launched a survey and have not answered any questions
        self.launchSurvey('test', 'is_skipping_question')

        # When I try access a section summary
        self.get('questionnaire/test/is_skipping_question/789/test-skipping-section-summary-group/0/test-skipping-section-summary')

        # Then I should be redirected to the first incomplete question in that section
        self.assertInPage('This is section 1')
        self.assertInPage('Were you forced to complete section 1?')

    def test_section_summary_not_available_after_invalidating_section(self):

        # Given I launched a survey and have completed a section
        self.launchSurvey('test', 'is_skipping_question')
        self.post({'test-skipping-answer': 'No'})
        self.assertInPage('This section is now complete')
        self.assertInPage('Were you forced to complete section 1?')

        # When I invalidate the section and try access it's section summary
        self.get('questionnaire/test/is_skipping_question/789/test-skipping-group/0/test-skipping-forced#test-skipping-answer')
        self.post({'test-skipping-answer': 'Yes'})
        self.get('questionnaire/test/is_skipping_question/789/test-skipping-section-summary-group/0/test-skipping-section-summary')

        # Then I should be redirected to the first incomplete question in that section
        self.assertInPage('This is section 1')
        self.assertInPage('What would incentivise you to complete this section?')

    def test_final_summary_not_available_if_any_question_incomplete(self):

        # Given I launched a survey and have not answered any questions
        self.launchSurvey('test', 'is_skipping_question')

        # When I try access the final summary
        self.get('questionnaire/test/is_skipping_question/789/summary-group/0/summary')

        # Then I should be redirected to the first incomplete question in the survey
        self.assertInPage('This is section 1')
        self.assertInPage('Were you forced to complete section 1?')

    def test_final_summary_not_available_after_invalidating_section(self):

        # Given I launched a survey and have answered all questions
        self.launchSurvey('test', 'is_skipping_question')
        self.post({'test-skipping-answer': 'No'})
        self.assertInPage('This section is now complete')
        self.assertInPage('Were you forced to complete section 1?')
        self.post(action='save_continue')

        self.post({'test-skipping-answer-2': 'No'})
        self.assertInPage('This section is now complete')
        self.assertInPage('Were you forced to complete section 2?')
        self.post(action='save_continue')

        self.assertInPage('Please check your answers carefully before submitting.')
        self.assertInPage('Were you forced to complete section 1?')
        self.assertInPage('Were you forced to complete section 2?')
        self.assertInPage('Submit answers')

        # When I invalidate any block and try access the final summary
        self.get('questionnaire/test/is_skipping_question/789/test-skipping-group-2/0/test-skipping-forced-2#test-skipping-answer-2')
        self.post({'test-skipping-answer-2': 'Yes'})

        self.get('questionnaire/test/is_skipping_question/789/test-skipping-group/0/test-skipping-forced#test-skipping-answer')
        self.post({'test-skipping-answer': 'Yes'})

        self.get('questionnaire/test/is_skipping_question/789/summary-group/0/summary')

        # Then I should be redirected to the first incomplete question in the survey
        self.assertInPage('This is section 1')
        self.assertInPage('What would incentivise you to complete this section?')
