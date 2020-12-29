from mock import patch
from tests.integration.integration_test_case import IntegrationTestCase


class TestFlushCollection(IntegrationTestCase):

    def setUp(self):
        self.submitter_patcher = patch('app.setup.LogSubmitter')
        mock_submitter_class = self.submitter_patcher.start()
        self.submitter_instance = mock_submitter_class.return_value
        self.submitter_instance.send_message.return_value = True

        self.encrypter_patcher = patch('app.views.flush_collection.encrypt')
        mock_encrypter_class = self.encrypter_patcher.start()
        self.encrypt_instance = mock_encrypter_class

        super().setUp()
        self.launchSurvey('test', '0205')
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

        super().tearDown()

    def test_no_token(self):
        """GIVEN the endpoint is called,
        WHEN the application tries to find
        the expected token in the request
        query parameters
        AND it is not there
        THEN the request should respond with:

        HTTP/1.1 400 Bad Request
        """

        self.post(url='/flush_collection')

        self.assertStatusCode(400)

    def test_cannot_decrypt_token(self):
        """GIVEN the endpoint is called,
        AND a token is given,
        WHEN the application tries to decrypt it
        AND fails
        THEN the request should respond with:

        HTTP/1.1 403 Forbidden
        """

        self.post(url='/flush_collection?token=someInvalidJWT123')

        self.assertStatusCode(403)

    def test_cannot_find_collection_id(self):
        """GIVEN the endpoint is called,
        AND a token is given,
        AND the token can be decrypted,
        WHEN the application tries to find 
        the 'collection_exercise_id' property
        AND it is not there
        THEN the request should respond with:

        HTTP/1.1 400 Bad Request
        """

        mock_payload = {'pilot': 'Po'}
        token = self.token_generator.generate_token(mock_payload)

        url = '/flush_collection?token=' + token

        self.post(url=url)

        self.assertStatusCode(400)

    def test_successful_flush(self):
        """GIVEN the endpoint is called,
        AND a token is given,
        AND the token can be decrypted,
        AND the application can find the 
        'collection_exercise_id' property,
        AND there are partial responses for
        the given collection exercise
        AND the application is able to flush them 
        THEN the request should respond with:

        HTTP/1.1 200 OK
        """

        mock_payload = {'collection_exercise_id': '0cf4d629-49f5-4f28-ab88-123b42ea9dc9'}

        token = self.token_generator.generate_token(mock_payload)

        url = '/flush_collection?token=' + token

        self.post(url=url)

        self.assertStatusCode(200)
