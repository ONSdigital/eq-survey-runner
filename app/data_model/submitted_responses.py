from flask import current_app

from app.storage import dynamo_api


def put_item(item):
    table = _get_table()
    if not table:
        return

    return dynamo_api.put_item(table, item)


def get_item(tx_id):
    table = _get_table()
    if not table:
        return

    return dynamo_api.get_item(table, {'tx_id': tx_id})


def _get_table():
    table_name = current_app.config['EQ_SUBMITTED_RESPONSES_TABLE_NAME']
    return dynamo_api.get_table(table_name)
