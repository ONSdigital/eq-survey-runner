from flask import current_app
from structlog import get_logger

logger = get_logger()


def put_item(table_name, key_field, item, overwrite=True):
    """Insert an item into table"""
    table = get_table(table_name)

    put_kwargs = {'Item': item}
    if not overwrite:
        put_kwargs['ConditionExpression'] = 'attribute_not_exists({key_field})'.format(
            key_field=key_field)

    response = table.put_item(**put_kwargs)['ResponseMetadata']['HTTPStatusCode']
    return response == 200


def get_item(table_name, key):
    """ Get an item given its key """
    table = get_table(table_name)

    response = table.get_item(Key=key, ConsistentRead=True)
    item = response.get('Item', None)

    return item


def delete_item(table_name, key):
    """Deletes an item by its key
    """
    table = get_table(table_name)

    response = table.delete_item(Key=key)
    item = response.get('Item', None)
    return item


def get_table(table_name):
    return current_app.eq['dynamodb'].Table(table_name)
