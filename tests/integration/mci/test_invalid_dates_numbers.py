from tests.integration.create_token import create_token
from tests.integration.integration_test_case import IntegrationTestCase


class TestInvalidDateNumber(IntegrationTestCase):

    def test_invalid_date_number_205(self):
        self.invalid_date_number('0205', '1')

    def invalid_date_number(self, form_type_id, eq_id):
        # Get a token
        token = create_token(form_type_id, eq_id)
        resp = self.client.get('/session?token=' + token.decode(), follow_redirects=True)
        self.assertEquals(resp.status_code, 200)

        # We are on the landing page
        content = resp.get_data(True)
        self.assertRegexpMatches(content, '<title>Introduction</title>')
        self.assertRegexpMatches(content, '>Get Started<')
        self.assertRegexpMatches(content, '(?s)Monthly Business Survey - Retail Sales Index.*?Monthly Business Survey - Retail Sales Index')

        # We proceed to the questionnaire
        post_data = {
            'action[start_questionnaire]': 'Start Questionnaire'
        }
        resp = self.client.post('/questionnaire/' + eq_id + '/789/introduction', data=post_data, follow_redirects=False)
        self.assertEquals(resp.status_code, 302)

        # We proceed to the questionnaire
        resp = self.client.get('/questionnaire/' + eq_id + '/789/cd3b74d1-b687-4051-9634-a8f9ce10a27d', follow_redirects=True)
        self.assertEquals(resp.status_code, 200)

        # We are in the Questionnaire
        content = resp.get_data(True)
        self.assertRegexpMatches(content, "What are the dates of the sales period you are reporting for\?")
        self.assertRegexpMatches(content, ">Save &amp; Continue<")

        form_data = {
            # Start Date
            "6fd644b0-798e-4a58-a393-a438b32fe637-day": "01",
            "6fd644b0-798e-4a58-a393-a438b32fe637-month": "1",
            "6fd644b0-798e-4a58-a393-a438b32fe637-year": "",
            # End Date
            "06a6a4b7-6ce4-4687-879d-3443cd8e2ff0-day": "01",
            "06a6a4b7-6ce4-4687-879d-3443cd8e2ff0-month": "01",
            "06a6a4b7-6ce4-4687-879d-3443cd8e2ff0-year": "",
            # Total Turnover
            "e81adc6d-6fb0-4155-969c-d0d646f15345": "100000",
            # User action
            "action[save_continue]": "Save &amp; Continue"
        }

        # We submit the form with an invalid date
        resp = self.client.post('/questionnaire/' + eq_id + '/789/cd3b74d1-b687-4051-9634-a8f9ce10a27d', data=form_data, follow_redirects=True)
        self.assertEquals(resp.status_code, 200)
        content = resp.get_data(True)
        self.assertRegexpMatches(content, "The date entered is not valid.  Please correct your answer.")

        form_data = {
            # Start Date
            "6fd644b0-798e-4a58-a393-a438b32fe637-day": "01",
            "6fd644b0-798e-4a58-a393-a438b32fe637-month": "01",
            "6fd644b0-798e-4a58-a393-a438b32fe637-year": "2016",
            # End Date
            "06a6a4b7-6ce4-4687-879d-3443cd8e2ff0-day": "01",
            "06a6a4b7-6ce4-4687-879d-3443cd8e2ff0-month": "01",
            "06a6a4b7-6ce4-4687-879d-3443cd8e2ff0-year": "2017",
            # Total Turnover
            "e81adc6d-6fb0-4155-969c-d0d646f15345": "rubbish",
            # User action
            "action[save_continue]": "Save &amp; Continue"
        }

        # We submit the form without a valid turnover value
        resp = self.client.post('/questionnaire/' + eq_id + '/789/cd3b74d1-b687-4051-9634-a8f9ce10a27d', data=form_data, follow_redirects=True)
        self.assertEquals(resp.status_code, 200)
        content = resp.get_data(True)
        self.assertRegexpMatches(content, "Please only enter whole numbers into the field.")

        form_data = {
            # Start Date
            "6fd644b0-798e-4a58-a393-a438b32fe637-day": "01",
            "6fd644b0-798e-4a58-a393-a438b32fe637-month": "01",
            "6fd644b0-798e-4a58-a393-a438b32fe637-year": "2016",
            # End Date
            "06a6a4b7-6ce4-4687-879d-3443cd8e2ff0-day": "01",
            "06a6a4b7-6ce4-4687-879d-3443cd8e2ff0-month": "01",
            "06a6a4b7-6ce4-4687-879d-3443cd8e2ff0-year": "",
            # Total Turnover
            "e81adc6d-6fb0-4155-969c-d0d646f15345": "10000",
            # User action
            "action[save_continue]": "Save &amp; Continue"
        }

        # We submit the form without a valid 2nd date
        resp = self.client.post('/questionnaire/' + eq_id + '/789/cd3b74d1-b687-4051-9634-a8f9ce10a27d', data=form_data, follow_redirects=True)
        self.assertEquals(resp.status_code, 200)
        content = resp.get_data(True)
        self.assertRegexpMatches(content, "The date entered is not valid")

        # We try to access the submission page without correction
        resp = self.client.get('/questionnaire/1/789/summary', follow_redirects=True)
        self.assertEquals(resp.status_code, 200)
        content = resp.get_data(True)
        self.assertRegexpMatches(content, "What are the dates of the sales period you are reporting for\?")

        form_data = {
            # Start Date
            "6fd644b0-798e-4a58-a393-a438b32fe637-day": "01",
            "6fd644b0-798e-4a58-a393-a438b32fe637-month": "01",
            "6fd644b0-798e-4a58-a393-a438b32fe637-year": "2017",
            # End Date
            "06a6a4b7-6ce4-4687-879d-3443cd8e2ff0-day": "01",
            "06a6a4b7-6ce4-4687-879d-3443cd8e2ff0-month": "01",
            "06a6a4b7-6ce4-4687-879d-3443cd8e2ff0-year": "2016",
            # Total Turnover
            "e81adc6d-6fb0-4155-969c-d0d646f15345": "10000",
            # User action
            "action[save_continue]": "Save &amp; Continue"
        }

        # We submit the form with the front date later then the to date
        resp = self.client.post('/questionnaire/' + eq_id + '/789/cd3b74d1-b687-4051-9634-a8f9ce10a27d', data=form_data, follow_redirects=True)
        self.assertEquals(resp.status_code, 200)
        content = resp.get_data(True)
        self.assertRegexpMatches(content, "The &#39;to&#39; date cannot be before the &#39;from&#39; date.")

        form_data = {
            # Start Date
            "6fd644b0-798e-4a58-a393-a438b32fe637-day": "01",
            "6fd644b0-798e-4a58-a393-a438b32fe637-month": "01",
            "6fd644b0-798e-4a58-a393-a438b32fe637-year": "2016",
            # End Date
            "06a6a4b7-6ce4-4687-879d-3443cd8e2ff0-day": "01",
            "06a6a4b7-6ce4-4687-879d-3443cd8e2ff0-month": "01",
            "06a6a4b7-6ce4-4687-879d-3443cd8e2ff0-year": "2016",
            # Total Turnover
            "e81adc6d-6fb0-4155-969c-d0d646f15345": "100000",
            # User action
            "action[save_continue]": "Save &amp; Continue"
        }

        # We submit the form with the dates the same
        resp = self.client.post('/questionnaire/' + eq_id + '/789/cd3b74d1-b687-4051-9634-a8f9ce10a27d', data=form_data, follow_redirects=True)
        self.assertEquals(resp.status_code, 200)
        content = resp.get_data(True)
        self.assertRegexpMatches(content, "The &#39;to&#39; date must be different to the &#39;from&#39; date.")

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
            "e81adc6d-6fb0-4155-969c-d0d646f15345": "100000",
            # User action
            "action[save_continue]": "Save &amp; Continue"
        }

        # We correct our answers and submit
        resp = self.client.post('/questionnaire/' + eq_id + '/789/cd3b74d1-b687-4051-9634-a8f9ce10a27d', data=form_data, follow_redirects=False)
        self.assertEquals(resp.status_code, 302)

        # There are no validation errors
        self.assertRegexpMatches(resp.headers['Location'], '\/questionnaire\/1\/789\/summary$')
        resp = self.client.get(resp.headers['Location'], follow_redirects=True)
        self.assertEquals(resp.status_code, 200)

        # We are on the review answers page
        content = resp.get_data(True)
        self.assertRegexpMatches(content, '>Your responses<')
        self.assertRegexpMatches(content, '>Please check carefully before submission<')
        self.assertRegexpMatches(content, '>Submit answers<')

        # We submit our answers
        post_data = {
            "action[submit_answers]": 'Submit answers'
        }
        resp = self.client.post('/questionnaire/' + eq_id + '/789/summary', data=post_data, follow_redirects=False)
        self.assertEquals(resp.status_code, 302)
        self.assertRegexpMatches(resp.headers['Location'], '\/questionnaire\/1\/789\/thank-you$')
        resp = self.client.get(resp.headers['Location'], follow_redirects=True)
        self.assertEquals(resp.status_code, 200)

        # We are on the thank you page
        content = resp.get_data(True)
        self.assertRegexpMatches(content, '>Successfully Received<')
