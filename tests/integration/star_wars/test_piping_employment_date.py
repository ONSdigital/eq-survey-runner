import unittest
from app import create_app
from tests.integration.create_token import create_token
from app import settings


class TestPipingEmploymentDate(unittest.TestCase):
    def setUp(self):
        settings.EQ_SERVER_SIDE_STORAGE = False
        self.application = create_app('development')
        self.client = self.application.test_client()

    def test_piping_employment_date(self):
        eq_id = "0"
        # Get a token
        token = create_token('star_wars', eq_id)
        resp = self.client.get('/session?token=' + token.decode(), follow_redirects=True)
        self.assertEquals(resp.status_code, 200)

        # We are on the landing page
        content = resp.get_data(True)

        self.assertRegexpMatches(content, '<title>Introduction</title>')
        self.assertRegexpMatches(content, '>Get Started<')
        self.assertRegexpMatches(content, '(?s)Star Wars.*?Star Wars')

         # We proceed to the questionnaire
        post_data = {
            'action[start_questionnaire]': 'Start Questionnaire'
        }
        resp = self.client.post('/questionnaire/' + eq_id + '/789/introduction', data=post_data, follow_redirects=False)
        self.assertEquals(resp.status_code, 302)

        first_page = resp.headers['Location']



        resp = self.client.get(first_page, follow_redirects=False)
        self.assertEquals(resp.status_code, 200)

        # We are in the Questionnaire
        content = resp.get_data(True)

        # Questionnaire Title
        self.assertRegexpMatches(content, 'Star Wars Quiz')
        self.assertRegexpMatches(content, 'May the force be with you young EQ developer')
        self.assertRegexpMatches(content, ">Save &amp; Continue<")

        # We fill in our answers
        form_data = {
            # Start Date
            "6cf5c72a-c1bf-4d0c-af6c-d0f07bc5b65b": "234",
            "92e49d93-cbdc-4bcb-adb2-0e0af6c9a07c" : "40",
            "pre49d93-cbdc-4bcb-adb2-0e0af6c9a07c": "1370",

            "a5dc09e8-36f2-4bf4-97be-c9e6ca8cbe0d": "Elephant",
            "7587eb9b-f24e-4dc0-ac94-66118b896c10" : "Luke, I am your father",

            "6fd644b0-798e-4a58-a393-a438b32fe637-day": "28",
            "6fd644b0-798e-4a58-a393-a438b32fe637-month": "05",
            "6fd644b0-798e-4a58-a393-a438b32fe637-year": "1983",
            # End Date
            "06a6a4b7-6ce4-4687-879d-3443cd8e2ff0-day": "29",
            "06a6a4b7-6ce4-4687-879d-3443cd8e2ff0-month": "05",
            "06a6a4b7-6ce4-4687-879d-3443cd8e2ff0-year": "1983",
            # User Action
            "action[save_continue]": "Save &amp; Continue"
        }

         # We submit the form
        resp = self.client.post(first_page, data=form_data, follow_redirects=False)
        self.assertEquals(resp.status_code, 302)

        # On to page two
        second_page = resp.headers['Location']

        resp = self.client.get(second_page, follow_redirects=False)
        self.assertEquals(resp.status_code, 200)

        # We are in the Questionnaire
        content = resp.get_data(True)


        # We are in the Questionnaire
        content = resp.get_data(True)

        self.assertRegexpMatches(content, 'On 2 June 1983 how many were employed?')
