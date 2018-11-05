from tests.integration.star_wars import star_wars_test_urls, STAR_WARS_TRIVIA_PART_1_DEFAULT_ANSWERS
from tests.integration.star_wars.star_wars_tests import StarWarsTestCase


class TestEmptyRadioBoxes(StarWarsTestCase):

    def test_radio_boxes_mandatory_empty(self):
        self.launchSurvey()

        self.start_questionnaire_and_navigate_routing()

        # We fill in the survey without a mandatory radio box
        form_data = STAR_WARS_TRIVIA_PART_1_DEFAULT_ANSWERS.copy()
        del form_data['tie-fighter-sound-answer']

        # We submit the form
        self.post(form_data)

        # We stay on the current page
        self.assertInBody('Star Wars Quiz')
        self.assertInBody('May the force be with you young EQ developer')
        self.assertInBody('This page has an error')
        self.assertInBody('This <strong>must be corrected</strong> to continue.')
        self.assertInBody('Select an answer to continue.')

        # We submit the form
        self.post(STAR_WARS_TRIVIA_PART_1_DEFAULT_ANSWERS)

        # There are no validation errors
        self.assertInUrl(star_wars_test_urls.STAR_WARS_TRIVIA_PART_2)

        # Check we are on the next page
        self.assertInBody("Why doesn't Chewbacca receive a medal at the end of A New Hope?")
