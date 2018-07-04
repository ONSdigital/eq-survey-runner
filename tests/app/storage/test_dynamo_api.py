from botocore.exceptions import ClientError
from flask import current_app

from app.storage import dynamo_api
from tests.app.app_context_test_case import AppContextTestCase


KEY = {'user_id': 'someuser'}


class TestDynamoApi(AppContextTestCase):

    def test_get_update(self):
        self._assert_item(None)
        _put_item(1)
        self._assert_item(1)
        _put_item(2)
        self._assert_item(2)

    def test_dont_overwrite(self):
        _put_item(1)
        with self.assertRaises(ClientError):
            _put_item(1, overwrite=False)

    def test_delete(self):
        _put_item(1)
        self._assert_item(1)
        table_name = current_app.config['EQ_QUESTIONNAIRE_STATE_TABLE_NAME']
        dynamo_api.delete_item(table_name, KEY)
        self._assert_item(None)

    def _assert_item(self, version):
        table_name = current_app.config['EQ_QUESTIONNAIRE_STATE_TABLE_NAME']
        item = dynamo_api.get_item(table_name, KEY)
        actual_version = item['version'] if item else None
        self.assertEqual(actual_version, version)


def _put_item(version, overwrite=True):
    table_name = current_app.config['EQ_QUESTIONNAIRE_STATE_TABLE_NAME']
    dynamo_api.put_item(table_name, 'user_id', {'user_id': KEY['user_id'], 'version': version}, overwrite)
