from tests.integration.create_token import create_token
from tests.integration.star_wars import star_wars_test_urls
from tests.integration.star_wars.star_wars_tests import StarWarsTestCase


class TestConfirmationPage(StarWarsTestCase):

    def test_confirmation_page(self):
        self.rogue_one_login_and_check_introduction_text()
        post_data = {
            'action[start_questionnaire]': 'Start Questionnaire'
        }
        response = self.client.post(star_wars_test_urls.ROGUE_ONE_INTRODUCTION, data=post_data, follow_redirects=False)
        self.assertEqual(response.status_code, 302)

        character_page = response.headers['Location']

        self.rogue_one_check_character_page(character_page)

        # Our answers
        form_data = {
            "ca3ce3a3-ae44-4e30-8f85-5b6a7a2fb23c": "Cassian Andor",
            # User Action
            "action[save_continue]": "Save &amp; Continue"
        }

        # Form submission with no errors
        resp = self.submit_page(character_page, form_data)
        self.assertNotEqual(resp.location, character_page)

        # Like page
        description_page = resp.location

        self.rogue_one_check_description_page(description_page)

        # Our answers
        form_data = {
            "3f1f1bb7-2452-4f8d-ac7a-735ea5d4517f": "Yes",
            # User Action
            "action[save_continue]": "Save &amp; Continue"
        }

        # Form submission with no errors
        resp = self.submit_page(description_page, form_data)
        self.assertNotEqual(resp.location, description_page)

        # Takings page
        takings_page = resp.location

        self.rogue_one_check_takings_page(takings_page)

        # Our answers
        form_data = {
            "a04a516d-502d-4068-bbed-a43427c68cd9": "900",
            # User Action
            "action[save_continue]": "Save &amp; Continue"
        }

        # Form submission with no errors
        resp = self.submit_page(takings_page, form_data)
        self.assertNotEqual(resp.location, takings_page)

        # Confirmation page
        confirmation_page = resp.location

        self.rogue_one_check_confirmation_page(confirmation_page)

        # User Action
        form_data["action[save_continue]"] = "Save &amp; Continue"

        # Form submission with no errors
        resp = self.submit_page(confirmation_page, form_data)
        self.assertNotEqual(resp.location, confirmation_page)

        self.complete_survey('rogue_one')

    def rogue_one_login_and_check_introduction_text(self):
        token = create_token('rogue_one', '0')
        response = self.get_first_page(token)
        self.rogue_one_check_introduction_text(response)

    def rogue_one_check_introduction_text(self, response):
        content = response.get_data(True)
        self.assertIn('<title>Introduction</title>', content)
        self.assertRegex(content, '(?s)Rogue One')

    def rogue_one_check_character_page(self, page):
        content = self.retrieve_content(page)
        self.assertIn('Who do you want to know more about?', content)
        self.assertIn('Jyn Erso', content)
        self.assertIn('ca3ce3a3-ae44-4e30-8f85-5b6a7a2fb23c-3', content)

    def rogue_one_check_description_page(self, page):
        content = self.retrieve_content(page)
        self.assertIn('An accomplished Rebel Alliance Intelligence Officer', content)
        self.assertIn('Do you like this page?', content)
        self.assertIn('3f1f1bb7-2452-4f8d-ac7a-735ea5d4517f-1', content)

    def rogue_one_check_takings_page(self, page):
        content = self.retrieve_content(page)
        self.assertIn('In millions, how much do you think this film will take?', content)
        self.assertIn('a04a516d-502d-4068-bbed-a43427c68cd9', content)

    def rogue_one_check_confirmation_page(self, page):
        content = self.retrieve_content(page)
        self.assertIn('Summary', content)
        self.assertIn('Please check carefully before submission', content)
