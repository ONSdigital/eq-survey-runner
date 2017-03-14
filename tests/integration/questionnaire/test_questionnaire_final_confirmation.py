from tests.integration.integration_test_case import IntegrationTestCase


class TestQuestionnaireFinalConfirmation(IntegrationTestCase):

    def test_final_confirmation_asked_at_end_of_questionnaire(self):
        # Given
        self.launchSurvey('test', 'final_confirmation')

        # When we proceed through the questionnaire
        self.post(action='start_questionnaire')
        self.assertInPage('What is your favourite breakfast food')
        self.post({'breakfast-answer': 'Bacon'})

        # Then we are presented with a confirmation page
        self.assertInUrl('confirmation')
        self.assertInPage('Thank you for your answers, do you wish to submit')
        self.assertInPage('Submit answers')

    def test_requesting_final_confirmation_before_finished_redirects(self):
        # Given
        self.launchSurvey('test', 'final_confirmation')

        # When we proceed through the questionnaire
        self.post(action='start_questionnaire')
        self.assertInPage('What is your favourite breakfast food')

        # And try posting straight to the confirmation screen
        self.post(url='/questionnaire/test/final_confirmation/789/final-confirmation/0/confirmation')

        # Then we are re-directed back
        self.assertInPage('What is your favourite breakfast food')
