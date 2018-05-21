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


def delete_all(table):
    """Deletes all items from a table
    """
    if isinstance(table, str):
        table = get_table(table)

    keys = [k['AttributeName'] for k in table.key_schema]
    response = table.scan()

    with table.batch_writer() as batch:
        for item in response['Items']:
            key_dict = {k: item[k] for k in keys}
            batch.delete_item(Key=key_dict)


def get_table(table_name):
    dynamodb = get_dynamodb()
    if dynamodb and table_name:
        return dynamodb.Table(table_name)
