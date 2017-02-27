from tests.integration.navigation import navigate_to_page
from tests.integration.star_wars import star_wars_test_urls, BLOCK_2_DEFAULT_ANSWERS, BLOCK_8_DEFAULT_ANSWERS
from tests.integration.star_wars.star_wars_tests import StarWarsTestCase


class TestConditionalDisplay(StarWarsTestCase):

    def test_conditional_display_questions_present(self):

        self.login()

        first_page = self.start_questionnaire_and_navigate_routing()

        form_data = {
            "death-star-plans-answer": "Bothans",
            "chewies-age-answer": "234",
            "death-star-cost-answer": "40",
            "lightsaber-cost-answer": "1370",

            "tie-fighter-sound-answer": "Elephant",
            "darth-vader-quotes-answer": "Luke, I am your father",

            "green-lightsaber-answer": ["Luke Skywalker", "Yoda", "Qui-Gon Jinn"],

            "empire-strikes-back-from-answer-day": "28",
            "empire-strikes-back-from-answer-month": "5",
            "empire-strikes-back-from-answer-year": "1983",

            "empire-strikes-back-to-answer-day": "29",
            "empire-strikes-back-to-answer-month": "5",
            "empire-strikes-back-to-answer-year": "1983",

            "action[save_continue]": "Save &amp; Continue"
        }

        # We submit the form
        resp = self.submit_page(first_page, form_data)

        # There are no validation errors
        self.assertIn(star_wars_test_urls.STAR_WARS_QUIZ_2, resp.location)

        second_page = resp.location
        resp = navigate_to_page(self.client, second_page)

        # Check we are on the next page
        content = resp.get_data(True)
        self.assertIn('The force is strong with you, young Jedi', content)
        self.assertIn('What else did the Bothan spies steal for the Rebel Alliance?', content)

        # Our answers
        form_data = {
            "rebel-alliance-answer": "Shield generator codes",
            "chewbacca-medal-answer": "Wookiees don’t place value in material rewards and refused the medal initially",  # NOQA
            "confirm-chewbacca-age-answer": "Yes",
            "star-wars-prequel-answer": "Awesome, I love them all",
            # User Action
            "action[save_continue]": "Save &amp; Continue"
        }

        resp = self.submit_page(second_page, form_data)

        third_page = resp.location
        resp = navigate_to_page(self.client, third_page)

        content = resp.get_data(True)
        self.assertIn('What is the name of Jar Jar Binks', content)

        resp = self.submit_page(third_page, BLOCK_8_DEFAULT_ANSWERS)

        # There are no validation errors
        self.assertRegex(resp.location, star_wars_test_urls.STAR_WARS_SUMMARY_REGEX)

        summary_url = resp.location

        resp = navigate_to_page(self.client, summary_url)

        # We are on the review answers page
        content = resp.get_data(True)
        self.assertIn('<title>Summary</title>', content)
        self.assertIn('>Star Wars</', content)
        self.assertIn('>Your responses<', content)
        self.assertIn('What is the name of Jar Jar Binks', content)

    def test_conditional_display_questions_non_present(self):

        self.login()

        first_page = self.start_questionnaire_and_navigate_routing()

        # We submit the form
        resp = self.submit_page(first_page, BLOCK_2_DEFAULT_ANSWERS)

        # There are no validation errors
        self.assertIn(star_wars_test_urls.STAR_WARS_QUIZ_2, resp.location)

        second_page = resp.location
        resp = navigate_to_page(self.client, second_page)

        # Check we are on the next page
        content = resp.get_data(True)
        self.assertNotIn('The force is strong with you, young Jedi', content)
        self.assertNotIn('What else did the Bothan spies steal for the Rebel Alliance?', content)

        # Our answers
        form_data = {
            "chewbacca-medal-answer": "Wookiees don’t place value in material rewards and refused the medal initially",  # NOQA
            "confirm-chewbacca-age-answer": "Yes",
            # this answer means the jar jar binks question doesn't appear
            "star-wars-prequel-answer": "I like to pretend they didn't happen",
            # User Action
            "action[save_continue]": "Save &amp; Continue"
        }

        resp = self.submit_page(second_page, form_data)

        third_page = resp.location
        resp = navigate_to_page(self.client, third_page)

        content = resp.get_data(True)
        self.assertNotIn('What is the name of Jar Jar Binks', content)

        form_data = {
            # final answers
            "favourite-film-answer": "5",
            # User Action
            "action[save_continue]": "Save &amp; Continue"
        }

        resp = self.submit_page(third_page, form_data)

        # There are no validation errors
        self.assertRegex(resp.location, star_wars_test_urls.STAR_WARS_SUMMARY_REGEX)

        summary_url = resp.location

        resp = navigate_to_page(self.client, summary_url)

        # We are on the review answers page
        content = resp.get_data(True)
        self.assertIn('<title>Summary</title>', content)
        self.assertIn('>Star Wars</', content)
        self.assertIn('>Your responses<', content)
        self.assertNotIn('What is the name of Jar Jar Binks', content)
