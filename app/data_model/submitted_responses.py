from datetime import datetime
from botocore.exceptions import BotoCoreError, ConnectionError as BotoConnectionError
from structlog import get_logger

logger = get_logger()


class SubmittedResponses(object):

    def __init__(self, table):
        self.table = table

    def put_item(self, item):
        """Insert an item to table"""
        if item and item['valid_until']:
            item['valid_until'] = int(item['valid_until'].strftime('%s'))  # convert to epoch

        try:
            response = self.table.put_item(Item=item)['ResponseMetadata']['HTTPStatusCode']
            return response == 200

        except (BotoCoreError, BotoConnectionError, ConnectionError):
            logger.warn('Could not load data into DynamoDB')
            return False

    def get_item(self, tx_id):
        """ Get an item given its key """
        try:
            response = self.table.get_item(Key={'tx_id': tx_id})
            item = response.get('Item', None)
            if item:
                item['valid_until'] = datetime.utcfromtimestamp(item['valid_until'])
            return item

        except (BotoCoreError, BotoConnectionError, ConnectionError):
            logger.warn('Could not get data from DynamoDB')
            return None
