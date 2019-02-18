from tests.integration.integration_test_case import IntegrationTestCase


class TestQuestionnaireChangeAnswer(IntegrationTestCase):

    def test_question_is_skipped(self):

        # Given I launched a survey and have not answered any questions
        self.launchSurvey('test', 'skip_condition_question')

        # When I provide answers that should skip
        self.post({
            'do-you-want-to-skip-first-answer': 'Yes',
            'do-you-want-to-skip-second-answer': 'Yes',
        })

        self.assertInUrl('should-skip')

        # Then the answer is not displayed
        self.assertNotInBody('Was I skipped?')

    def test_question_is_not_skipped(self):

        # Given I launched a survey and have not answered any questions
        self.launchSurvey('test', 'skip_condition_question')

        # When I provide answers that should not skip
        self.post({
            'do-you-want-to-skip-first-answer': 'No',
            'do-you-want-to-skip-second-answer': 'No',
        })

        self.assertInUrl('should-skip')

        # Then the answer is displayed
        self.assertInBody('Was I skipped?')
