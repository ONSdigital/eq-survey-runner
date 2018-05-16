from datetime import datetime
from botocore.exceptions import BotoCoreError, ConnectionError as BotoConnectionError
from structlog import get_logger

from app.globals import get_dynamodb

logger = get_logger()


def put_item(table, item):
    """Insert an item to table"""
    if item and item['valid_until']:
        item['valid_until'] = int(
            item['valid_until'].strftime('%s'))  # convert to epoch

    try:
        response = table.put_item(
            Item=item)['ResponseMetadata']['HTTPStatusCode']
        return response == 200

    except (BotoCoreError, BotoConnectionError, ConnectionError):
        logger.warn('Could not load data into DynamoDB')
        return False


def get_item(table, key):
    """ Get an item given its key """
    assert isinstance(key, dict)
    try:
        response = table.get_item(Key=key)
        item = response.get('Item', None)
        if item:
            item['valid_until'] = datetime.utcfromtimestamp(
                item['valid_until'])
        return item

    except (BotoCoreError, BotoConnectionError, ConnectionError):
        logger.warn('Could not get data from DynamoDB')
        return None


def get_table(table_name):
    dynamodb = get_dynamodb()
    if dynamodb and table_name:
        return dynamodb.Table(table_name)
