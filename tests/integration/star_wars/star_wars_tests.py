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
        self.assertRegexpMatches(content, '<title>Introduction</title>')
        self.assertRegexpMatches(content, 'Star Wars')
        self.assertRegexpMatches(content, 'If actual figures are not available, please provide informed estimates.')
        self.assertRegexpMatches(content, 'Legal Information')
        self.assertRegexpMatches(content, '>Start survey<')
        self.assertRegexpMatches(content, '(?s)Trading as.*?Integration Tests')
        self.assertRegexpMatches(content, '(?s)Business name.*?MCI Integration Testing')
        self.assertRegexpMatches(content, '(?s)PLEASE SUBMIT BY.*?6 May 2016')
        self.assertRegexpMatches(content, '(?s)PERIOD.*?1 April 2016.*?30 April 2016')
        self.assertRegexpMatches(content, 'questionnaire by 6 May 2016, penalties may be incurred')

        # Legal checks
        self.assertRegexpMatches(content, 'We will treat your data securely and confidentially')
        self.assertRegexpMatches(content, 'You are required to complete this questionnaire')

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
        resp = self.client.post(star_wars_test_urls.STAR_WARS_INTRODUCTION, data=post_data, follow_redirects=False)
        self.assertEquals(resp.status_code, 302)

        routing_start = resp.headers['Location']

        first_page = self.default_routing(routing_start)

        return self.check_quiz_first_page(first_page)

    def start_questionnaire(self):
        # Go to questionnaire
        post_data = {
            'action[start_questionnaire]': 'Start Questionnaire'
        }
        resp = self.client.post(star_wars_test_urls.STAR_WARS_INTRODUCTION, data=post_data, follow_redirects=False)
        self.assertEquals(resp.status_code, 302)

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

    def routing_pick_your_character_light_side(self, page):
        content = self.retrieve_content(page)
        self.assertRegexpMatches(content, 'A wise choice young Yedi. Pick your hero')
        self.assertRegexpMatches(content, '91631df0-4356-4e9f-a9d9-ce8b08d26eb3')
        self.assertRegexpMatches(content, 'Do you want to pick a ship?')
        self.assertRegexpMatches(content, '2e0989b8-5185-4ba6-b73f-c126e3a06ba7')
        return page

    def routing_pick_your_character_dark_side(self, page):
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
        self.assertRegexpMatches(content, ">Save and continue<")
        self.assertRegexpMatches(content, 'Star Wars Quiz')
        self.assertRegexpMatches(content, 'May the force be with you young EQ developer')

        # Integer question
        self.assertRegexpMatches(content, 'How old is Chewy?')
        self.assertRegexpMatches(content, '6cf5c72a-c1bf-4d0c-af6c-d0f07bc5b65b')

        # Currency question
        self.assertRegexpMatches(content, 'How many Octillions do Nasa reckon it would cost to build a death star?')
        self.assertRegexpMatches(content, '92e49d93-cbdc-4bcb-adb2-0e0af6c9a07c')

        # Radio box question
        self.assertRegexpMatches(content,
                                 'What animal was used to create the engine sound of the Empire&#39;s TIE fighters?')  # NOQA
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
        self.assertRegexpMatches(content, 'Period from')
        self.assertRegexpMatches(content, 'Period to')
        self.assertRegexpMatches(content, 'Day')
        self.assertRegexpMatches(content, 'Month')
        self.assertRegexpMatches(content, 'Year')
        self.assertRegexpMatches(content, '6fd644b0-798e-4a58-a393-a438b32fe637')
        self.assertRegexpMatches(content, '06a6a4b7-6ce4-4687-879d-3443cd8e2ff0')

        # Pipe Test for question description
        self.assertRegexpMatches(content,
                                 'It could be between 1 April 2016 and 30 April 2016. But that might just be a test')  # NOQA

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
        self.assertRegexpMatches(resp.headers['Location'], r'/questionnaire\/0\/' + form_type_id + '\/789\/thank-you$')
        resp = self.client.get(resp.headers['Location'], follow_redirects=True)
        self.assertEquals(resp.status_code, 200)

    def rogue_one_login_and_check_introduction_text(self):
        self.token = create_token('rogue_one', '0')
        response = self.get_first_page()
        self.rogue_one_check_introduction_text(response)

    def rogue_one_check_introduction_text(self, response):
        content = response.get_data(True)
        self.assertRegexpMatches(content, '<title>Introduction</title>')
        self.assertRegexpMatches(content, '(?s)Rogue One')

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
