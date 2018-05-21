import mock
from app.globals import get_dynamodb

from tests.app.app_context_test_case import AppContextTestCase


class TestGetDynamoDB(AppContextTestCase):

    @mock.patch('boto3.resource')
    def test_get_dynamodb_enabled(self, dynamodb):  # pylint: disable=unused-argument
        self._app.config['EQ_DYNAMODB_ENABLED'] = True
        self._app.config['EQ_DYNAMODB_ENDPOINT'] = 'http://localhost:6060'
        self.assertTrue(get_dynamodb())

    def test_get_dynamodb_disabled(self):
        self._app.config['EQ_DYNAMODB_ENABLED'] = False

        self.assertFalse(get_dynamodb())

        self._app.config['EQ_DYNAMODB_ENABLED'] = True
