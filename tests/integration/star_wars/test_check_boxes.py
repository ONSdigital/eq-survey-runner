from tests.integration.star_wars.star_wars_tests import StarWarsTestCase
from werkzeug.datastructures import MultiDict
from tests.integration.star_wars import star_wars_test_urls


class TestEmptyCheckBoxes(StarWarsTestCase):

    def test_check_boxes_mandatory_empty(self):
        self.login_and_check_introduction_text()

        first_page = self.start_questionnaire_and_navigate_routing()

        # We fill in the survey without a mandatory check box
        form_data = MultiDict()
        # Start Date
        form_data.add("6cf5c72a-c1bf-4d0c-af6c-d0f07bc5b65b", "234")
        form_data.add("92e49d93-cbdc-4bcb-adb2-0e0af6c9a07c", "40")
        form_data.add("pre49d93-cbdc-4bcb-adb2-0e0af6c9a07c", "1370")

        form_data.add("a5dc09e8-36f2-4bf4-97be-c9e6ca8cbe0d", "Elephant")
        form_data.add("7587eb9b-f24e-4dc0-ac94-66118b896c10", "Luke, I am your father")

        # Skip these three checkboxes
        # form_data.add("9587eb9b-f24e-4dc0-ac94-66117b896c10", 'Luke Skywalker')
        # form_data.add("9587eb9b-f24e-4dc0-ac94-66117b896c10", 'Yoda')
        # form_data.add("9587eb9b-f24e-4dc0-ac94-66117b896c10", 'Qui-Gon Jinn')

        form_data.add("6fd644b0-798e-4a58-a393-a438b32fe637-day", "28")
        form_data.add("6fd644b0-798e-4a58-a393-a438b32fe637-month", "05")
        form_data.add("6fd644b0-798e-4a58-a393-a438b32fe637-year", "1983")
        # End Date
        form_data.add("06a6a4b7-6ce4-4687-879d-3443cd8e2ff0-day", "29")
        form_data.add("06a6a4b7-6ce4-4687-879d-3443cd8e2ff0-month", "05")
        form_data.add("06a6a4b7-6ce4-4687-879d-3443cd8e2ff0-year", "1983")
        # Total Turnover
        form_data.add("215015b1-f87c-4740-9fd4-f01f707ef558", "Wookiees don’t place value in material rewards and refused the medal initially")
        form_data.add("7587qe9b-f24e-4dc0-ac94-66118b896c10", "Yes")
        # User Action
        form_data.add("action[save_continue]", "Save &amp; Continue")

        # We submit the form
        resp = self.submit_page(first_page, form_data)

        # We stay on the current page
        content = resp.get_data(True)
        self.assertRegexpMatches(content, 'Star Wars Quiz')
        self.assertRegexpMatches(content, 'May the force be with you young EQ developer')
        self.assertRegexpMatches(content, 'This page has 1 errors')
        self.assertRegexpMatches(content, 'This field is mandatory.')

        # We correct the error
        form_data = MultiDict()
        # Start Date
        form_data.add("6cf5c72a-c1bf-4d0c-af6c-d0f07bc5b65b", "234")
        form_data.add("92e49d93-cbdc-4bcb-adb2-0e0af6c9a07c", "40")
        form_data.add("pre49d93-cbdc-4bcb-adb2-0e0af6c9a07c", "1370")

        form_data.add("a5dc09e8-36f2-4bf4-97be-c9e6ca8cbe0d", "Elephant")
        form_data.add("7587eb9b-f24e-4dc0-ac94-66118b896c10", "Luke, I am your father")

        # Check three boxes
        form_data.add("9587eb9b-f24e-4dc0-ac94-66117b896c10", 'Luke Skywalker')
        form_data.add("9587eb9b-f24e-4dc0-ac94-66117b896c10", 'Yoda')
        form_data.add("9587eb9b-f24e-4dc0-ac94-66117b896c10", 'Qui-Gon Jinn')

        form_data.add("6fd644b0-798e-4a58-a393-a438b32fe637-day", "28")
        form_data.add("6fd644b0-798e-4a58-a393-a438b32fe637-month", "05")
        form_data.add("6fd644b0-798e-4a58-a393-a438b32fe637-year", "1983")
        # End Date
        form_data.add("06a6a4b7-6ce4-4687-879d-3443cd8e2ff0-day", "29")
        form_data.add("06a6a4b7-6ce4-4687-879d-3443cd8e2ff0-month", "05")
        form_data.add("06a6a4b7-6ce4-4687-879d-3443cd8e2ff0-year", "1983")
        # Total Turnover
        form_data.add("215015b1-f87c-4740-9fd4-f01f707ef558", "Wookiees don’t place value in material rewards and refused the medal initially")
        form_data.add("7587qe9b-f24e-4dc0-ac94-66118b896c10", "Yes")
        # User Action
        form_data.add("action[save_continue]", "Save &amp; Continue")

        # We submit the form
        resp = self.submit_page(first_page, form_data)

        # There are no validation errors

        self.assertRegexpMatches(resp.headers['Location'], star_wars_test_urls.STAR_WARS_QUIZ_2_REGEX)
        second_page = resp.headers['Location']

        self.check_second_quiz_page(second_page)
