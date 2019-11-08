import boto3
from flask import current_app
from moto import mock_dynamodb2

from app.data_model.app_models import QuestionnaireState
from app.storage.dynamodb import TABLE_CONFIG, DynamodbStorage
from app.storage.errors import ItemAlreadyExistsError
from tests.app.app_context_test_case import AppContextTestCase


class TestDynamo(AppContextTestCase):
    def setUp(self):
        self._ddb = mock_dynamodb2()
        self._ddb.start()

        super().setUp()

        client = boto3.resource('dynamodb', endpoint_url=None)
        self.ddb = DynamodbStorage(client)

        for config in TABLE_CONFIG.values():
            table_name = current_app.config[config['table_name_key']]
            if table_name:
                client.create_table(  # pylint: disable=no-member
                    TableName=table_name,
                    AttributeDefinitions=[
                        {'AttributeName': config['key_field'], 'AttributeType': 'S'}
                    ],
                    KeySchema=[
                        {'AttributeName': config['key_field'], 'KeyType': 'HASH'}
                    ],
                    ProvisionedThroughput={
                        'ReadCapacityUnits': 1,
                        'WriteCapacityUnits': 1,
                    },
                )

    def tearDown(self):
        super().tearDown()

        self._ddb.stop()

    def test_get_update(self):
        self._assert_item(None)
        self._put_item(1)
        self._assert_item(1)
        self._put_item(2)
        self._assert_item(2)

    def test_dont_overwrite(self):
        self._put_item(1)
        with self.assertRaises(ItemAlreadyExistsError):
            self._put_item(1, overwrite=False)

    def test_delete(self):
        self._put_item(1)
        self._assert_item(1)
        model = QuestionnaireState('someuser', 'data', 1)
        self.ddb.delete(model)
        self._assert_item(None)

    def _assert_item(self, version):
        item = self.ddb.get_by_key(QuestionnaireState, 'someuser')
        actual_version = item.version if item else None
        self.assertEqual(actual_version, version)

    def _put_item(self, version, overwrite=True):
        model = QuestionnaireState('someuser', 'data', version)
        self.ddb.put(model, overwrite)
