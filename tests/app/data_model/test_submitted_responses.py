import unittest

from datetime import datetime, timedelta
from mock import Mock
from botocore.exceptions import BotoCoreError, ConnectionError as BotoConnectionError
from app.data_model.submitted_responses import SubmittedResponses


class SubmittedResponsesTest(unittest.TestCase):

    def setUp(self):
        self.table = Mock()
        self.submitted_responses = SubmittedResponses(self.table)

        valid_until = datetime.utcnow() + timedelta(seconds=10)

        self.item = {
            'tx_id': 'test_tx_id',
            'data': 'test_data',
            'valid_until': valid_until
        }


    def test_put_item(self):
        self.table.put_item = Mock(return_value={'ResponseMetadata': {'HTTPStatusCode': 200}})
        valid_until = self.item['valid_until']
        response = self.submitted_responses.put_item(self.item)

        self.assertTrue(response)
        item = self.table.put_item.call_args[1]['Item']
        self.assertEqual(item.get('tx_id'), self.item['tx_id'])
        self.assertEqual(item.get('data'), self.item['data'])
        self.assertEqual(item.get('valid_until'), int(valid_until.strftime('%s')))


    def test_get_item(self):
        item_in = self.item
        item_in['valid_until'] = int(item_in['valid_until'].strftime('%s'))

        self.table.get_item = Mock(return_value={'Item': item_in})
        item_out = self.submitted_responses.get_item('test_tx_id')

        self.assertEqual(item_out.get('tx_id'), self.item['tx_id'])
        self.assertEqual(item_out.get('data'), self.item['data'])
        self.assertEqual(item_out.get('valid_until'), self.item['valid_until'])


    def test_exceptions(self):
        self.table.put_item = Mock(side_effect=BotoCoreError)
        response = self.submitted_responses.put_item(self.item)
        self.assertFalse(response)

        self.table.get_item = Mock(side_effect=BotoConnectionError)
        item = self.submitted_responses.get_item('test_tx_id')
        self.assertIsNone(item)
