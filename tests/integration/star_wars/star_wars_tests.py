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
        self.assertRegex(content, '<title>Introduction</title>')
        self.assertRegex(content, 'Star Wars')
        self.assertRegex(content, 'If actual figures are not available, please provide informed estimates.')
        self.assertRegex(content, 'Legal Information')
        self.assertRegex(content, '>Start survey<')
        self.assertRegex(content, '(?s)Trading as.*?Integration Tests')
        self.assertRegex(content, '(?s)Business name.*?MCI Integration Testing')
        self.assertRegex(content, '(?s)PLEASE SUBMIT BY.*?6 May 2016')
        self.assertRegex(content, '(?s)PERIOD.*?1 April 2016.*?30 April 2016')
        self.assertRegex(content, 'questionnaire by 6 May 2016, penalties may be incurred')

        # Legal checks
        self.assertRegex(content, 'We will treat your data securely and confidentially')
        self.assertRegex(content, 'You are required to complete this questionnaire')

        # Information to provide
        self.assertRegex(content, 'Total Yearly cost of Rebel Alliance')
        self.assertRegex(content, 'Yoda&#39;s siblings')

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

        routing_start = resp.headers['Location']

        first_page = self.default_routing(routing_start)

        return self.check_quiz_first_page(first_page)

    def start_questionnaire(self):
        # Go to questionnaire
        post_data = {
            'action[start_questionnaire]': 'Start Questionnaire'
        }
        resp = self.client.post(star_wars_test_urls.STAR_WARS_INTRODUCTION, data=post_data, follow_redirects=False)
        self.assertEqual(resp.status_code, 302)

        first_page = resp.headers['Location']
        return first_page

    def default_routing(self, current_page):
        # navigate back to first page
        self.navigate_to_page(current_page)

        form_data = {

            "ca3ce3a3-ae44-4e30-8f85-5b6a7a2fb23c": "Light Side",
            "action[save_continue]": "Save &amp; Continue"
        }

        resp = self.submit_page(current_page, form_data)
        self.assertNotEqual(resp.headers['Location'], current_page)
        current_page = resp.headers['Location']

        self.routing_pick_your_character_light_side(current_page)

        form_data = {

            "91631df0-4356-4e9f-a9d9-ce8b08d26eb3": "Light Side",
            "2e0989b8-5185-4ba6-b73f-c126e3a06ba7": "Yes",
            "action[save_continue]": "Save &amp; Continue"
        }

        resp = self.submit_page(current_page, form_data)
        self.assertNotEqual(resp.headers['Location'], current_page)
        current_page = resp.headers['Location']

        self.routing_select_your_ship_light_side(current_page)

        form_data = {

            "a2c2649a-85ff-4a26-ba3c-e1880f7c807b": "Millennium Falcon",
            "action[save_continue]": "Save &amp; Continue"
        }

        resp = self.submit_page(current_page, form_data)
        self.assertNotEqual(resp.headers['Location'], current_page)
        current_page = resp.headers['Location']

        return current_page

    def check_choose_your_side(self, start_page):
        resp = self.client.get(start_page, follow_redirects=False)
        self.assertEqual(resp.status_code, 200)
        content = resp.get_data(True)

        self.assertRegex(content, 'Choose your side')
        self.assertRegex(content, 'ca3ce3a3-ae44-4e30-8f85-5b6a7a2fb23c')
        return start_page

    def retrieve_content(self, page):
        response = self.client.get(page, follow_redirects=False)
        self.assertEqual(response.status_code, 200)
        content = response.get_data(True)
        return content

    def routing_pick_your_character_light_side(self, page):
        content = self.retrieve_content(page)
        self.assertRegex(content, 'A wise choice young Yedi. Pick your hero')
        self.assertRegex(content, '91631df0-4356-4e9f-a9d9-ce8b08d26eb3')
        self.assertRegex(content, 'Do you want to pick a ship?')
        self.assertRegex(content, '2e0989b8-5185-4ba6-b73f-c126e3a06ba7')
        return page

    def routing_pick_your_character_dark_side(self, page):
        content = self.retrieve_content(page)
        self.assertRegex(content, 'Good! Your hate has made you powerful. Pick your baddie')
        self.assertRegex(content, '653e6407-43d6-4dfc-8b11-a673a73d602d')
        self.assertRegex(content, 'Do you want to pick a ship?')
        self.assertRegex(content, 'pel989b8-5185-4ba6-b73f-c126e3a06ba7')
        return page

    def routing_select_your_ship_light_side(self, page):
        content = self.retrieve_content(page)
        self.assertRegex(content, 'Which ship do you want?')
        self.assertRegex(content, 'Millennium Falcon')
        self.assertRegex(content, 'X-wing')
        self.assertRegex(content, 'a2c2649a-85ff-4a26-ba3c-e1880f7c807b')
        return page

    def routing_select_your_ship_dark_side(self, page):
        content = self.retrieve_content(page)
        self.assertRegex(content, 'Which ship do you want?')
        self.assertRegex(content, 'TIE Fighter')
        self.assertRegex(content, 'Death Star')
        self.assertRegex(content, 'a5d5ca1a-cf58-4626-be35-dce81297688b')
        return page

    def check_quiz_first_page(self, page):
        content = self.retrieve_content(page)
        self.assertRegex(content, ">Save and continue<")
        self.assertRegex(content, 'Star Wars Quiz')
        self.assertRegex(content, 'May the force be with you young EQ developer')

        # Integer question
        self.assertRegex(content, 'How old is Chewy?')
        self.assertRegex(content, '6cf5c72a-c1bf-4d0c-af6c-d0f07bc5b65b')

        # Currency question
        self.assertRegex(content, 'How many Octillions do Nasa reckon it would cost to build a death star?')
        self.assertRegex(content, '92e49d93-cbdc-4bcb-adb2-0e0af6c9a07c')

        # Radio box question
        self.assertRegex(content,
                                 'What animal was used to create the engine sound of the Empire&#39;s TIE fighters?')  # NOQA
        self.assertRegex(content, 'Lion')
        self.assertRegex(content, 'Cow')
        self.assertRegex(content, 'Elephant')
        self.assertRegex(content, 'Hippo')
        self.assertRegex(content, 'a5dc09e8-36f2-4bf4-97be-c9e6ca8cbe0d')

        # Checkbox question
        self.assertRegex(content, 'Which 3 have wielded a green lightsaber?')
        self.assertRegex(content, 'Luke Skywalker')
        self.assertRegex(content, 'Anakin Skywalker')
        self.assertRegex(content, 'Obi-Wan Kenobi')
        self.assertRegex(content, 'Yoda')
        self.assertRegex(content, 'Rey')
        self.assertRegex(content, 'Qui-Gon Jinn')
        self.assertRegex(content, '9587eb9b-f24e-4dc0-ac94-66117b896c10')

        # Date Range question
        self.assertRegex(content, 'When was The Empire Strikes Back released?')
        self.assertRegex(content, 'Period from')
        self.assertRegex(content, 'Period to')
        self.assertRegex(content, 'Day')
        self.assertRegex(content, 'Month')
        self.assertRegex(content, 'Year')
        self.assertRegex(content, '6fd644b0-798e-4a58-a393-a438b32fe637')
        self.assertRegex(content, '06a6a4b7-6ce4-4687-879d-3443cd8e2ff0')

        # Pipe Test for question description
        self.assertRegex(content,
                                 'It could be between 1 April 2016 and 30 April 2016. But that might just be a test')  # NOQA

        return page

    def check_second_quiz_page(self, page):
        resp = self.client.get(page, follow_redirects=False)
        self.assertEqual(resp.status_code, 200)

        content = resp.get_data(True)

        # Pipe Test for section title
        self.assertRegex(content, 'On 2 June 1983 how many were employed?')

        # Textarea question
        self.assertRegex(content, 'Why doesn\'t Chewbacca receive a medal at the end of A New Hope?')
        self.assertRegex(content, '215015b1-f87c-4740-9fd4-f01f707ef558')

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
        self.assertRegex(resp.headers['Location'], r'/questionnaire\/0\/' + form_type_id + '\/789\/thank-you$')
        resp = self.client.get(resp.headers['Location'], follow_redirects=True)
        self.assertEqual(resp.status_code, 200)

    def rogue_one_login_and_check_introduction_text(self):
        self.token = create_token('rogue_one', '0')
        response = self.get_first_page()
        self.rogue_one_check_introduction_text(response)

    def rogue_one_check_introduction_text(self, response):
        content = response.get_data(True)
        self.assertRegex(content, '<title>Introduction</title>')
        self.assertRegex(content, '(?s)Rogue One')

    def rogue_one_check_character_page(self, page):
        content = self.retrieve_content(page)
        self.assertRegex(content, 'Who do you want to know more about?')
        self.assertRegex(content, 'Jyn Erso')
        self.assertRegex(content, 'ca3ce3a3-ae44-4e30-8f85-5b6a7a2fb23c-3')

    def rogue_one_check_description_page(self, page):
        content = self.retrieve_content(page)
        self.assertRegex(content, 'An accomplished Rebel Alliance Intelligence Officer')
        self.assertRegex(content, 'Do you like this page?')
        self.assertRegex(content, '3f1f1bb7-2452-4f8d-ac7a-735ea5d4517f-2')

    def rogue_one_check_takings_page(self, page):
        content = self.retrieve_content(page)
        self.assertRegex(content, 'In millions, how much do you think this film will take?')
        self.assertRegex(content, 'a04a516d-502d-4068-bbed-a43427c68cd9')

    def rogue_one_check_confirmation_page(self, page):
        content = self.retrieve_content(page)
        self.assertRegex(content, 'Summary')
        self.assertRegex(content, 'Please check carefully before submission')
