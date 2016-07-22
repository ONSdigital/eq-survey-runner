from tests.integration.star_wars.star_wars_tests import StarWarsTestCase


class TestPageErrors(StarWarsTestCase):
    def test_multi_page_errors(self):
        # Get a token

        self.assert_introduction_text()

        first_page = self.start_questionnaire()

        second_page = self.submit_first_page(first_page)

        resp = self.client.get(second_page, follow_redirects=False)
        self.assertEquals(resp.status_code, 200)

        content = resp.get_data(True)

        # Pipe Test for section title
        self.assertRegexpMatches(content, 'On 2 June 1983 how many were employed?')

        # Textarea question
        self.assertRegexpMatches(content, 'Why doesn&#39;t Chewbacca receive a medal at the end of A New Hope?')
        self.assertRegexpMatches(content, '215015b1-f87c-4740-9fd4-f01f707ef558')

        # Our answers
        form_data = {
            # Make this data missing
            "215015b1-f87c-4740-9fd4-f01f707ef558": "", # Required answer
            # User Action
            "action[save_continue]": "Save &amp; Continue"
        }

        resp = self.client.post(second_page, data=form_data, follow_redirects=False)
        self.assertEquals(resp.status_code, 302)

        # There are validation errors
        self.assertEquals(resp.headers['Location'], second_page)

        # Go back to the first page
        resp = self.client.get(first_page, follow_redirects=False)
        self.assertEquals(resp.status_code, 200)

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
        resp = self.client.post(first_page, data=form_data, follow_redirects=False)
        self.assertEquals(resp.status_code, 302)

        # We have a validation error
        self.assertEquals(resp.headers['Location'], first_page)
        resp = self.client.get(first_page, follow_redirects=False)
        self.assertEquals(resp.status_code, 200)

        content = resp.get_data(True)
        self.assertRegex(content, '<a href="#a5dc09e8-36f2-4bf4-97be-c9e6ca8cbe0d">Go to this error')
        # We DO NOT have the error from page two
        self.assertNotRegex(content, '<a href="215015b1-f87c-4740-9fd4-f01f707ef558">Go to this error')
