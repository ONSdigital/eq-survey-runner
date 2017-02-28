from tests.integration.create_token import create_token
from tests.integration.integration_test_case import IntegrationTestCase
from tests.integration.mci import mci_test_urls


class TestInvalidDateNumber(IntegrationTestCase):

    def test_correct_invalid_date(self):
        # Get a token
        token = create_token('0205', '1')
        resp = self.client.get('/session?token=' + token.decode(), follow_redirects=True)
        self.assertEqual(resp.status_code, 200)

        # We are on the landing page
        content = resp.get_data(True)
        self.assertRegex(content, '<title>Introduction</title>')
        self.assertRegex(content, '>Start survey<')
        self.assertRegex(content, 'Monthly Business Survey - Retail Sales Index')

        # We proceed to the questionnaire
        post_data = {
            'action[start_questionnaire]': 'Start Questionnaire'
        }
        resp = self.client.post(mci_test_urls.MCI_0205_INTRODUCTION, data=post_data, follow_redirects=False)
        self.assertEqual(resp.status_code, 302)

        form_data = {
            # Start Date
            "period-from-day": "01",
            "period-from-month": "1",
            "period-from-year": "2016",
            # End Date
            "period-to-day": "01",
            "period-to-month": "1",
            "period-to-year": "2016",
            # Total Turnover
            "total-retail-turnover": "100000",
            # User action
            "action[save_continue]": "Save &amp; Continue"
        }

        # We submit the form with the dates the same
        resp = self.client.post(mci_test_urls.MCI_0205_BLOCK1, data=form_data, follow_redirects=True)
        self.assertEqual(resp.status_code, 200)
        content = resp.get_data(True)
        self.assertRegex(content, "The &#39;period to&#39; date must be different to the &#39;period from&#39; date.")

        form_data = {
            # Start Date
            "period-from-day": "01",
            "period-from-month": "1",
            "period-from-year": "2016",
            # End Date
            "period-to-day": "01",
            "period-to-month": "1",
            "period-to-year": "2017",
            # Total Turnover
            "total-retail-turnover": "10000",
            # User action
            "action[save_continue]": "Save &amp; Continue"
        }

        # We correct our answers and submit
        resp = self.client.post(mci_test_urls.MCI_0205_BLOCK1, data=form_data, follow_redirects=False)
        self.assertEqual(resp.status_code, 302)

        # There are no validation errors
        self.assertRegex(resp.location, mci_test_urls.MCI_0205_SUMMARY)
        resp = self.client.get(resp.location, follow_redirects=True)
        self.assertEqual(resp.status_code, 200)

        # We are on the review answers page
        content = resp.get_data(True)
        self.assertRegex(content, '>Your responses<')
        self.assertRegex(content, 'Please check carefully before submission')
        self.assertRegex(content, '>Submit answers<')

        # We submit our answers
        post_data = {
            "action[submit_answers]": 'Submit answers'
        }
        _, resp = self.postRedirectGet('/questionnaire/1/0205/789/submit-answers', post_data)

        # We are on the thank you page
        content = resp.get_data(True)
        self.assertRegex(content, '<title>Submission Successful</title>')

    def test_invalid_same_date(self):
        # Get a token
        token = create_token('0205', '1')
        resp = self.client.get('/session?token=' + token.decode(), follow_redirects=True)
        self.assertEqual(resp.status_code, 200)
        form_data = {
            # Start Date
            "period-from-day": "01",
            "period-from-month": "1",
            "period-from-year": "2016",
            # End Date
            "period-to-day": "01",
            "period-to-month": "1",
            "period-to-year": "2016",
            # Total Turnover
            "total-retail-turnover": "10000",
            # User action
            "action[save_continue]": "Save &amp; Continue"
        }
        # We submit the form with the dates the same
        resp = self.client.post(mci_test_urls.MCI_0205_BLOCK1, data=form_data, follow_redirects=True)
        self.assertEqual(resp.status_code, 200)
        content = resp.get_data(True)
        self.assertRegex(content, "The &#39;period to&#39; date must be different to the &#39;period from&#39; date.")

    def test_invalid_date_range(self):
        # Get a token
        token = create_token('0205', '1')
        resp = self.client.get('/session?token=' + token.decode(), follow_redirects=True)
        self.assertEqual(resp.status_code, 200)

        form_data = {
            # Start Date
            "period-from-day": "01",
            "period-from-month": "1",
            "period-from-year": "2017",
            # End Date
            "period-to-day": "01",
            "period-to-month": "1",
            "period-to-year": "2016",
            # Total Turnover
            "total-retail-turnover": "10000",
            # User action
            "action[save_continue]": "Save &amp; Continue"
        }
        # We submit the form with the front date later then the to date
        resp = self.client.post(mci_test_urls.MCI_0205_BLOCK1, data=form_data, follow_redirects=True)
        self.assertEqual(resp.status_code, 200)
        content = resp.get_data(True)
        self.assertRegex(content, "The &#39;period to&#39; date cannot be before the &#39;period from&#39; date.")

    def test_invalid_year(self):
        # Get a token
        token = create_token('0205', '1')
        resp = self.client.get('/session?token=' + token.decode(), follow_redirects=True)
        self.assertEqual(resp.status_code, 200)
        form_data = {
            # Start Date
            "period-from-day": "01",
            "period-from-month": "1",
            "period-from-year": "",
            # End Date
            "period-to-day": "01",
            "period-to-month": "1",
            "period-to-year": "",
            # Total Turnover
            "total-retail-turnover": "100000",
            # User action
            "action[save_continue]": "Save &amp; Continue"
        }

        # We submit the form without a valid 2nd date
        resp = self.client.post(mci_test_urls.MCI_0205_BLOCK1, data=form_data, follow_redirects=True)
        self.assertEqual(resp.status_code, 200)
        content = resp.get_data(True)
        self.assertRegex(content, "The date entered is not valid")

    def test_invalid_integer(self):
        # Get a token
        token = create_token('0205', '1')
        resp = self.client.get('/session?token=' + token.decode(), follow_redirects=True)
        self.assertEqual(resp.status_code, 200)
        form_data = {
            # Start Date
            "period-from-day": "01",
            "period-from-month": "1",
            "period-from-year": "2016",
            # End Date
            "period-to-day": "01",
            "period-to-month": "1",
            "period-to-year": "2017",
            # Total Turnover
            "total-retail-turnover": "rubbish",
            # User action
            "action[save_continue]": "Save &amp; Continue"
        }

        # We submit the form without a valid turnover value
        resp = self.client.post(mci_test_urls.MCI_0205_BLOCK1, data=form_data, follow_redirects=True)
        self.assertEqual(resp.status_code, 200)
        content = resp.get_data(True)
        self.assertRegex(content, "Please only enter whole numbers into the field.")

    def test_invalid_date_number(self):
        # Get a token
        token = create_token('0205', '1')
        resp = self.client.get('/session?token=' + token.decode(), follow_redirects=True)
        self.assertEqual(resp.status_code, 200)
        form_data = {
            # Start Date
            "period-from-day": "01",
            "period-from-month": "1",
            "period-from-year": "",
            # End Date
            "period-to-day": "01",
            "period-to-month": "1",
            "period-to-year": "",
            # Total Turnover
            "total-retail-turnover": "100000",
            # User action
            "action[save_continue]": "Save &amp; Continue"
        }

        # We submit the form with an invalid date
        resp = self.client.post(mci_test_urls.MCI_0205_BLOCK1, data=form_data, follow_redirects=True)
        self.assertEqual(resp.status_code, 200)
        content = resp.get_data(True)
        self.assertRegex(content, "The date entered is not valid.  Please correct your answer.")
