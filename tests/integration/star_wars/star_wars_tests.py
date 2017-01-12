from tests.integration.create_token import create_token
from tests.integration.integration_test_case import IntegrationTestCase
from tests.integration.star_wars import star_wars_test_urls


class StarWarsTestCase(IntegrationTestCase):
    def setUp(self):
        super().setUp()

    def login_and_check_introduction_text(self):
        self.token = create_token('star_wars', '0')
        resp = self.get_first_page()
        self.check_introduction_text(resp)

    def check_introduction_text(self, response):
        # Landing page tests
        content = response.get_data(True)
        self.assertIn('<title>Introduction</title>', content)
        self.assertIn('Star Wars', content)
        self.assertIn('If actual figures are not available, please provide informed estimates.', content)
        self.assertIn('Legal Information', content)
        self.assertIn('>Start survey<', content)
        self.assertRegex(content, '(?s)Trading as.*?Integration Tests')
        self.assertRegex(content, '(?s)Business name.*?MCI Integration Testing')
        self.assertRegex(content, '(?s)PLEASE SUBMIT BY.*?6 May 2016')
        self.assertRegex(content, '(?s)PERIOD.*?1 April 2016.*?30 April 2016')
        self.assertIn('questionnaire by 6 May 2016, penalties may be incurred', content)

        # Legal checks
        self.assertIn('We will treat your data securely and confidentially', content)
        self.assertIn('You are required to complete this questionnaire', content)

        # Information to provide
        self.assertIn('Total Yearly cost of Rebel Alliance', content)
        self.assertIn('Yoda&#39;s siblings', content)

    def get_first_page(self):
        resp = self.client.get('/session?token=' + self.token.decode(), follow_redirects=True)
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

        first_page = self.default_routing(routing_start)

        return self.check_quiz_first_page(first_page)

    def start_questionnaire(self):
        # Go to questionnaire
        post_data = {
            'action[start_questionnaire]': 'Start Questionnaire'
        }
        resp = self.client.post(star_wars_test_urls.STAR_WARS_INTRODUCTION, data=post_data, follow_redirects=False)
        self.assertEqual(resp.status_code, 302)

        first_page = resp.location
        return first_page

    def default_routing(self, current_page):
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

            "91631df0-4356-4e9f-a9d9-ce8b08d26eb3": "Light Side",
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

    def check_choose_your_side(self, start_page):
        resp = self.client.get(start_page, follow_redirects=False)
        self.assertEqual(resp.status_code, 200)
        content = resp.get_data(True)

        self.assertIn('Choose your side', content)
        self.assertIn('ca3ce3a3-ae44-4e30-8f85-5b6a7a2fb23c', content)
        return start_page

    def retrieve_content(self, page):
        response = self.client.get(page, follow_redirects=False)
        self.assertEqual(response.status_code, 200)
        content = response.get_data(True)
        return content

    def routing_pick_your_character_light_side(self, page):
        content = self.retrieve_content(page)
        self.assertIn('A wise choice young Yedi. Pick your hero', content)
        self.assertIn('91631df0-4356-4e9f-a9d9-ce8b08d26eb3', content)
        self.assertIn('Do you want to pick a ship?', content)
        self.assertIn('2e0989b8-5185-4ba6-b73f-c126e3a06ba7', content)
        return page

    def routing_pick_your_character_dark_side(self, page):
        content = self.retrieve_content(page)
        self.assertIn('Good! Your hate has made you powerful. Pick your baddie', content)
        self.assertIn('653e6407-43d6-4dfc-8b11-a673a73d602d', content)
        self.assertIn('Do you want to pick a ship?', content)
        self.assertIn('pel989b8-5185-4ba6-b73f-c126e3a06ba7', content)
        return page

    def routing_select_your_ship_light_side(self, page):
        content = self.retrieve_content(page)
        self.assertIn('Which ship do you want?', content)
        self.assertIn('Millennium Falcon', content)
        self.assertIn('X-wing', content)
        self.assertIn('a2c2649a-85ff-4a26-ba3c-e1880f7c807b', content)
        return page

    def routing_select_your_ship_dark_side(self, page):
        content = self.retrieve_content(page)
        self.assertIn('Which ship do you want?', content)
        self.assertIn('TIE Fighter', content)
        self.assertIn('Death Star', content)
        self.assertIn('a5d5ca1a-cf58-4626-be35-dce81297688b', content)
        return page

    def check_quiz_first_page(self, page):
        content = self.retrieve_content(page)
        self.assertIn(">Save and continue<", content)
        self.assertIn('Star Wars Quiz', content)
        self.assertIn('May the force be with you young EQ developer', content)

        # Integer question
        self.assertIn('How old is Chewy?', content)
        self.assertIn('6cf5c72a-c1bf-4d0c-af6c-d0f07bc5b65b', content)

        # Currency question
        self.assertIn('How many Octillions do Nasa reckon it would cost to build a death star?', content)
        self.assertIn('92e49d93-cbdc-4bcb-adb2-0e0af6c9a07c', content)

        # Radio box question
        self.assertIn('What animal was used to create the engine sound of the Empire&#39;s TIE fighters?', content)  # NOQA
        self.assertIn('Lion', content)
        self.assertIn('Cow', content)
        self.assertIn('Elephant', content)
        self.assertIn('Hippo', content)
        self.assertIn('a5dc09e8-36f2-4bf4-97be-c9e6ca8cbe0d', content)

        # Checkbox question
        self.assertIn('Which 3 have wielded a green lightsaber?', content)
        self.assertIn('Luke Skywalker', content)
        self.assertIn('Anakin Skywalker', content)
        self.assertIn('Obi-Wan Kenobi', content)
        self.assertIn('Yoda', content)
        self.assertIn('Rey', content)
        self.assertIn('Qui-Gon Jinn', content)
        self.assertIn('9587eb9b-f24e-4dc0-ac94-66117b896c10', content)

        # Date Range question
        self.assertIn('When was The Empire Strikes Back released?', content)
        self.assertIn('Period from', content)
        self.assertIn('Period to', content)
        self.assertIn('Day', content)
        self.assertIn('Month', content)
        self.assertIn('Year', content)
        self.assertIn('6fd644b0-798e-4a58-a393-a438b32fe637', content)
        self.assertIn('06a6a4b7-6ce4-4687-879d-3443cd8e2ff0', content)

        # Pipe Test for question description
        self.assertIn('It could be between 1 April 2016 and 30 April 2016. But that might just be a test', content)  # NOQA

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

    def complete_survey(self, summary_page, form_type_id):
        # Submit answers
        post_data = {
            "action[submit_answers]": "Submit answers"
        }
        resp = self.client.post(summary_page, data=post_data, follow_redirects=False)

        self.assertEqual(resp.status_code, 302)
        self.assertRegex(resp.location, r'/questionnaire\/0\/' + form_type_id + r'\/789\/thank-you$')
        resp = self.client.get(resp.location, follow_redirects=True)
        self.assertEqual(resp.status_code, 200)

    def rogue_one_login_and_check_introduction_text(self):
        self.token = create_token('rogue_one', '0')
        response = self.get_first_page()
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
        self.assertIn('3f1f1bb7-2452-4f8d-ac7a-735ea5d4517f-2', content)

    def rogue_one_check_takings_page(self, page):
        content = self.retrieve_content(page)
        self.assertIn('In millions, how much do you think this film will take?', content)
        self.assertIn('a04a516d-502d-4068-bbed-a43427c68cd9', content)

    def rogue_one_check_confirmation_page(self, page):
        content = self.retrieve_content(page)
        self.assertIn('Summary', content)
        self.assertIn('Please check carefully before submission', content)
