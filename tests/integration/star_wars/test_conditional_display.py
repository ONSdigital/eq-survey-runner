from tests.integration.star_wars.star_wars_tests import StarWarsTestCase
from tests.integration.star_wars import star_wars_test_urls


class TestConditionalDisplay(StarWarsTestCase):

    def test_conditional_display_questions_present(self):

        self.login_and_check_introduction_text()

        first_page = self.start_questionnaire_and_navigate_routing()

        # We correct the error
        form_data = {
            # conditional display question - submit the correct answer
            "cccfe681-9969-4175-8ac3-98184ab58423": "Bothans",

            # Start Date
            "6cf5c72a-c1bf-4d0c-af6c-d0f07bc5b65b": "234",
            "92e49d93-cbdc-4bcb-adb2-0e0af6c9a07c": "40",
            "pre49d93-cbdc-4bcb-adb2-0e0af6c9a07c": "1370",

            "a5dc09e8-36f2-4bf4-97be-c9e6ca8cbe0d": "Elephant",
            "7587eb9b-f24e-4dc0-ac94-66118b896c10": "Luke, I am your father",
            "9587eb9b-f24e-4dc0-ac94-66117b896c10": "[Luke Skywalker, Yoda, Qui-Gon Jinn]",


            "6fd644b0-798e-4a58-a393-a438b32fe637-day": "28",
            "6fd644b0-798e-4a58-a393-a438b32fe637-month": "05",
            "6fd644b0-798e-4a58-a393-a438b32fe637-year": "1983",
            # End Date
            "06a6a4b7-6ce4-4687-879d-3443cd8e2ff0-day": "29",
            "06a6a4b7-6ce4-4687-879d-3443cd8e2ff0-month": "05",
            "06a6a4b7-6ce4-4687-879d-3443cd8e2ff0-year": "1983",
            # Total Turnover
            "215015b1-f87c-4740-9fd4-f01f707ef558": "Wookiees don’t place value in material rewards and refused the medal initially",
            # User Action
            "action[save_continue]": "Save &amp; Continue"
        }

        # We submit the form
        resp = self.submit_page(first_page, form_data)

        # There are no validation errors
        self.assertRegexpMatches(resp.headers['Location'], star_wars_test_urls.STAR_WARS_QUIZ_2_REGEX)

        second_page = resp.headers['Location']
        resp = self.navigate_to_page(second_page)

        # Check we are on the next page
        content = resp.get_data(True)
        self.assertRegexpMatches(content, 'The force is strong with you, young Jedi')
        self.assertRegexpMatches(content, 'What else did the Bothan spies steal for the Rebel Alliance?')

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

        third_page = resp.headers['Location']
        resp = self.navigate_to_page(third_page)

        content = resp.get_data(True)
        self.assertRegexpMatches(content, 'What is the name of Jar Jar Binks')

        form_data = {
          # final answers
          "fcf636ff-7b3d-47b6-aaff-9a4b00aa888b": "Naboo",
          "4a085fe5-6830-4ef6-96e6-2ea2b3caf0c1": "5",
          # User Action
          "action[save_continue]": "Save &amp; Continue"
        }

        resp = self.submit_page(third_page, form_data)

        # There are no validation errors
        self.assertRegexpMatches(resp.headers['Location'], star_wars_test_urls.STAR_WARS_SUMMARY_REGEX)

        summary_url = resp.headers['Location']

        resp = self.navigate_to_page(summary_url)

        # We are on the review answers page
        content = resp.get_data(True)
        self.assertRegexpMatches(content, '<title>Summary</title>')
        self.assertRegexpMatches(content, '>Star Wars</')
        self.assertRegexpMatches(content, '>Your responses<')
        self.assertRegexpMatches(content, 'What is the name of Jar Jar Binks')

    def test_conditional_display_questions_non_present(self):

        self.login_and_check_introduction_text()

        first_page = self.start_questionnaire_and_navigate_routing()

        # We correct the error
        form_data = {
            # conditional display question - submit an incorrect answer
            "cccfe681-9969-4175-8ac3-98184ab58423": "Ewoks",

            # Start Date
            "6cf5c72a-c1bf-4d0c-af6c-d0f07bc5b65b": "234",
            "92e49d93-cbdc-4bcb-adb2-0e0af6c9a07c": "40",
            "pre49d93-cbdc-4bcb-adb2-0e0af6c9a07c": "1370",

            "a5dc09e8-36f2-4bf4-97be-c9e6ca8cbe0d": "Elephant",
            "7587eb9b-f24e-4dc0-ac94-66118b896c10": "Luke, I am your father",
            "9587eb9b-f24e-4dc0-ac94-66117b896c10": "[Luke Skywalker, Yoda, Qui-Gon Jinn]",


            "6fd644b0-798e-4a58-a393-a438b32fe637-day": "28",
            "6fd644b0-798e-4a58-a393-a438b32fe637-month": "05",
            "6fd644b0-798e-4a58-a393-a438b32fe637-year": "1983",
            # End Date
            "06a6a4b7-6ce4-4687-879d-3443cd8e2ff0-day": "29",
            "06a6a4b7-6ce4-4687-879d-3443cd8e2ff0-month": "05",
            "06a6a4b7-6ce4-4687-879d-3443cd8e2ff0-year": "1983",
            # Total Turnover
            "215015b1-f87c-4740-9fd4-f01f707ef558": "Wookiees don’t place value in material rewards and refused the medal initially",
            # User Action
            "action[save_continue]": "Save &amp; Continue"
        }

        # We submit the form
        resp = self.submit_page(first_page, form_data)

        # There are no validation errors
        self.assertRegexpMatches(resp.headers['Location'], star_wars_test_urls.STAR_WARS_QUIZ_2_REGEX)

        second_page = resp.headers['Location']
        resp = self.navigate_to_page(second_page)

        # Check we are on the next page
        content = resp.get_data(True)
        self.assertNotRegex(content, 'The force is strong with you, young Jedi')
        self.assertNotRegex(content, 'What else did the Bothan spies steal for the Rebel Alliance?')

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

        third_page = resp.headers['Location']
        resp = self.navigate_to_page(third_page)

        content = resp.get_data(True)
        self.assertNotRegex(content, 'What is the name of Jar Jar Binks')

        form_data = {
          # final answers
          "4a085fe5-6830-4ef6-96e6-2ea2b3caf0c1": "5",
          # User Action
          "action[save_continue]": "Save &amp; Continue"
        }

        resp = self.submit_page(third_page, form_data)

        # There are no validation errors
        self.assertRegexpMatches(resp.headers['Location'], star_wars_test_urls.STAR_WARS_SUMMARY_REGEX)

        summary_url = resp.headers['Location']

        resp = self.navigate_to_page(summary_url)

        # We are on the review answers page
        content = resp.get_data(True)
        self.assertRegexpMatches(content, '<title>Summary</title>')
        self.assertRegexpMatches(content, '>Star Wars</')
        self.assertRegexpMatches(content, '>Your responses<')
        self.assertNotRegex(content, 'What is the name of Jar Jar Binks')
