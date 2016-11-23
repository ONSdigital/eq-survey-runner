from werkzeug.datastructures import MultiDict

from tests.integration.create_token import create_token
from tests.integration.downstream.downstream_test_case import DownstreamTestCase
from tests.integration.star_wars import star_wars_test_urls
from tests.integration.star_wars.star_wars_tests import StarWarsTestCase


class TestDownstreamDataTyping(DownstreamTestCase, StarWarsTestCase):
    def setUp(self):
        super().setUp()
        self.token = create_token('star_wars', '0')

    def test_star_wars_kitchen_sink(self):
        self.login_and_check_introduction_text()

        first_page = self.start_questionnaire_and_navigate_routing()

        # Our answers
        form_data = MultiDict()
        # Start Date
        form_data.add("6cf5c72a-c1bf-4d0c-af6c-d0f07bc5b65b", "234")
        form_data.add("92e49d93-cbdc-4bcb-adb2-0e0af6c9a07c", "00000000000000000000000000000000040")        # 40
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

        # Form submission with no errors
        resp = self.submit_page(first_page, form_data)
        self.assertNotEquals(resp.headers['Location'], first_page)

        # Second page
        second_page = resp.headers['Location']
        resp = self.navigate_to_page(second_page)
        content = resp.get_data(True)

        # Pipe Test for section title
        self.assertRegexpMatches(content, 'On 2 June 1983 how many were employed?')

        # Textarea question
        self.assertRegexpMatches(content, 'Why doesn&#39;t Chewbacca receive a medal at the end of A New Hope?')
        self.assertRegexpMatches(content, '215015b1-f87c-4740-9fd4-f01f707ef558')

        # Our answers
        form_data = {
            # People in household
            "215015b1-f87c-4740-9fd4-f01f707ef558": "Wookiees don’t place value in material rewards and refused the medal initially",  # NOQA
            "7587qe9b-f24e-4dc0-ac94-66118b896c10": "Yes",
            # User Action
            "action[save_continue]": "Save &amp; Continue"
        }

        resp = self.submit_page(second_page, form_data)

        # third page
        third_page = resp.headers['Location']
        resp = self.navigate_to_page(third_page)
        content = resp.get_data(True)

        self.assertRegexpMatches(content, "Finally, which  is your favourite film?")

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

        self.navigate_to_page(summary_url)

        self.complete_survey(star_wars_test_urls.STAR_WARS_SUBMIT, 'star_wars')

        # Get the message that would be sent downstream
        message = DownstreamTestCase._submitter._message
        self.assertIn('data', message.keys())

        data = message['data']

        expected = {
            '20': 'Light Side',
            '23': 'Yes',
            '22': 'Millennium Falcon',
            '1': '234',
            '2': '40',
            '3': '1370',
            '4': 'Elephant',
            '5': 'Luke, I am your father',
            '6': ['Luke Skywalker', 'Yoda', 'Qui-Gon Jinn'],
            '81': '28/05/1983',
            '82': '29/05/1983',
            '10': "Wookiees don’t place value in material rewards and refused the medal initially",
            '43': 'Yes'
        }

        for key, value in expected.items():
            self.assertIn(key, data.keys())
            self.assertTrue(type(expected[key]) == type(data[key]))  # NOQA
            self.assertEquals(expected[key], data[key])
            if isinstance(expected[key], list):
                for item in expected[key]:
                    self.assertIn(item, data[key])
