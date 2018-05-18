from datetime import datetime
from botocore.exceptions import BotoCoreError, ConnectionError as BotoConnectionError
from structlog import get_logger

from app.globals import get_dynamodb

logger = get_logger()


def put_item(table, item, overwrite=True):
    """Insert an item to table"""
    if isinstance(table, str):
        table = get_table(table)

    put_kwargs = {'Item': item}
    if not overwrite:
        first_key = next(iter(item.keys()))
        put_kwargs['ConditionExpression'] = 'attribute_not_exists({first_key})'.format(
                first_key=first_key)

    response = table.put_item(
        **put_kwargs)['ResponseMetadata']['HTTPStatusCode']
    return response == 200


def get_item(table, key):
    """ Get an item given its key """
    if isinstance(table, str):
        table = get_table(table)

    response = table.get_item(Key=key)
    item = response.get('Item', None)
    return item


def delete_item(table, key):
    """Deletes an item by its key
    """
    if isinstance(table, str):
        table = get_table(table)

    response = table.delete_item(Key=key)
    item = response.get('Item', None)
    return item


def get_table(table_name):
    dynamodb = get_dynamodb()
    if dynamodb and table_name:
        return dynamodb.Table(table_name)
