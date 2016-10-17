from tests.integration.star_wars.star_wars_tests import StarWarsTestCase
from werkzeug.datastructures import MultiDict


class TestDarkSidePath(StarWarsTestCase):

    def test_dark_side_path(self):
        self.login_and_check_introduction_text()

        first_page = self.start_questionnaire_and_navigate_routing()

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

        form_data = MultiDict({

            "6cf5c72a-c1bf-4d0c-af6c-d0f07bc5b65b": "555555555555555555",
            "92e49d93-cbdc-4bcb-adb2-0e0af6c9a07c": "text",
            "pre49d93-cbdc-4bcb-adb2-0e0af6c9a07c": "###",

            "a5dc09e8-36f2-4bf4-97be-c9e6ca8cbe0d": "",
            "7587eb9b-f24e-4dc0-ac94-66118b896c10": "",
            "9587eb9b-f24e-4dc0-ac94-66117b896c10": "",

            "6fd644b0-798e-4a58-a393-a438b32fe637-day": "",
            "6fd644b0-798e-4a58-a393-a438b32fe637-month": "",
            "6fd644b0-798e-4a58-a393-a438b32fe637-year": "",

            "06a6a4b7-6ce4-4687-879d-3443cd8e2ff0-day": "30",
            "06a6a4b7-6ce4-4687-879d-3443cd8e2ff0-month": "2",
            "06a6a4b7-6ce4-4687-879d-3443cd8e2ff0-year": "2016",

            "action[save_continue]": "Save &amp; Continue"
        })

        # Submit the form
        resp = self.submit_page(first_page, form_data)

        # Test error messages
        content = resp.get_data(True)
        self.assertRegexpMatches(content, 'No one lives that long, not even Yoda')
        self.assertRegexpMatches(content, 'Please only enter whole numbers into the field.')
        self.assertRegexpMatches(content, 'Please only enter whole numbers into the field.')
        self.assertRegexpMatches(content, 'This field is mandatory.')
        self.assertRegexpMatches(content, 'This field is mandatory.')
        self.assertRegexpMatches(content, 'The date entered is not valid')
        self.assertRegexpMatches(content, 'The date entered is not valid')

        '''
        Testing
               Integer  - Mandatory
                        - Negative
               Currency - To large
               Date     - From and to the same
        '''

        form_data = MultiDict({

            "6cf5c72a-c1bf-4d0c-af6c-d0f07bc5b65b": "",
            "92e49d93-cbdc-4bcb-adb2-0e0af6c9a07c": "9999999999999",
            "pre49d93-cbdc-4bcb-adb2-0e0af6c9a07c": "-5",

            "a5dc09e8-36f2-4bf4-97be-c9e6ca8cbe0d": "Elephant",
            "9587eb9b-f24e-4dc0-ac94-66117b896c10": ['Luke Skywalker', 'Yoda', 'Qui-Gon Jinn'],

            "6fd644b0-798e-4a58-a393-a438b32fe637-day": "1",
            "6fd644b0-798e-4a58-a393-a438b32fe637-month": "1",
            "6fd644b0-798e-4a58-a393-a438b32fe637-year": "2016",

            "06a6a4b7-6ce4-4687-879d-3443cd8e2ff0-day": "1",
            "06a6a4b7-6ce4-4687-879d-3443cd8e2ff0-month": "1",
            "06a6a4b7-6ce4-4687-879d-3443cd8e2ff0-year": "2016",

            "action[save_continue]": "Save &amp; Continue"
        })

        # Submit the form
        resp = self.submit_page(first_page, form_data)

        # Test error messages
        content = resp.get_data(True)
        self.assertRegexpMatches(content, 'This field is mandatory')
        self.assertRegexpMatches(content, 'How much, idiot you must be')
        self.assertRegexpMatches(content, 'How can it be negative?')
        self.assertRegexpMatches(content, 'The &#39;period to&#39; date must be different to the &#39;period from&#39; date.')

        '''
         Testing
                Currency  - Negative
                Date      - To before From
        '''

        form_data = MultiDict({

            "6cf5c72a-c1bf-4d0c-af6c-d0f07bc5b65b": "430",
            "92e49d93-cbdc-4bcb-adb2-0e0af6c9a07c": "-10",
            "pre49d93-cbdc-4bcb-adb2-0e0af6c9a07c": "",

            "a5dc09e8-36f2-4bf4-97be-c9e6ca8cbe0d": "Elephant",
            "9587eb9b-f24e-4dc0-ac94-66117b896c10": ['Luke Skywalker', 'Yoda', 'Qui-Gon Jinn'],

            "6fd644b0-798e-4a58-a393-a438b32fe637-day": "1",
            "6fd644b0-798e-4a58-a393-a438b32fe637-month": "1",
            "6fd644b0-798e-4a58-a393-a438b32fe637-year": "2016",

            "06a6a4b7-6ce4-4687-879d-3443cd8e2ff0-day": "1",
            "06a6a4b7-6ce4-4687-879d-3443cd8e2ff0-month": "1",
            "06a6a4b7-6ce4-4687-879d-3443cd8e2ff0-year": "2015",

            "action[save_continue]": "Save &amp; Continue"
        })

        # Submit the form
        resp = self.submit_page(first_page, form_data)

        # Test error messages
        content = resp.get_data(True)
        self.assertRegexpMatches(content, 'How can it be negative?')
        self.assertRegexpMatches(content, 'The &#39;period to&#39; date cannot be before the &#39;period from&#39; date.')

        # Testing Currency  - Mandatory

        form_data = MultiDict({

            "6cf5c72a-c1bf-4d0c-af6c-d0f07bc5b65b": "430",
            "92e49d93-cbdc-4bcb-adb2-0e0af6c9a07c": "",
            "pre49d93-cbdc-4bcb-adb2-0e0af6c9a07c": "",

            "a5dc09e8-36f2-4bf4-97be-c9e6ca8cbe0d": "Elephant",
            "9587eb9b-f24e-4dc0-ac94-66117b896c10": ['Luke Skywalker', 'Yoda', 'Qui-Gon Jinn'],

            "6fd644b0-798e-4a58-a393-a438b32fe637-day": "1",
            "6fd644b0-798e-4a58-a393-a438b32fe637-month": "1",
            "6fd644b0-798e-4a58-a393-a438b32fe637-year": "2016",

            "06a6a4b7-6ce4-4687-879d-3443cd8e2ff0-day": "1",
            "06a6a4b7-6ce4-4687-879d-3443cd8e2ff0-month": "1",
            "06a6a4b7-6ce4-4687-879d-3443cd8e2ff0-year": "2017",

            "action[save_continue]": "Save &amp; Continue"
        })

        # Submit the form
        resp = self.submit_page(first_page, form_data)

        # Test error messages
        content = resp.get_data(True)
        self.assertRegexpMatches(content, 'This field is mandatory.')

        # Correct all errors
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

        # Submit form with no errors
        resp = self.submit_page(first_page, form_data)
        self.assertNotEquals(resp.headers['Location'], first_page)

        # Second page
        second_page = resp.headers['Location']
        resp = self.navigate_to_page(second_page)

        content = resp.get_data(True)

        # Make sure we are on the next page
        self.assertRegexpMatches(content, 'What was the total number of Ewokes?')
        self.assertRegexpMatches(content, '5rr015b1-f87c-4740-9fd4-f01f707ef558')
