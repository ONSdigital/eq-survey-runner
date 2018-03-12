import unittest
from datetime import datetime, timedelta
import mock

from botocore.exceptions import BotoCoreError, ConnectionError as BotoConnectionError
from app.data_model import submitted_responses


class SubmittedResponsesTest(unittest.TestCase):

    def setUp(self):
        valid_until = datetime.utcnow() + timedelta(seconds=10)

        self.item = {
            'tx_id': 'test_tx_id',
            'data': 'test_data',
            'valid_until': valid_until
        }

        self.table = mock.Mock()
        self.table_patcher = mock.patch(
            'app.data_model.submitted_responses._get_table',
            return_value=self.table)
        self.table_patcher.start()

    def tearDown(self):
        super().tearDown()

        self.table_patcher.stop()

    def test_put_item(self):
        self.table.put_item.return_value = {'ResponseMetadata': {'HTTPStatusCode': 200}}

        valid_until = self.item['valid_until']
        response = submitted_responses.put_item(self.item)

        self.assertTrue(response)

        item = self.table.put_item.call_args[1]['Item']
        self.assertEqual(item.get('tx_id'), self.item['tx_id'])
        self.assertEqual(item.get('data'), self.item['data'])
        self.assertEqual(item.get('valid_until'), int(valid_until.strftime('%s')))

    def test_get_item(self):
        item_in = self.item
        item_in['valid_until'] = int(item_in['valid_until'].strftime('%s'))

        self.table.get_item.return_value = {'Item': item_in}
        item_out = submitted_responses.get_item('test_tx_id')

        self.assertEqual(item_out.get('tx_id'), self.item['tx_id'])
        self.assertEqual(item_out.get('data'), self.item['data'])
        self.assertEqual(item_out.get('valid_until'), self.item['valid_until'])

    def test_exceptions(self):
        self.table.put_item.side_effect = BotoCoreError
        response = submitted_responses.put_item(self.item)
        self.assertFalse(response)

        self.table.get_item.side_effect = BotoConnectionError
        item = submitted_responses.get_item('test_tx_id')
        self.assertIsNone(item)

    @mock.patch('app.data_model.submitted_responses._get_table', return_value=None)
    def test_no_table(self, _get_table):
        self.assertFalse(submitted_responses.put_item(self.item))
        self.assertFalse(submitted_responses.get_item('test_tx_id'))


class SubmittedResponsesGetTableTest(unittest.TestCase):
    @mock.patch('app.data_model.submitted_responses.get_dynamodb')
    @mock.patch('app.data_model.submitted_responses.current_app', **{'config.new': {'EQ_SUBMITTED_RESPONSES_TABLE_NAME': 'foo'}})
    def test_get_table(self, get_dynamodb, current_app): # pylint: disable=unused-argument
        self.assertTrue(submitted_responses._get_table())  # pylint: disable=protected-access
