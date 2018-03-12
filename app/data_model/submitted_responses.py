from datetime import datetime
from botocore.exceptions import BotoCoreError, ConnectionError as BotoConnectionError
from flask import current_app
from structlog import get_logger

from app.globals import get_dynamodb


logger = get_logger()


def put_item(item):
    """Insert an item to table"""
    table = _get_table()
    if not table:
        return

    if item and item['valid_until']:
        item['valid_until'] = int(item['valid_until'].strftime('%s'))  # convert to epoch

    try:
        response = table.put_item(Item=item)['ResponseMetadata']['HTTPStatusCode']
        return response == 200

    except (BotoCoreError, BotoConnectionError, ConnectionError):
        logger.warn('Could not load data into DynamoDB')
        return False


def get_item(tx_id):
    """ Get an item given its key """
    table = _get_table()
    if not table:
        return

    try:
        response = table.get_item(Key={'tx_id': tx_id})
        item = response.get('Item', None)
        if item:
            item['valid_until'] = datetime.utcfromtimestamp(item['valid_until'])
        return item

    except (BotoCoreError, BotoConnectionError, ConnectionError):
        logger.warn('Could not get data from DynamoDB')
        return None


def _get_table():
    dynamodb = get_dynamodb()
    table_name = current_app.config['EQ_SUBMITTED_RESPONSES_TABLE_NAME']
    if dynamodb and table_name:
        return dynamodb.Table(table_name)
