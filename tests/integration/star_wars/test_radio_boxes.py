from tests.integration.star_wars.star_wars_tests import StarWarsTestCase
from tests.integration.star_wars import star_wars_test_urls


class TestEmptyRadioBoxes(StarWarsTestCase):

    def test_radio_boxes_mandatory_empty(self):

        self.login_and_check_introduction_text()

        first_page = self.start_questionnaire_and_navigate_routing()

        # We fill in the survey without a mandatory radio box
        form_data = {
            # Start Date
            "6cf5c72a-c1bf-4d0c-af6c-d0f07bc5b65b": "234",
            "92e49d93-cbdc-4bcb-adb2-0e0af6c9a07c": "40",
            "pre49d93-cbdc-4bcb-adb2-0e0af6c9a07c": "1370",

            "a5dc09e8-36f2-4bf4-97be-c9e6ca8cbe0d": "",     # This is mandatory
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
            "7587qe9b-f24e-4dc0-ac94-66118b896c10": "Yes",
            # User Action
            "action[save_continue]": "Save &amp; Continue"
        }

        # We submit the form
        resp = self.submit_page(first_page, form_data)

        # We stay on the current page
        content = resp.get_data(True)
        self.assertRegexpMatches(content, 'Star Wars Quiz')
        self.assertRegexpMatches(content, 'May the force be with you young EQ developer')
        self.assertRegexpMatches(content, 'This page has 1 errors')
        self.assertRegexpMatches(content, 'This field is mandatory.')

        # We correct the error
        form_data = {
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
        summary_url = resp.headers['Location']
        resp = self.navigate_to_page(summary_url)

        # Check we are on the next page
        content = resp.get_data(True)
        self.assertRegexpMatches(content, 'Why doesn&#39;t Chewbacca receive a medal at the end of A New Hope?')
