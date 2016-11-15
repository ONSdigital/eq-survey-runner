from tests.integration.create_token import create_token
from tests.integration.star_wars.star_wars_tests import StarWarsTestCase
from werkzeug.datastructures import MultiDict


class TestPageErrors(StarWarsTestCase):
    def test_multi_page_errors(self):
        # Get a token

        self.login_and_check_introduction_text()

        first_page = self.start_questionnaire_and_navigate_routing()

        form_data = MultiDict({

            "6cf5c72a-c1bf-4d0c-af6c-d0f07bc5b65b": "234",
            "92e49d93-cbdc-4bcb-adb2-0e0af6c9a07c": "40",
            "pre49d93-cbdc-4bcb-adb2-0e0af6c9a07c": "1370",

            "a5dc09e8-36f2-4bf4-97be-c9e6ca8cbe0d": "Elephant",
            "7587eb9b-f24e-4dc0-ac94-66118b896c10": "Luke, I am your father",
            "9587eb9b-f24e-4dc0-ac94-66117b896c10": ['Luke Skywalker', 'Yoda', 'Qui-Gon Jinn'],

            "6fd644b0-798e-4a58-a393-a438b32fe637-day": "28",
            "6fd644b0-798e-4a58-a393-a438b32fe637-month": "05",
            "6fd644b0-798e-4a58-a393-a438b32fe637-year": "1983",

            "06a6a4b7-6ce4-4687-879d-3443cd8e2ff0-day": "29",
            "06a6a4b7-6ce4-4687-879d-3443cd8e2ff0-month": "05",
            "06a6a4b7-6ce4-4687-879d-3443cd8e2ff0-year": "1983",

            "action[save_continue]": "Save &amp; Continue"
        })

        resp = self.submit_page(first_page, form_data)

        self.assertNotEquals(resp.headers['Location'], first_page)
        # Second page
        second_page = resp.headers['Location']

        self.check_second_quiz_page(second_page)

        # Our answers
        form_data = {
            # Make this data missing
            "215015b1-f87c-4740-9fd4-f01f707ef558": "",  # Required answer
            # User Action
            "action[save_continue]": "Save &amp; Continue"
        }

        self.submit_page(second_page, form_data)

        # We fill in our answers missing one required field
        form_data = {

            "6cf5c72a-c1bf-4d0c-af6c-d0f07bc5b65b": "234",
            "92e49d93-cbdc-4bcb-adb2-0e0af6c9a07c": "40",
            "pre49d93-cbdc-4bcb-adb2-0e0af6c9a07c": "1370",

            # Miss this as well
            "a5dc09e8-36f2-4bf4-97be-c9e6ca8cbe0d": "",  # Missing required answer
            "7587eb9b-f24e-4dc0-ac94-66118b896c10": "Luke, I am your father",
            "9587eb9b-f24e-4dc0-ac94-66117b896c10": "[Luke Skywalker, Yoda, Qui-Gon Jinn]",

            "6fd644b0-798e-4a58-a393-a438b32fe637-day": "28",
            "6fd644b0-798e-4a58-a393-a438b32fe637-month": "05",
            "6fd644b0-798e-4a58-a393-a438b32fe637-year": "1983",

            "06a6a4b7-6ce4-4687-879d-3443cd8e2ff0-day": "29",
            "06a6a4b7-6ce4-4687-879d-3443cd8e2ff0-month": "05",
            "06a6a4b7-6ce4-4687-879d-3443cd8e2ff0-year": "1983",

            # User Action
            "action[save_continue]": "Save &amp; Continue"
        }

        # We submit the form
        resp = self.submit_page(first_page, form_data)

        content = resp.get_data(True)
        self.assertRegex(content, 'href="#a5dc09e8-36f2-4bf4-97be-c9e6ca8cbe0d"')
        # We DO NOT have the error from page two
        self.assertNotRegex(content, 'href="215015b1-f87c-4740-9fd4-f01f707ef558"')

    def test_skip_question_errors(self):
        # Given on the page with skip question with skip condition
        self.token = create_token('skip_condition', 'test')
        self.client.get('/session?token=' + self.token.decode(), follow_redirects=True)
        post_data = {'action[start_questionnaire]': 'Start Questionnaire'}
        self.client.post('/questionnaire/test/skip_condition/201604/789/introduction', data=post_data, follow_redirects=True)
        post_data = {'food-answer': 'Bacon', 'action[save_continue]': 'Save &amp; Continue'}
        self.client.post('/questionnaire/test/skip_condition/201604/789/breakfast/0/food-block', data=post_data, follow_redirects=True)

        # When submit no answers which is invalid
        post_data = {'action[save_continue]': 'Save &amp; Continue'}
        resp = self.client.post('/questionnaire/test/skip_condition/789/breakfast/0/drink-block', data=post_data)

        # Then errors exists on page
        self.assertEqual(resp.status_code, 200)
        self.assertRegex(resp.get_data(True), 'This page has 1 errors')
