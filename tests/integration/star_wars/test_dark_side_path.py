from tests.integration.create_token import create_token
from tests.integration.integration_test_case import IntegrationTestCase


class TestDarkSidePath(IntegrationTestCase):

    def test_dark_side_path(self):

        # Get a token
        token = create_token('star_wars', '0')
        resp = self.client.get('/session?token=' + token.decode(), follow_redirects=True)
        self.assertEquals(resp.status_code, 200)

        # Go to questionnaire
        post_data = {
            'action[start_questionnaire]': 'Start Questionnaire'
        }
        resp = self.client.post('/questionnaire/0/789/introduction', data=post_data, follow_redirects=False)
        self.assertEquals(resp.status_code, 302)

        first_page = resp.headers['Location']

        resp = self.client.get(first_page, follow_redirects=False)
        self.assertEquals(resp.status_code, 200)

        '''
        Testing
               Integer     - To large
                           - Not Integer
               Currency    - Not Integer
               Radio boxes - Mandatory
               Checkboxes  - Mandatory
               Date        - Invalid (empty)
                           - Invalid (Bad date)
        '''

        form_data = {

            "6cf5c72a-c1bf-4d0c-af6c-d0f07bc5b65b": "555555555555555555",
            "92e49d93-cbdc-4bcb-adb2-0e0af6c9a07c": "text",
            "pre49d93-cbdc-4bcb-adb2-0e0af6c9a07c": "###",

            "a5dc09e8-36f2-4bf4-97be-c9e6ca8cbe0d": "",
            "7587eb9b-f24e-4dc0-ac94-66118b896c10" : "",
            "9587eb9b-f24e-4dc0-ac94-66117b896c10":"",

            "6fd644b0-798e-4a58-a393-a438b32fe637-day": "",
            "6fd644b0-798e-4a58-a393-a438b32fe637-month": "",
            "6fd644b0-798e-4a58-a393-a438b32fe637-year": "",

            "06a6a4b7-6ce4-4687-879d-3443cd8e2ff0-day": "30",
            "06a6a4b7-6ce4-4687-879d-3443cd8e2ff0-month": "2",
            "06a6a4b7-6ce4-4687-879d-3443cd8e2ff0-year": "2016",

            "action[save_continue]": "Save &amp; Continue"
        }

        # Submit the form
        resp = self.client.post(first_page, data=form_data, follow_redirects=False)
        self.assertEquals(resp.status_code, 302)

        # Check we stay on the page
        self.assertEquals(resp.headers['Location'], first_page)

        resp = self.client.get(first_page, follow_redirects=False)
        self.assertEquals(resp.status_code, 200)

        # Test error messages
        content = resp.get_data(True)
        self.assertRegexpMatches(content, '1\) No one lives that long, not even Yoda')
        self.assertRegexpMatches(content, '2\) Please only enter whole numbers into the field.')
        self.assertRegexpMatches(content, '3\) Please only enter whole numbers into the field.')
        self.assertRegexpMatches(content, '4\) This field is mandatory.')
        self.assertRegexpMatches(content, '5\) This field is mandatory.')
        self.assertRegexpMatches(content, '6\) The date entered is not valid')
        self.assertRegexpMatches(content, '7\) The date entered is not valid')

        '''
        Testing
               Integer  - Mandatory
                        - Negative
               Currency - To large
               Date     - From and to the same
        '''

        form_data = {

            "6cf5c72a-c1bf-4d0c-af6c-d0f07bc5b65b": "",
            "92e49d93-cbdc-4bcb-adb2-0e0af6c9a07c": "9999999999999",
            "pre49d93-cbdc-4bcb-adb2-0e0af6c9a07c": "-5",

            "a5dc09e8-36f2-4bf4-97be-c9e6ca8cbe0d": "Elephant",
            "9587eb9b-f24e-4dc0-ac94-66117b896c10":"[Luke Skywalker, Yoda, Qui-Gon Jinn]",

            "6fd644b0-798e-4a58-a393-a438b32fe637-day": "1",
            "6fd644b0-798e-4a58-a393-a438b32fe637-month": "1",
            "6fd644b0-798e-4a58-a393-a438b32fe637-year": "2016",

            "06a6a4b7-6ce4-4687-879d-3443cd8e2ff0-day": "1",
            "06a6a4b7-6ce4-4687-879d-3443cd8e2ff0-month": "1",
            "06a6a4b7-6ce4-4687-879d-3443cd8e2ff0-year": "2016",

            "action[save_continue]": "Save &amp; Continue"
        }

        # Submit the form
        resp = self.client.post(first_page, data=form_data, follow_redirects=False)
        self.assertEquals(resp.status_code, 302)

        # Check we stay on the page
        self.assertEquals(resp.headers['Location'], first_page)

        resp = self.client.get(first_page, follow_redirects=False)
        self.assertEquals(resp.status_code, 200)

        # Test error messages
        content = resp.get_data(True)
        self.assertRegexpMatches(content, '1\) This field is mandatory')
        self.assertRegexpMatches(content, '2\) How much, idiot you must be')
        self.assertRegexpMatches(content, '3\) How can it be negative?')
        self.assertRegexpMatches(content, '4\) The &#39;to&#39; date must be different to the &#39;from&#39; date.')

        '''
         Testing
                Currency  - Negative
                Date      - To before From
        '''

        form_data = {

            "6cf5c72a-c1bf-4d0c-af6c-d0f07bc5b65b": "430",
            "92e49d93-cbdc-4bcb-adb2-0e0af6c9a07c": "-10",
            "pre49d93-cbdc-4bcb-adb2-0e0af6c9a07c": "",

            "a5dc09e8-36f2-4bf4-97be-c9e6ca8cbe0d": "Elephant",
            "9587eb9b-f24e-4dc0-ac94-66117b896c10":"[Luke Skywalker, Yoda, Qui-Gon Jinn]",

            "6fd644b0-798e-4a58-a393-a438b32fe637-day": "1",
            "6fd644b0-798e-4a58-a393-a438b32fe637-month": "1",
            "6fd644b0-798e-4a58-a393-a438b32fe637-year": "2016",

            "06a6a4b7-6ce4-4687-879d-3443cd8e2ff0-day": "1",
            "06a6a4b7-6ce4-4687-879d-3443cd8e2ff0-month": "1",
            "06a6a4b7-6ce4-4687-879d-3443cd8e2ff0-year": "2015",

            "action[save_continue]": "Save &amp; Continue"
        }

        # Submit the form
        resp = self.client.post(first_page, data=form_data, follow_redirects=False)
        self.assertEquals(resp.status_code, 302)

        # Check we stay on the page
        self.assertEquals(resp.headers['Location'], first_page)

        resp = self.client.get(first_page, follow_redirects=False)
        self.assertEquals(resp.status_code, 200)

        # Test error messages
        content = resp.get_data(True)
        self.assertRegexpMatches(content, '1\) How can it be negative?')
        self.assertRegexpMatches(content, '2\) The &#39;to&#39; date cannot be before the &#39;from&#39; date.')

        # Testing Currecy  - Mandatory

        form_data = {

            "6cf5c72a-c1bf-4d0c-af6c-d0f07bc5b65b": "430",
            "92e49d93-cbdc-4bcb-adb2-0e0af6c9a07c": "",
            "pre49d93-cbdc-4bcb-adb2-0e0af6c9a07c": "",

            "a5dc09e8-36f2-4bf4-97be-c9e6ca8cbe0d": "Elephant",
            "9587eb9b-f24e-4dc0-ac94-66117b896c10":"[Luke Skywalker, Yoda, Qui-Gon Jinn]",

            "6fd644b0-798e-4a58-a393-a438b32fe637-day": "1",
            "6fd644b0-798e-4a58-a393-a438b32fe637-month": "1",
            "6fd644b0-798e-4a58-a393-a438b32fe637-year": "2016",

            "06a6a4b7-6ce4-4687-879d-3443cd8e2ff0-day": "1",
            "06a6a4b7-6ce4-4687-879d-3443cd8e2ff0-month": "1",
            "06a6a4b7-6ce4-4687-879d-3443cd8e2ff0-year": "2017",

            "action[save_continue]": "Save &amp; Continue"
        }

        # Submit the form
        resp = self.client.post(first_page, data=form_data, follow_redirects=False)
        self.assertEquals(resp.status_code, 302)

        # Check we stay on the page
        self.assertEquals(resp.headers['Location'], first_page)

        resp = self.client.get(first_page, follow_redirects=False)
        self.assertEquals(resp.status_code, 200)

        # Test error messages
        content = resp.get_data(True)
        self.assertRegexpMatches(content, '1\) This field is mandatory.')

        # Correct all errors
        form_data = {

            "6cf5c72a-c1bf-4d0c-af6c-d0f07bc5b65b": "234",
            "92e49d93-cbdc-4bcb-adb2-0e0af6c9a07c": "40",
            "pre49d93-cbdc-4bcb-adb2-0e0af6c9a07c": "1370",

            "a5dc09e8-36f2-4bf4-97be-c9e6ca8cbe0d": "Elephant",
            "7587eb9b-f24e-4dc0-ac94-66118b896c10": "Luke, I am your father",
            "9587eb9b-f24e-4dc0-ac94-66117b896c10":"[Luke Skywalker, Yoda, Qui-Gon Jinn]",

            "6fd644b0-798e-4a58-a393-a438b32fe637-day": "28",
            "6fd644b0-798e-4a58-a393-a438b32fe637-month": "05",
            "6fd644b0-798e-4a58-a393-a438b32fe637-year": "1983",

            "06a6a4b7-6ce4-4687-879d-3443cd8e2ff0-day": "29",
            "06a6a4b7-6ce4-4687-879d-3443cd8e2ff0-month": "05",
            "06a6a4b7-6ce4-4687-879d-3443cd8e2ff0-year": "1983",

            "action[save_continue]": "Save &amp; Continue"
        }

        # Submit form with no errors
        resp = self.client.post(first_page, data=form_data, follow_redirects=False)
        self.assertEquals(resp.status_code, 302)
        self.assertNotEquals(resp.headers['Location'], first_page)

        # Second page
        second_page = resp.headers['Location']
        resp = self.client.get(second_page, follow_redirects=False)
        self.assertEquals(resp.status_code, 200)

        content = resp.get_data(True)

        # Make sure we are on the next page
        self.assertRegexpMatches(content, 'What was the total number of Ewokes?')
        self.assertRegexpMatches(content, '5rr015b1-f87c-4740-9fd4-f01f707ef558')
