from tests.integration.star_wars import STAR_WARS_TRIVIA_PART_1_DEFAULT_ANSWERS
from tests.integration.star_wars.star_wars_tests import StarWarsTestCase


class TestPiping(StarWarsTestCase):

    def test_piping_employment_date(self):
        self.launchSurvey()

        self.start_questionnaire_and_navigate_routing()

        # We submit the form
        self.post(STAR_WARS_TRIVIA_PART_1_DEFAULT_ANSWERS)

        # We are in the Questionnaire
        self.assertInPage('On 2 June 1983 how many were employed?')

    def test_piping_an_answer(self):
        self.launchSurvey()

        self.start_questionnaire_and_navigate_routing()

        # Form submission with no errors
        self.post(STAR_WARS_TRIVIA_PART_1_DEFAULT_ANSWERS)
        self.assertInUrl('star-wars-trivia-part-2')

        # Pipe Test for section title
        self.assertInPage('On 2 June 1983 how many were employed?')

        # Textarea question
        self.assertInPage('Why doesn\'t Chewbacca receive a medal at the end of A New Hope?')
        self.assertInPage('chewbacca-medal-answer')

        # Check Cheewies Age has been correctly piped into the question text
        self.assertInPage("Do you really think that Chewbacca is 234 years old?")
