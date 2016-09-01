from tests.integration.create_token import create_token
from tests.integration.integration_test_case import IntegrationTestCase
from werkzeug.datastructures import MultiDict


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
        self.assertRegexpMatches(content, '<title>Introduction</title>')
        self.assertRegexpMatches(content, '(?s)Star Wars.*?Star Wars')
        self.assertRegexpMatches(content, 'If actual figures are not available, please provide informed estimates.')
        self.assertRegexpMatches(content, 'How is your information used?')
        self.assertRegexpMatches(content, '>Get Started<')
        self.assertRegexpMatches(content, '(?s)Trading as.*?Integration Tests')
        self.assertRegexpMatches(content, '(?s)To be completed by.*?MCI Integration Testing')
        self.assertRegexpMatches(content, '(?s)PLEASE SUBMIT BY.*?6 May 2016')
        self.assertRegexpMatches(content, '(?s)PERIOD.*?1 April 2016.*?30 April 2016')

        # Legal checks
        self.assertRegexpMatches(content, 'Notice is given under section 1 of the Statistics of Trade Act 1947')
        self.assertRegexpMatches(content, 'You are required by law to complete this questionnaire')
        self.assertRegexpMatches(content, 'NB: Your response is legally required')

        # Information to provide
        self.assertRegexpMatches(content, 'Total Yearly cost of Rebel Alliance')
        self.assertRegexpMatches(content, 'Yoda&#39;s siblings')

    def get_first_page(self):
        resp = self.client.get('/session?token=' + self.token.decode(), follow_redirects=True)
        self.assertEquals(resp.status_code, 200)
        return resp

    def start_questionnaire_and_navigate_routing(self):
        # Go to questionnaire
        post_data = {
            'action[start_questionnaire]': 'Start Questionnaire'
        }
        resp = self.client.post('/questionnaire/0/star_wars/201604/789/introduction', data=post_data, follow_redirects=False)
        self.assertEquals(resp.status_code, 302)

        routing_start = resp.headers['Location']
        repeating_elements = self.default_routing(routing_start)
        first_page = self.repeating_elements(repeating_elements)

        return self.check_quiz_first_page(first_page)

    def default_routing(self, current_page):

        # navigate back to first page
        self.navigate_to_page(current_page)

        form_data = {

            "ca3ce3a3-ae44-4e30-8f85-5b6a7a2fb23c": "Light Side",
            "action[save_continue]": "Save &amp; Continue"
        }

        resp = self.submit_page(current_page, form_data)
        self.assertNotEquals(resp.headers['Location'], current_page)
        current_page = resp.headers['Location']

        self.routing_pick_your_character_light_side(current_page)

        form_data = {

            "91631df0-4356-4e9f-a9d9-ce8b08d26eb3": "Light Side",
            "2e0989b8-5185-4ba6-b73f-c126e3a06ba7": "Yes",
            "action[save_continue]": "Save &amp; Continue"
        }

        resp = self.submit_page(current_page, form_data)
        self.assertNotEquals(resp.headers['Location'], current_page)
        current_page = resp.headers['Location']

        self.routing_select_your_ship_light_side(current_page)

        form_data = {

            "a2c2649a-85ff-4a26-ba3c-e1880f7c807b": "Millennium Falcon",
            "action[save_continue]": "Save &amp; Continue"
        }

        resp = self.submit_page(current_page, form_data)
        self.assertNotEquals(resp.headers['Location'], current_page)
        current_page = resp.headers['Location']

        return current_page


    def repeating_elements(self, repeating_question_page):

        # navigate back to first page
        self.navigate_to_page(repeating_question_page)
        self.check_repeating_question(repeating_question_page)

        form_data = {

            "8fe76762-d07f-4a1f-a315-0b0385940f8c": "2",
            "action[save_continue]": "Save &amp; Continue"
        }

        resp = self.submit_page(repeating_question_page, form_data)
        self.assertNotEquals(resp.headers['Location'], repeating_question_page)
        first_repeat = resp.headers['Location']
        self.navigate_to_page(first_repeat)

        form_data = {

            "56b6f367-e84b-43fa-a5e2-19193f223fa0_1": "crawler1",
            "action[save_continue]": "Save &amp; Continue"
        }

        resp = self.submit_page(first_repeat, form_data)
        self.assertNotEquals(resp.headers['Location'], first_repeat)
        self.check_repeating_answer(first_repeat, "56b6f367-e84b-43fa-a5e2-19193f223fa0_1")
        second_repeat = resp.headers['Location']
        self.navigate_to_page(second_repeat)


        form_data = {
            "56b6f367-e84b-43fa-a5e2-19193f223fa0_2": "crawler2",
            "action[save_continue]": "Save &amp; Continue"
        }

        resp = self.submit_page(second_repeat, form_data)
        self.assertNotEquals(resp.headers['Location'], second_repeat)
        questionnaire_page = resp.headers['Location']

        return questionnaire_page


    def check_repeating_question(self, repeating_question_page):
        resp = self.client.get(repeating_question_page, follow_redirects=False)
        self.assertEquals(resp.status_code, 200)
        content = resp.get_data(True)

        self.assertRegexpMatches(content, 'How many starting crawlers do you know?')
        self.assertRegexpMatches(content, '8fe76762-d07f-4a1f-a315-0b0385940f8c')


    def check_repeating_answer(self, repeating_answer_page, question_id):
        resp = self.client.get(repeating_answer_page, follow_redirects=False)
        self.assertEquals(resp.status_code, 200)
        content = resp.get_data(True)
        self.assertRegexpMatches(content, 'Please provide a general description of each crawler you know')
        self.assertRegexpMatches(content, question_id )


    def check_choose_your_side(self, start_page):
        resp = self.client.get(start_page, follow_redirects=False)
        self.assertEquals(resp.status_code, 200)
        content = resp.get_data(True)

        self.assertRegexpMatches(content, 'Choose your side')
        self.assertRegexpMatches(content, 'ca3ce3a3-ae44-4e30-8f85-5b6a7a2fb23c')
        return start_page

    def retrieve_content(self, page):
        response = self.client.get(page, follow_redirects=False)
        self.assertEquals(response.status_code, 200)
        content = response.get_data(True)
        return content

    def routing_pick_your_character_light_side(self,page):
        content = self.retrieve_content(page)
        self.assertRegexpMatches(content, 'A wise choice young Yedi. Pick your hero')
        self.assertRegexpMatches(content, '91631df0-4356-4e9f-a9d9-ce8b08d26eb3')
        self.assertRegexpMatches(content, 'Do you want to pick a ship?')
        self.assertRegexpMatches(content, '2e0989b8-5185-4ba6-b73f-c126e3a06ba7')
        return page

    def routing_pick_your_character_dark_side(self,page):
        content = self.retrieve_content(page)
        self.assertRegexpMatches(content, 'Good! Your hate has made you powerful. Pick your baddie')
        self.assertRegexpMatches(content, '653e6407-43d6-4dfc-8b11-a673a73d602d')
        self.assertRegexpMatches(content, 'Do you want to pick a ship?')
        self.assertRegexpMatches(content, 'pel989b8-5185-4ba6-b73f-c126e3a06ba7')
        return page

    def routing_select_your_ship_light_side(self, page):
        content = self.retrieve_content(page)
        self.assertRegexpMatches(content, 'Which ship do you want?')
        self.assertRegexpMatches(content, 'Millennium Falcon')
        self.assertRegexpMatches(content, 'X-wing')
        self.assertRegexpMatches(content, 'a2c2649a-85ff-4a26-ba3c-e1880f7c807b')
        return page

    def routing_select_your_ship_dark_side(self, page):
        content = self.retrieve_content(page)
        self.assertRegexpMatches(content, 'Which ship do you want?')
        self.assertRegexpMatches(content, 'TIE Fighter')
        self.assertRegexpMatches(content, 'Death Star')
        self.assertRegexpMatches(content, 'a5d5ca1a-cf58-4626-be35-dce81297688b')
        return page

    def check_quiz_first_page(self, page):
        content = self.retrieve_content(page)
        self.assertRegexpMatches(content, ">Save &amp; Continue<")
        self.assertRegexpMatches(content, 'Star Wars Quiz')
        self.assertRegexpMatches(content, 'May the force be with you young EQ developer')

        # Integer question
        self.assertRegexpMatches(content, 'How old is Chewy?')
        self.assertRegexpMatches(content, '6cf5c72a-c1bf-4d0c-af6c-d0f07bc5b65b')

        # Currency question
        self.assertRegexpMatches(content, 'How many Octillions do Nasa reckon it would cost to build a death star?')
        self.assertRegexpMatches(content, '92e49d93-cbdc-4bcb-adb2-0e0af6c9a07c')

        # Radio box question
        self.assertRegexpMatches(content, 'What animal was used to create the engine sound of the Empire&#39;s TIE fighters?')  # NOQA
        self.assertRegexpMatches(content, 'Lion')
        self.assertRegexpMatches(content, 'Cow')
        self.assertRegexpMatches(content, 'Elephant')
        self.assertRegexpMatches(content, 'Hippo')
        self.assertRegexpMatches(content, 'a5dc09e8-36f2-4bf4-97be-c9e6ca8cbe0d')

        # Checkbox question
        self.assertRegexpMatches(content, 'Which 3 have wielded a green lightsaber?')
        self.assertRegexpMatches(content, 'Luke Skywalker')
        self.assertRegexpMatches(content, 'Anakin Skywalker')
        self.assertRegexpMatches(content, 'Obi-Wan Kenobi')
        self.assertRegexpMatches(content, 'Yoda')
        self.assertRegexpMatches(content, 'Rey')
        self.assertRegexpMatches(content, 'Qui-Gon Jinn')
        self.assertRegexpMatches(content, '9587eb9b-f24e-4dc0-ac94-66117b896c10')

        # Date Range question
        self.assertRegexpMatches(content, 'When was The Empire Strikes Back released?')
        self.assertRegexpMatches(content, 'From')
        self.assertRegexpMatches(content, 'To')
        self.assertRegexpMatches(content, 'Day')
        self.assertRegexpMatches(content, 'Month')
        self.assertRegexpMatches(content, 'Year')
        self.assertRegexpMatches(content, '6fd644b0-798e-4a58-a393-a438b32fe637')
        self.assertRegexpMatches(content, '06a6a4b7-6ce4-4687-879d-3443cd8e2ff0')

        # Pipe Test for question description
        self.assertRegexpMatches(content, 'It could be between 1 April 2016 and 30 April 2016. But that might just be a test')  # NOQA

        return page

    def check_second_quiz_page(self, page):
        resp = self.client.get(page, follow_redirects=False)
        self.assertEquals(resp.status_code, 200)

        content = resp.get_data(True)

        # Pipe Test for section title
        self.assertRegexpMatches(content, 'On 2 June 1983 how many were employed?')

        # Textarea question
        self.assertRegexpMatches(content, 'Why doesn&#39;t Chewbacca receive a medal at the end of A New Hope?')
        self.assertRegexpMatches(content, '215015b1-f87c-4740-9fd4-f01f707ef558')

    def submit_page(self, page, form_data):
        resp = self.client.post(page, data=form_data, follow_redirects=False)
        self.assertEquals(resp.status_code, 302)
        return resp

    def navigate_to_page(self, page):
        resp = self.client.get(page, follow_redirects=False)
        self.assertEquals(resp.status_code, 200)
        return resp

    def complete_survey(self, summary_page, form_type_id):
        # Submit answers
        post_data = {
            "action[submit_answers]": "Submit answers"
        }
        resp = self.client.post(summary_page, data=post_data, follow_redirects=False)

        self.assertEquals(resp.status_code, 302)
        self.assertRegexpMatches(resp.headers['Location'], r'/questionnaire\/0\/'+ form_type_id+ '\/201604\/789\/thank-you$')
        resp = self.client.get(resp.headers['Location'], follow_redirects=True)
        self.assertEquals(resp.status_code, 200)

        # Thank you page
        content = resp.get_data(True)
        self.assertRegexpMatches(content, '<title>Submission Successful</title>')

    def rogue_one_login_and_check_introduction_text(self):
        self.token = create_token('rogue_one', '0')
        response = self.get_first_page()
        self.rogue_one_check_introduction_text(response)

    def rogue_one_check_introduction_text(self, response):
        content = response.get_data(True)
        self.assertRegexpMatches(content, '<title>Introduction</title>')
        self.assertRegexpMatches(content, '(?s)Rogue One.*?Rogue One')
        self.assertRegexpMatches(content, 'Good luck in stealing the plans to the Death Star')

    def rogue_one_check_character_page(self, page):
        content = self.retrieve_content(page)
        self.assertRegexpMatches(content, 'Who do you want to know more about?')
        self.assertRegexpMatches(content, 'Jyn Erso')
        self.assertRegexpMatches(content, 'ca3ce3a3-ae44-4e30-8f85-5b6a7a2fb23c-3')

    def rogue_one_check_description_page(self, page):
        content = self.retrieve_content(page)
        self.assertRegexpMatches(content, 'An accomplished Rebel Alliance Intelligence Officer')
        self.assertRegexpMatches(content, 'Do you like this page?')
        self.assertRegexpMatches(content, '3f1f1bb7-2452-4f8d-ac7a-735ea5d4517f-2')

    def rogue_one_check_takings_page(self, page):
        content = self.retrieve_content(page)
        self.assertRegexpMatches(content, 'In millions, how much do you think this film will take?')
        self.assertRegexpMatches(content, 'a04a516d-502d-4068-bbed-a43427c68cd9')

    def rogue_one_check_confirmation_page(self, page):
        content = self.retrieve_content(page)
        self.assertRegexpMatches(content, 'Summary')
        self.assertRegexpMatches(content, 'Please check carefully before submission')
