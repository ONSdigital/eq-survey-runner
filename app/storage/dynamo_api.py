from datetime import datetime
from botocore.exceptions import BotoCoreError, ConnectionError as BotoConnectionError
from structlog import get_logger

from app.globals import get_dynamodb

logger = get_logger()


def put_item(table, item, fail_silently=False):
    """Insert an item to table"""
    if isinstance(table, str):
        table = get_table(table)

    if item and item.get('valid_until'):
        item['valid_until'] = int(
            item['valid_until'].strftime('%s'))  # convert to epoch

    try:
        response = table.put_item(
            Item=item)['ResponseMetadata']['HTTPStatusCode']
        return response == 200

    except (BotoCoreError, BotoConnectionError, ConnectionError):
        logger.warn('Could not load data into DynamoDB')
        if fail_silently:
            return False
        raise


def get_item(table, key, fail_silently=False):
    """ Get an item given its key """
    if isinstance(table, str):
        table = get_table(table)

    try:
        response = table.get_item(Key=key)
        item = response.get('Item', None)
        if item and item.get('valid_until'):
            item['valid_until'] = datetime.utcfromtimestamp(
                item['valid_until'])
        return item

    except (BotoCoreError, BotoConnectionError, ConnectionError):
        logger.warn('Could not get data from DynamoDB')
        if fail_silently:
            return None
        raise


def get_table(table_name):
    dynamodb = get_dynamodb()
    if dynamodb and table_name:
        return dynamodb.Table(table_name)
