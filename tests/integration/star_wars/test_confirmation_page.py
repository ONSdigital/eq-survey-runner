from tests.integration.integration_test_case import IntegrationTestCase


class TestConfirmationPage(IntegrationTestCase):

    def test_confirmation_page(self):
        self.rogue_one_login_and_check_introduction_text()
        self.post(action='start_questionnaire')

        self.rogue_one_check_character_page()

        # Form submission with no errors
        self.post({'character-answer': 'Cassian Andor'})
        self.assertInUrl('cassian-andor-like-this-page')

        # Like page
        self.rogue_one_check_description_page()

        # Form submission with no errors
        self.post({'cassian-andor-like-this-page-answer': 'Yes'})
        self.assertInUrl('film-takings')

        # Takings page
        self.rogue_one_check_takings_page()

        # Form submission with no errors
        self.post({'film-takings-answer': '900'})
        self.assertInUrl('summary')

        # Summary page
        self.rogue_one_check_confirmation_page()

        # Form submission with no errors
        self.post()
        self.assertInUrl('thank-you')

    def rogue_one_login_and_check_introduction_text(self):
        self.launchSurvey('0', 'rogue_one')
        self.rogue_one_check_introduction_text()

    def rogue_one_check_introduction_text(self):
        self.assertRegexPage('(?s)Rogue One')

    def rogue_one_check_character_page(self):
        self.assertInPage('Who do you want to know more about?')
        self.assertInPage('Jyn Erso')
        self.assertInPage('character-answer-3')

    def rogue_one_check_description_page(self):
        self.assertInPage('An accomplished Rebel Alliance Intelligence Officer')
        self.assertInPage('Do you like this page?')
        self.assertInPage('cassian-andor-like-this-page-answer-1')

    def rogue_one_check_takings_page(self):
        self.assertInPage('In millions, how much do you think this film will take?')
        self.assertInPage('film-takings-answer')

    def rogue_one_check_confirmation_page(self):
        self.assertInPage('Summary')
        self.assertInPage('Please check your responses carefully before submitting')
