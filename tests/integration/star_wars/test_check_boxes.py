from tests.integration.star_wars import star_wars_test_urls, STAR_WARS_TRIVIA_PART_1_DEFAULT_ANSWERS
from tests.integration.star_wars.star_wars_tests import StarWarsTestCase


class TestEmptyCheckBoxes(StarWarsTestCase):

    def test_check_boxes_mandatory_empty(self):
        self.launchSurvey()

        self.start_questionnaire_and_navigate_routing()

        # We fill in the survey without a mandatory check box
        form_data = STAR_WARS_TRIVIA_PART_1_DEFAULT_ANSWERS.copy()

        # Skip this question
        del form_data['green-lightsaber-answer']

        # We submit the form
        self.post(form_data)

        # We stay on the current page
        self.assertInPage('Star Wars Quiz')
        self.assertInPage('May the force be with you young EQ developer')
        self.assertInPage('This page has 1 errors')
        self.assertInPage('Select all that apply to continue.')

        # We correct the error
        self.post(STAR_WARS_TRIVIA_PART_1_DEFAULT_ANSWERS)

        # There are no validation errors
        self.assertInUrl(star_wars_test_urls.STAR_WARS_TRIVIA_PART_2)

        self.check_second_quiz_page()
