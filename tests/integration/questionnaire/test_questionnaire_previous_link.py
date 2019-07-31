from tests.integration.integration_test_case import IntegrationTestCase


class TestQuestionnairePreviousLink(IntegrationTestCase):
    def test_previous_link_doesnt_appear_on_introduction(self):
        # Given
        self.launchSurvey('test_final_confirmation')
        # When we open the introduction
        # Then previous link does not appear
        self.assertNotInBody('Previous')

    def test_previous_link_doesnt_appear_on_page_following_introduction(self):
        # Given
        self.launchSurvey('test_final_confirmation')

        # When we proceed through the questionnaire
        self.post(action='start_questionnaire')
        self.assertInBody('Previous')
        self.post({'breakfast-answer': 'Bacon'})
        self.assertNotInUrl('thank-you')
        self.assertNotInBody('Previous')

    def test_previous_link_doesnt_appear_on_thank_you(self):
        # Given
        self.launchSurvey('test_final_confirmation')

        # When ee proceed through the questionnaire
        self.post(action='start_questionnaire')
        self.post({'breakfast-answer': 'Eggs'})
        self.post(action=None)
        self.assertInUrl('thank-you')
        self.assertNotInUrl('Previous')

    def test_previous_link_appears_on_questions_preceded_by_another_question(self):

        # Given a survey with multiple questions
        self.launchSurvey('test_checkbox')

        # When I answer a question
        self.assertInUrl('mandatory-checkbox')
        self.post({'mandatory-checkbox-answer': 'None'})

        # Then there should be a previous link on the current page
        self.assertInBody('Previous')

    def test_previous_link_appears_on_the_first_question_preceded_by_the_hub(self):

        # Given a survey with a hub enabled
        self.launchSurvey('test_hub_and_spoke')

        # When I answer go to the first question in a section
        self.assertInUrl('/')
        self.post()

        # Then there should be a previous link on the current page
        self.assertInBody('Previous')
