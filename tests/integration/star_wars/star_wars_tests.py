from tests.integration.create_token import create_token
from tests.integration.integration_test_case import IntegrationTestCase
from tests.integration.star_wars import star_wars_test_urls


class StarWarsTestCase(IntegrationTestCase):
    def setUp(self):
        super().setUp()

    def login(self):
        token = create_token('star_wars', '0')
        return self.get_first_page(token)

    def get_first_page(self, token):
        resp = self.client.get('/session?token=' + token.decode(), follow_redirects=True)
        self.assertEqual(resp.status_code, 200)
        return resp

    def start_questionnaire_and_navigate_routing(self):
        # Go to questionnaire
        post_data = {
            'action[start_questionnaire]': 'Start Questionnaire'
        }
        resp = self.client.post(star_wars_test_urls.STAR_WARS_INTRODUCTION, data=post_data, follow_redirects=False)
        self.assertEqual(resp.status_code, 302)

        routing_start = resp.location

        return self._default_routing(routing_start)

    def _default_routing(self, current_page):
        # navigate back to first page
        self.navigate_to_page(current_page)

        form_data = {

            "ca3ce3a3-ae44-4e30-8f85-5b6a7a2fb23c": "Light Side",
            "action[save_continue]": "Save &amp; Continue"
        }

        resp = self.submit_page(current_page, form_data)
        self.assertNotEqual(resp.location, current_page)
        current_page = resp.location

        self.routing_pick_your_character_light_side(current_page)

        form_data = {
            "91631df0-4356-4e9f-a9d9-ce8b08d26eb3": "Leyoda",
            "2e0989b8-5185-4ba6-b73f-c126e3a06ba7": "Yes",
            "action[save_continue]": "Save &amp; Continue"
        }

        resp = self.submit_page(current_page, form_data)
        self.assertNotEqual(resp.location, current_page)
        current_page = resp.location

        self.routing_select_your_ship_light_side(current_page)

        form_data = {
            "a2c2649a-85ff-4a26-ba3c-e1880f7c807b": "Millennium Falcon",
            "action[save_continue]": "Save &amp; Continue"
        }

        resp = self.submit_page(current_page, form_data)
        self.assertNotEqual(resp.location, current_page)
        current_page = resp.location

        return current_page

    def retrieve_content(self, page):
        response = self.client.get(page, follow_redirects=False)
        self.assertEqual(response.status_code, 200)
        content = response.get_data(True)
        return content

    def routing_pick_your_character_light_side(self, page):
        content = self.retrieve_content(page)
        self.assertIn('A wise choice young Jedi. Pick your hero', content)
        self.assertIn('91631df0-4356-4e9f-a9d9-ce8b08d26eb3', content)
        self.assertIn('Do you want to pick a ship?', content)
        self.assertIn('2e0989b8-5185-4ba6-b73f-c126e3a06ba7', content)
        return page

    def routing_select_your_ship_light_side(self, page):
        content = self.retrieve_content(page)
        self.assertIn('Which ship do you want?', content)
        self.assertIn('Millennium Falcon', content)
        self.assertIn('X-wing', content)
        self.assertIn('a2c2649a-85ff-4a26-ba3c-e1880f7c807b', content)
        return page

    def check_second_quiz_page(self, page):
        resp = self.client.get(page, follow_redirects=False)
        self.assertEqual(resp.status_code, 200)

        content = resp.get_data(True)

        # Pipe Test for section title
        self.assertIn('On 2 June 1983 how many were employed?', content)

        # Textarea question
        self.assertIn('Why doesn\'t Chewbacca receive a medal at the end of A New Hope?', content)
        self.assertIn('215015b1-f87c-4740-9fd4-f01f707ef558', content)

    def submit_page(self, page, form_data):
        resp = self.client.post(page, data=form_data, follow_redirects=False)
        return resp

    def navigate_to_page(self, page):
        resp = self.client.get(page, follow_redirects=False)
        self.assertEqual(resp.status_code, 200)
        return resp

    def complete_survey(self, form_type):
        # Submit answers
        post_data = {
            "action[submit_answers]": "Submit answers"
        }
        _, resp = self.postRedirectGet('/questionnaire/0/{form_type}/789/submit-answers'.format(form_type=form_type), post_data)
        return resp
