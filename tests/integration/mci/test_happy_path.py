import unittest
from app import create_app
from tests.integration.create_token import create_token


class TestHappyPath(unittest.TestCase):
    def setUp(self):
        self.application = create_app('development')
        self.client = self.application.test_client()

    def test_happy_path_203(self):
        self.happy_path('0203')

    def test_happy_path_205(self):
        self.happy_path('0205')

    def happy_path(self,form_type_id):
        # Get a token
        token = create_token(form_type_id)
        resp = self.client.get('/session?token=' + token.decode(), follow_redirects=True)
        self.assertEquals(resp.status_code, 200)

        # We are on the landing page
        content = resp.get_data(True)
        self.assertRegexpMatches(content, '<title>Introduction</title>')
        self.assertRegexpMatches(content, '>Get Started<')
        self.assertRegexpMatches(content, '(?s)Monthly Business Survey - Retail Sales Index.*?Monthly Business Survey - Retail Sales Index')

        # We proceed to the questionnaire
        resp = self.client.get('/questionnaire', follow_redirects=True)
        self.assertEquals(resp.status_code, 200)

        # We are in the Questionnaire
        content = resp.get_data(True)
        self.assertRegexpMatches(content, '<title>Survey</title>')
        self.assertRegexpMatches(content, '>Monthly Business Survey - Retail Sales Index</')
        self.assertRegexpMatches(content, "What are the dates of the sales period you are reporting for\?")
        self.assertRegexpMatches(content, ">Save &amp; Continue<")

        # We fill in our answers
        form_data = {
            # Start Date
            "6fd644b0-798e-4a58-a393-a438b32fe637-day": "01",
            "6fd644b0-798e-4a58-a393-a438b32fe637-month": "4",
            "6fd644b0-798e-4a58-a393-a438b32fe637-year": "2016",
            # End Date
            "06a6a4b7-6ce4-4687-879d-3443cd8e2ff0-day": "30",
            "06a6a4b7-6ce4-4687-879d-3443cd8e2ff0-month": "04",
            "06a6a4b7-6ce4-4687-879d-3443cd8e2ff0-year": "2016",
            # Total Turnover
            "e81adc6d-6fb0-4155-969c-d0d646f15345": "100000"
        }

        # We submit the form
        resp = self.client.post('/questionnaire', data=form_data, follow_redirects=False)
        self.assertEquals(resp.status_code, 302)

        # There are no validation errors
        self.assertRegexpMatches(resp.headers['Location'], '\/submission$')
        resp = self.client.get('/submission', follow_redirects=True)
        self.assertEquals(resp.status_code, 200)

        # We are on the review answers page
        content = resp.get_data(True)
        self.assertRegexpMatches(content, '<title>Summary</title>')
        self.assertRegexpMatches(content, '>Monthly Business Survey - Retail Sales Index</')
        self.assertRegexpMatches(content, '>Your responses<')
        self.assertRegexpMatches(content, '>Please check carefully before submission<')
        self.assertRegexpMatches(content, '>Submit answers<')

        # We submit our answers
        post_data = {}
        resp = self.client.post('/submission', data=post_data, follow_redirects=False)
        self.assertEquals(resp.status_code, 302)
        self.assertRegexpMatches(resp.headers['Location'], '\/thank-you$')
        resp = self.client.get('/thank-you', follow_redirects=True)
        self.assertEquals(resp.status_code, 200)

        # We are on the thank you page
        content = resp.get_data(True)
        self.assertRegexpMatches(content, '<title>Thank You</title>')
        self.assertRegexpMatches(content, '(?s)Monthly Business Survey - Retail Sales Index.*?Monthly Business Survey - Retail Sales Index')
        self.assertRegexpMatches(content, '>Successfully Received<')
