from tests.integration.create_token import create_token
from tests.integration.downstream.downstream_test_case import DownstreamTestCase
from tests.integration.star_wars import star_wars_test_urls, BLOCK_2_DEFAULT_ANSWERS
from tests.integration.star_wars.star_wars_tests import StarWarsTestCase


class TestDownstreamDataTyping(DownstreamTestCase, StarWarsTestCase):
    def setUp(self):
        super().setUp()
        self.token = create_token('star_wars', '0')

    def test_star_wars_kitchen_sink(self):
        self.login()

        first_page = self.start_questionnaire_and_navigate_routing()

        # Form submission with no errors
        resp = self.submit_page(first_page, BLOCK_2_DEFAULT_ANSWERS)
        self.assertNotEqual(resp.location, first_page)

        # Second page
        second_page = resp.location
        resp = self.navigate_to_page(second_page)
        content = resp.get_data(True)

        # Pipe Test for section title
        self.assertRegex(content, 'On 2 June 1983 how many were employed?')

        # Textarea question
        self.assertRegex(content, 'Why doesn\'t Chewbacca receive a medal at the end of A New Hope?')
        self.assertRegex(content, '215015b1-f87c-4740-9fd4-f01f707ef558')

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
        third_page = resp.location
        resp = self.navigate_to_page(third_page)
        content = resp.get_data(True)

        self.assertRegex(content, "Finally, which  is your favourite film?")

        form_data = {
            # final answers
            "fcf636ff-7b3d-47b6-aaff-9a4b00aa888b": "Naboo",
            "4a085fe5-6830-4ef6-96e6-2ea2b3caf0c1": "5",
            # User Action
            "action[save_continue]": "Save &amp; Continue"
        }

        resp = self.submit_page(third_page, form_data)

        # There are no validation errors
        self.assertRegex(resp.location, star_wars_test_urls.STAR_WARS_SUMMARY_REGEX)

        summary_url = resp.location

        self.navigate_to_page(summary_url)

        self.complete_survey('star_wars')

        # Get the message that would be sent downstream
        message = DownstreamTestCase.get_submitter().get_message()
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
            self.assertEqual(expected[key], value)
            if isinstance(expected[key], list):
                for item in expected[key]:
                    self.assertIn(item, value)
