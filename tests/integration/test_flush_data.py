import time
import uuid

from mock import patch

from tests.integration.integration_test_case import IntegrationTestCase


class TestFlushData(IntegrationTestCase):
    def setUp(self):
        self.submitter_patcher = patch('app.setup.LogSubmitter')
        mock_submitter_class = self.submitter_patcher.start()
        self.submitter_instance = mock_submitter_class.return_value
        self.submitter_instance.send_message.return_value = True

        self.encrypter_patcher = patch('app.routes.flush.encrypt')
        mock_encrypter_class = self.encrypter_patcher.start()
        self.encrypt_instance = mock_encrypter_class

        super().setUp()
        self.launchSurvey('test_textfield')

        form_data = {'name-answer': 'Joe Bloggs'}
        self.post(form_data)

    def tearDown(self):
        self.submitter_patcher.stop()
        self.encrypter_patcher.stop()

        super().tearDown()

    def test_flush_data_successful(self):
        self.post(
            url='/flush?token='
            + self.token_generator.generate_token(self.get_payload())
        )
        self.assertStatusOK()

    def test_no_data_to_flush(self):
        payload = self.get_payload()
        # Made up response_id
        payload['response_id'] = '0000000000000000'

        self.post(url='/flush?token=' + self.token_generator.generate_token(payload))
        self.assertStatusNotFound()

    def test_no_permission_to_flush(self):
        payload = self.get_payload()
        # A role with no flush permissions
        payload['roles'] = ['test']

        self.post(url='/flush?token=' + self.token_generator.generate_token(payload))
        self.assertStatusForbidden()

    def test_no_role_on_token(self):
        payload = self.get_payload()
        # Payload with no roles
        del payload['roles']

        self.post(url='/flush?token=' + self.token_generator.generate_token(payload))
        self.assertStatusForbidden()

    def test_double_flush(self):
        self.post(
            url='/flush?token='
            + self.token_generator.generate_token(self.get_payload())
        )

        # Once the data has been flushed it is wiped.
        # It can't be flushed again and should return 404 no data on second flush
        self.post(
            url='/flush?token='
            + self.token_generator.generate_token(self.get_payload())
        )
        self.assertStatusNotFound()

    def test_no_token_passed_to_flush(self):
        self.post(url='/flush')
        self.assertStatusForbidden()

    def test_invalid_token_passed_to_flush(self):
        self.post(url='/flush?token=test')
        self.assertStatusForbidden()

    def test_flush_errors_when_submission_fails(self):
        self.submitter_instance.send_message.return_value = (
            False
        )  # pylint: disable=no-member

        self.post(
            url='/flush?token='
            + self.token_generator.generate_token(self.get_payload())
        )
        self.assertStatusCode(500)

    def test_flush_sets_flushed_flag_to_true(self):

        self.post(
            url='/flush?token='
            + self.token_generator.generate_token(self.get_payload())
        )

        self.encrypt_instance.assert_called_once()  # pylint: disable=no-member
        args = self.encrypt_instance.call_args[0]  # pylint: disable=no-member

        self.assertTrue('"flushed": true' in args[0])

    @staticmethod
    def get_payload():
        return {
            'jti': str(uuid.uuid4()),
            'iat': time.time(),
            'exp': time.time() + 1000,
            'response_id': '1234567890123456',
            'roles': ['flusher'],
        }
