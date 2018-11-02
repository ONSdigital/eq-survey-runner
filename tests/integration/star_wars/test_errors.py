from tests.integration.star_wars import STAR_WARS_TRIVIA_PART_1_DEFAULT_ANSWERS
from tests.integration.star_wars.star_wars_tests import StarWarsTestCase


class TestPageErrors(StarWarsTestCase):
    def test_multi_page_errors(self):
        self.launchSurvey()

        self.start_questionnaire_and_navigate_routing()
        first_page = self.last_url

        self.post(STAR_WARS_TRIVIA_PART_1_DEFAULT_ANSWERS)
        self.assertInUrl('star-wars-trivia-part-2')

        # Second page
        self.check_second_quiz_page()

        # Our answers
        self.post({'chewbacca-medal-answer': ''})

        # We fill in our answers missing one required field
        form_data = STAR_WARS_TRIVIA_PART_1_DEFAULT_ANSWERS.copy()
        del form_data['tie-fighter-sound-answer']

        # We submit the form
        self.post(url=first_page, post_data=form_data)

        self.assertInBody('href="#container-tie-fighter-sound-answer"')

        # We DO NOT have the error from page two
        self.assertNotInBody('href="chewbacca-medal-answer"')

    def test_skip_question_errors(self):
        # Given on the page with skip question with skip condition
        self.launchSurvey('test', 'skip_condition')
        self.post(action='start_questionnaire')
        self.post({'food-answer': 'Bacon'})

        # When submit no answers which is invalid
        self.post()

        # Then errors exists on page
        self.assertStatusOK()
        self.assertInBody('This page has an error')
        self.assertInBody('This <strong>must be corrected</strong> to continue.')

    def test_mutliple_validation_errors(self):
        # Given on the page with two mandatory fields
        self.launchSurvey('test', 'numbers')
        self.post(action='start_questionnaire')

        # When submitted without answering
        self.post()

        # Then errors exists on page
        self.assertStatusOK()
        self.assertInBody('This page has 2 errors')
        self.assertInBody('These <strong>must be corrected</strong> to continue.')
