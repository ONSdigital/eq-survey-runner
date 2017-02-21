import time

from tests.integration.create_token import create_token
from tests.integration.integration_test_case import IntegrationTestCase
from tests.integration.mci import mci_test_urls
from app.views.dev_mode import generate_token


class TestFlushData(IntegrationTestCase):

    def setUp(self):
        super().setUp()

        token = create_token('0205', '1')
        self.client.get('/session?token=' + token.decode(), follow_redirects=True)

        post_data = {
            'action[start_questionnaire]': 'Start Questionnaire'
        }
        resp = self.client.post(mci_test_urls.MCI_0205_INTRODUCTION, data=post_data, follow_redirects=False)
        block_one_url = resp.location
        self.client.get(block_one_url, follow_redirects=False)

        form_data = {
            "period-from-day": "01",
            "period-from-month": "1",
            "period-from-year": "2017",
            "period-to-day": "01",
            "period-to-month": "02",
            "period-to-year": "2017",
            "total-retail-turnover": "100000",
            "action[save_continue]": "Save &amp; Continue"
        }

        self.client.post(block_one_url, data=form_data, follow_redirects=False)


    def test_flush_data_successful(self):
        resp = self.client.get('/flush?token=' + generate_token(self.get_payload()).decode(), follow_redirects=True)
        self.assertEqual(resp.status_code, 200)

    def test_no_data_to_flush(self):

        payload = self.get_payload()
        # Made up ru_ref
        payload['ru_ref'] = "no data"

        resp = self.client.get('/flush?token=' + generate_token(payload).decode(), follow_redirects=False)
        self.assertEqual(resp.status_code, 404)

    def test_no_permission_to_flush(self):

        payload = self.get_payload()
        # A role with no flush permissions
        payload['roles'] = ["test"]

        resp = self.client.get('/flush?token=' + generate_token(payload).decode(), follow_redirects=False)
        self.assertEqual(resp.status_code, 403)

    def test_no_role_on_token(self):

        payload = self.get_payload()
        # Payload with no roles
        del payload['roles']

        resp = self.client.get('/flush?token=' + generate_token(payload).decode(), follow_redirects=False)
        self.assertEqual(resp.status_code, 403)

    def test_double_flush(self):

        self.client.get('/flush?token=' + generate_token(self.get_payload()).decode(), follow_redirects=True)

        # Once the data has been flushed it is wiped. It can't be flushed again and should return 404 no data on second flush
        resp = self.client.get('/flush?token=' + generate_token(self.get_payload()).decode(), follow_redirects=True)
        self.assertEqual(resp.status_code, 404)

    def test_no_token_passed_to_flush(self):
        resp = self.client.get('/flush', follow_redirects=False)
        self.assertEqual(resp.status_code, 401)

    def test_in_valid_token_passed_to_flush(self):
        resp = self.client.get('/flush?token=test', follow_redirects=False)
        self.assertEqual(resp.status_code, 403)

    def get_payload(self):
        return {
            'iat': time.time(),
            'exp': time.time() + 1000,
            "eq_id": "1",
            "form_type": "0205",
            "collection_exercise_sid": "789",
            "ru_ref": "123456789012A",
            "roles": ["admin"],
        }
