from tests.integration.star_wars import star_wars_test_urls, BLOCK_2_DEFAULT_ANSWERS, BLOCK_8_DEFAULT_ANSWERS
from tests.integration.star_wars.star_wars_tests import StarWarsTestCase


class TestConditionalDisplay(StarWarsTestCase):

    def test_conditional_display_questions_present(self):

        self.launchSurvey()

        self.start_questionnaire_and_navigate_routing()

        form_data = {
            'death-star-plans-answer': 'Bothans',
            'chewies-age-answer': '234',
            'death-star-cost-answer': '40',
            'lightsaber-cost-answer': '1370',

            'tie-fighter-sound-answer': 'Elephant',
            'darth-vader-quotes-answer': 'Luke, I am your father',

            'green-lightsaber-answer': ['Luke Skywalker', 'Yoda', 'Qui-Gon Jinn'],

            'empire-strikes-back-from-answer-day': '28',
            'empire-strikes-back-from-answer-month': '5',
            'empire-strikes-back-from-answer-year': '1983',

            'empire-strikes-back-to-answer-day': '29',
            'empire-strikes-back-to-answer-month': '5',
            'empire-strikes-back-to-answer-year': '1983'
        }

        # We submit the form
        self.post(form_data)

        # There are no validation errors
        self.assertInUrl(star_wars_test_urls.STAR_WARS_QUIZ_2)

        # Check we are on the next page
        self.assertInPage('The force is strong with you, young Jedi')
        self.assertInPage('What else did the Bothan spies steal for the Rebel Alliance?')

        # Our answers
        form_data = {
            'rebel-alliance-answer': 'Shield generator codes',
            'chewbacca-medal-answer': 'Wookiees don’t place value in material rewards and refused the medal initially',  # NOQA
            'confirm-chewbacca-age-answer': 'Yes',
            'star-wars-prequel-answer': 'Awesome, I love them all'
        }

        self.post(form_data)

        self.assertInPage('What is the name of Jar Jar Binks')

        self.post(BLOCK_8_DEFAULT_ANSWERS)

        # There are no validation errors
        self.assertRegexUrl(star_wars_test_urls.STAR_WARS_SUMMARY_REGEX)

        # We are on the summary page
        self.assertInPage('>Star Wars</')
        self.assertInPage('>Your responses<')
        self.assertInPage('What is the name of Jar Jar Binks')

    def test_conditional_display_questions_non_present(self):

        self.launchSurvey()

        self.start_questionnaire_and_navigate_routing()

        # We submit the form
        self.post(BLOCK_2_DEFAULT_ANSWERS)

        # There are no validation errors
        self.assertInUrl(star_wars_test_urls.STAR_WARS_QUIZ_2)

        # Check we are on the next page
        self.assertNotInPage('The force is strong with you, young Jedi')
        self.assertNotInPage('What else did the Bothan spies steal for the Rebel Alliance?')

        # Our answers
        form_data = {
            'chewbacca-medal-answer': 'Wookiees don’t place value in material rewards and refused the medal initially',  # NOQA
            'confirm-chewbacca-age-answer': 'Yes',
            # this answer means the jar jar binks question doesn't appear
            'star-wars-prequel-answer': 'I like to pretend they didn\'t happen'
        }

        self.post(form_data)

        self.assertNotInPage('What is the name of Jar Jar Binks')

        # final answers
        self.post({'favourite-film-answer': '5'})

        # There are no validation errors
        self.assertRegexUrl(star_wars_test_urls.STAR_WARS_SUMMARY_REGEX)

        # We are on the review answers page
        self.assertInPage('>Star Wars</')
        self.assertInPage('>Your responses<')
        self.assertNotInPage('What is the name of Jar Jar Binks')
