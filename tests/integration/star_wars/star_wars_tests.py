from tests.integration.create_token import create_token
from tests.integration.integration_test_case import IntegrationTestCase


class StarWarsTestCase(IntegrationTestCase):
    def setUp(self):
        super().setUp()
        self.token = create_token('star_wars', '0')

    def login_and_check_introduction_text(self):
        resp = self.client.get('/session?token=' + self.token.decode(), follow_redirects=True)
        self.assertEquals(resp.status_code, 200)
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

    def start_questionnaire(self):
        # Go to questionnaire
        post_data = {
            'action[start_questionnaire]': 'Start Questionnaire'
        }
        resp = self.client.post('/questionnaire/0/789/introduction', data=post_data, follow_redirects=False)
        self.assertEquals(resp.status_code, 302)

        first_page = resp.headers['Location']
        return self.check_first_page(first_page)

    def check_first_page(self, first_page):
        resp = self.client.get(first_page, follow_redirects=False)
        self.assertEquals(resp.status_code, 200)

        # Questionnaire tests
        content = resp.get_data(True)
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

        return first_page

    def check_second_page(self, second_page):
        resp = self.client.get(second_page, follow_redirects=False)
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

    def complete_survey(self, summary_page):
        # Submit answers
        post_data = {
            "action[submit_answers]": "Submit answers"
        }
        resp = self.client.post(summary_page, data=post_data, follow_redirects=False)

        self.assertEquals(resp.status_code, 302)
        self.assertRegexpMatches(resp.headers['Location'], r'\/questionnaire\/0\/789\/thank-you$')
        resp = self.client.get(resp.headers['Location'], follow_redirects=True)
        self.assertEquals(resp.status_code, 200)

        # Thank you page
        content = resp.get_data(True)
        self.assertRegexpMatches(content, '<title>Thank You</title>')
        self.assertRegexpMatches(content, '(?s)Star Wars.*?Star Wars')
        self.assertRegexpMatches(content, '>Successfully Received<')
