import unittest

from flask import current_app
from moto import mock_dynamodb2

from app.setup import create_app
from app.storage.dynamo_api import TABLE_CONFIG


class AppContextTestCase(unittest.TestCase):
    """
    unittest.TestCase that creates a Flask app context on setUp
    and destroys it on tearDown
    """
    LOGIN_DISABLED = False

    def setUp(self):
        self._ddb = mock_dynamodb2()
        self._ddb.start()

        setting_overrides = {
            'SQLALCHEMY_DATABASE_URI': 'sqlite://',
            'LOGIN_DISABLED': self.LOGIN_DISABLED,
            'EQ_DYNAMODB_ENDPOINT': None,
        }
        self._app = create_app(setting_overrides)

        self._app.config['SERVER_NAME'] = 'test.localdomain'
        self._app_context = self._app.app_context()
        self._app_context.push()

        setup_tables()

    def tearDown(self):
        self._app_context.pop()

        self._ddb.stop()

    def app_request_context(self, *args, **kwargs):
        return self._app.test_request_context(*args, **kwargs)


def setup_tables():
    for config in TABLE_CONFIG.values():
        table_name = current_app.config[config['table_name_key']]
        current_app.eq['dynamodb'].create_table(
            TableName=table_name,
            AttributeDefinitions=[{'AttributeName': config['key_field'], 'AttributeType': 'S'}],
            KeySchema=[{'AttributeName': config['key_field'], 'KeyType': 'HASH'}],
            ProvisionedThroughput={'ReadCapacityUnits': 1, 'WriteCapacityUnits': 1}
        )
