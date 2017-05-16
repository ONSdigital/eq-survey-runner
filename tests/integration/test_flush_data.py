import time
from mock import patch
from tests.integration.integration_test_case import IntegrationTestCase
from tests.integration.create_token import generate_token


class TestFlushData(IntegrationTestCase):

    def setUp(self):
        self.submitter_patcher = patch('app.LogSubmitter')
        mock_submitter_class = self.submitter_patcher.start()
        self.submitter_instance = mock_submitter_class.return_value
        self.submitter_instance.send_message.return_value = True

        self.encrypter_patcher = patch('app.Encrypter')
        mock_encrypter_class = self.encrypter_patcher.start()
        self.encrypt_instance = mock_encrypter_class.return_value

        super().setUp()
        self.launchSurvey('1', '0205')
        self.post(action='start_questionnaire')

        form_data = {
            'period-from-day': '01',
            'period-from-month': '4',
            'period-from-year': '2016',
            'period-to-day': '30',
            'period-to-month': '4',
            'period-to-year': '2016',
            'total-retail-turnover': '100000'
        }
        self.post(form_data)

    def tearDown(self):
        self.submitter_patcher.stop()
        self.encrypter_patcher.stop()

    def test_flush_data_successful(self):
        self.get('/flush?token=' + generate_token(self.get_payload()).decode())
        self.assertStatusOK()

    def test_no_data_to_flush(self):
        payload = self.get_payload()
        # Made up ru_ref
        payload['ru_ref'] = 'no data'

        self.get('/flush?token=' + generate_token(payload).decode())
        self.assertStatusNotFound()

    def test_no_permission_to_flush(self):
        payload = self.get_payload()
        # A role with no flush permissions
        payload['roles'] = ['test']

        self.get('/flush?token=' + generate_token(payload).decode())
        self.assertStatusForbidden()

    def test_no_role_on_token(self):
        payload = self.get_payload()
        # Payload with no roles
        del payload['roles']

        self.get('/flush?token=' + generate_token(payload).decode())
        self.assertStatusForbidden()

    def test_double_flush(self):
        self.get('/flush?token=' + generate_token(self.get_payload()).decode())

        # Once the data has been flushed it is wiped.
        # It can't be flushed again and should return 404 no data on second flush
        self.get('/flush?token=' + generate_token(self.get_payload()).decode())
        self.assertStatusNotFound()

    def test_no_token_passed_to_flush(self):
        self.get('/flush')
        self.assertStatusForbidden()

    def test_invalid_token_passed_to_flush(self):
        self.get('/flush?token=test')
        self.assertStatusForbidden()

    def test_flush_errors_when_submission_fails(self):
        self.submitter_instance.send_message.return_value = False  # pylint: disable=no-member

        self.get('/flush?token=' + generate_token(self.get_payload()).decode())
        self.assertStatusCode(503)

    def test_flush_sets_flushed_flag_to_true(self):

        self.get('/flush?token=' + generate_token(self.get_payload()).decode())

        self.encrypt_instance.encrypt.assert_called_once() # pylint: disable=no-member
        args = self.encrypt_instance.encrypt.call_args[0] # pylint: disable=no-member

        self.assertTrue(args[0]['flushed'])

    @staticmethod
    def get_payload():
        return {
            'iat': time.time(),
            'exp': time.time() + 1000,
            'eq_id': '1',
            'form_type': '0205',
            'collection_exercise_sid': '789',
            'ru_ref': '123456789012A',
            'roles': ['flusher'],
        }
