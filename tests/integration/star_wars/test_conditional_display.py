from tests.integration.star_wars import star_wars_test_urls, \
    STAR_WARS_TRIVIA_PART_1_DEFAULT_ANSWERS, \
    STAR_WARS_TRIVIA_PART_2_DEFAULT_ANSWERS, \
    STAR_WARS_TRIVIA_PART_3_DEFAULT_ANSWERS
from tests.integration.star_wars.star_wars_tests import StarWarsTestCase


class TestConditionalDisplay(StarWarsTestCase):

    def test_conditional_display_questions_present(self):

        self.launchSurvey()

        self.start_questionnaire_and_navigate_routing()

        # We submit the form (Bothans reveals the hidden question)
        form_data = STAR_WARS_TRIVIA_PART_1_DEFAULT_ANSWERS.copy()
        form_data['death-star-plans-answer'] = 'Bothans'
        self.post(form_data)

        # There are no validation errors
        self.assertInUrl(star_wars_test_urls.STAR_WARS_TRIVIA_PART_2)

        # Check we are on the next page
        self.assertInBody('The force is strong with you, young Jedi')
        self.assertInBody('What else did the Bothan spies steal for the Rebel Alliance?')

        # Our answers
        form_data = STAR_WARS_TRIVIA_PART_2_DEFAULT_ANSWERS.copy()
        form_data.update({
            'rebel-alliance-answer': 'Shield generator codes',
            'star-wars-prequel-answer': 'Awesome, I love them all'
        })

        self.post(form_data)

        self.assertInBody('What is the name of Jar Jar Binks')

        self.post(STAR_WARS_TRIVIA_PART_3_DEFAULT_ANSWERS)

        # There are no validation errors
        self.assertRegexUrl(star_wars_test_urls.STAR_WARS_SUMMARY_REGEX)

        # We are on the summary page
        self.assertInBody('>Star Wars</')
        self.assertInBody('>Check your answers and submit<')
        self.assertInBody('What is the name of Jar Jar Binks')

    def test_conditional_display_questions_non_present(self):

        self.launchSurvey()

        self.start_questionnaire_and_navigate_routing()

        # We submit the form
        self.post(STAR_WARS_TRIVIA_PART_1_DEFAULT_ANSWERS)

        # There are no validation errors
        self.assertInUrl(star_wars_test_urls.STAR_WARS_TRIVIA_PART_2)

        # Check we are on the next page
        self.assertNotInBody('The force is strong with you, young Jedi')
        self.assertNotInBody('What else did the Bothan spies steal for the Rebel Alliance?')

        # Our answers
        form_data = STAR_WARS_TRIVIA_PART_2_DEFAULT_ANSWERS.copy()
        form_data.update({
            # this answer means the jar jar binks question doesn't appear
            'star-wars-prequel-answer': "I like to pretend they didn't happen"
        })

        self.post(form_data)

        self.assertNotInBody('What is the name of Jar Jar Binks')

        # final answers
        self.post({'favourite-film-answer': '5'})

        # There are no validation errors
        self.assertRegexUrl(star_wars_test_urls.STAR_WARS_SUMMARY_REGEX)

        # We are on the review answers page
        self.assertInBody('>Star Wars</')
        self.assertInBody('>Check your answers and submit<')
        self.assertNotInBody('What is the name of Jar Jar Binks')
