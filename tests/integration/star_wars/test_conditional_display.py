from werkzeug.datastructures import MultiDict

from tests.integration.star_wars import star_wars_test_urls, BLOCK_2_DEFAULT_ANSWERS, BLOCK_8_DEFAULT_ANSWERS
from tests.integration.star_wars.star_wars_tests import StarWarsTestCase


class TestConditionalDisplay(StarWarsTestCase):

    def test_conditional_display_questions_present(self):

        self.login_and_check_introduction_text()

        first_page = self.start_questionnaire_and_navigate_routing()

        form_data = MultiDict()
        form_data.add("cccfe681-9969-4175-8ac3-98184ab58423", "Bothans")
        form_data.add("6cf5c72a-c1bf-4d0c-af6c-d0f07bc5b65b", "234")
        form_data.add("92e49d93-cbdc-4bcb-adb2-0e0af6c9a07c", "40")
        form_data.add("pre49d93-cbdc-4bcb-adb2-0e0af6c9a07c", "1370")

        form_data.add("a5dc09e8-36f2-4bf4-97be-c9e6ca8cbe0d", "Elephant")
        form_data.add("7587eb9b-f24e-4dc0-ac94-66118b896c10", "Luke, I am your father")

        form_data.add("9587eb9b-f24e-4dc0-ac94-66117b896c10", 'Luke Skywalker')
        form_data.add("9587eb9b-f24e-4dc0-ac94-66117b896c10", 'Yoda')
        form_data.add("9587eb9b-f24e-4dc0-ac94-66117b896c10", 'Qui-Gon Jinn')

        form_data.add("6fd644b0-798e-4a58-a393-a438b32fe637-day", "28")
        form_data.add("6fd644b0-798e-4a58-a393-a438b32fe637-month", "05")
        form_data.add("6fd644b0-798e-4a58-a393-a438b32fe637-year", "1983")

        form_data.add("06a6a4b7-6ce4-4687-879d-3443cd8e2ff0-day", "29")
        form_data.add("06a6a4b7-6ce4-4687-879d-3443cd8e2ff0-month", "05")
        form_data.add("06a6a4b7-6ce4-4687-879d-3443cd8e2ff0-year", "1983")

        form_data.add("action[save_continue]", "Save &amp; Continue")

        # We submit the form
        resp = self.submit_page(first_page, form_data)

        # There are no validation errors
        self.assertIn(star_wars_test_urls.STAR_WARS_QUIZ_2, resp.location)

        second_page = resp.location
        resp = self.navigate_to_page(second_page)

        # Check we are on the next page
        content = resp.get_data(True)
        self.assertIn('The force is strong with you, young Jedi', content)
        self.assertIn('What else did the Bothan spies steal for the Rebel Alliance?', content)

        # Our answers
        form_data = {
            "c8d9d66e-6c0a-439e-8ef9-e0d7038be009": "Shield generator codes",
            "215015b1-f87c-4740-9fd4-f01f707ef558": "Wookiees don’t place value in material rewards and refused the medal initially",  # NOQA
            "7587qe9b-f24e-4dc0-ac94-66118b896c10": "Yes",
            "77e20f0e-cabb-4eac-8cb0-ac6e66f0e95f": "Awesome, I love them all",
            # User Action
            "action[save_continue]": "Save &amp; Continue"
        }

        resp = self.submit_page(second_page, form_data)

        third_page = resp.location
        resp = self.navigate_to_page(third_page)

        content = resp.get_data(True)
        self.assertIn('What is the name of Jar Jar Binks', content)

        resp = self.submit_page(third_page, BLOCK_8_DEFAULT_ANSWERS)

        # There are no validation errors
        self.assertRegex(resp.location, star_wars_test_urls.STAR_WARS_SUMMARY_REGEX)

        summary_url = resp.location

        resp = self.navigate_to_page(summary_url)

        # We are on the review answers page
        content = resp.get_data(True)
        self.assertIn('<title>Summary</title>', content)
        self.assertIn('>Star Wars</', content)
        self.assertIn('>Your responses<', content)
        self.assertIn('What is the name of Jar Jar Binks', content)

    def test_conditional_display_questions_non_present(self):

        self.login_and_check_introduction_text()

        first_page = self.start_questionnaire_and_navigate_routing()

        # We submit the form
        resp = self.submit_page(first_page, BLOCK_2_DEFAULT_ANSWERS)

        # There are no validation errors
        self.assertIn(star_wars_test_urls.STAR_WARS_QUIZ_2, resp.location)

        second_page = resp.location
        resp = self.navigate_to_page(second_page)

        # Check we are on the next page
        content = resp.get_data(True)
        self.assertNotIn('The force is strong with you, young Jedi', content)
        self.assertNotIn('What else did the Bothan spies steal for the Rebel Alliance?', content)

        # Our answers
        form_data = {
            "215015b1-f87c-4740-9fd4-f01f707ef558": "Wookiees don’t place value in material rewards and refused the medal initially",  # NOQA
            "7587qe9b-f24e-4dc0-ac94-66118b896c10": "Yes",
            # this answer means the jar jar binks question doesn't appear
            "77e20f0e-cabb-4eac-8cb0-ac6e66f0e95f": "I like to pretend they didn't happen",
            # User Action
            "action[save_continue]": "Save &amp; Continue"
        }

        resp = self.submit_page(second_page, form_data)

        third_page = resp.location
        resp = self.navigate_to_page(third_page)

        content = resp.get_data(True)
        self.assertNotIn('What is the name of Jar Jar Binks', content)

        form_data = {
            # final answers
            "4a085fe5-6830-4ef6-96e6-2ea2b3caf0c1": "5",
            # User Action
            "action[save_continue]": "Save &amp; Continue"
        }

        resp = self.submit_page(third_page, form_data)

        # There are no validation errors
        self.assertRegex(resp.location, star_wars_test_urls.STAR_WARS_SUMMARY_REGEX)

        summary_url = resp.location

        resp = self.navigate_to_page(summary_url)

        # We are on the review answers page
        content = resp.get_data(True)
        self.assertIn('<title>Summary</title>', content)
        self.assertIn('>Star Wars</', content)
        self.assertIn('>Your responses<', content)
        self.assertNotIn('What is the name of Jar Jar Binks', content)
