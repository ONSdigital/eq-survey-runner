import ujson

from botocore.exceptions import ClientError
from flask import current_app

from app.data_model import app_models

TABLE_CONFIG = {
    app_models.SubmittedResponse: {
        'key_field': 'tx_id',
        'db_index': 0,
        'schema': app_models.SubmittedResponseSchema,
    },
    app_models.QuestionnaireState: {
        'key_field': 'user_id',
        'db_index': 1,
        'schema': app_models.QuestionnaireStateSchema,
    },
    app_models.EQSession: {
        'key_field': 'eq_session_id',
        'db_index': 2,
        'schema': app_models.EQSessionSchema,
    },
    app_models.UsedJtiClaim: {
        'key_field': 'jti_claim',
        'db_index': 3,
        'schema': app_models.UsedJtiClaimSchema,
    },
}


def put(model, overwrite):
    config = TABLE_CONFIG[type(model)]
    schema = config['schema'](strict=True)
    key = getattr(model, config['key_field'])

    item, _ = schema.dump(model)
    if overwrite:
        get_db(config).set(key, ujson.dumps(item))
    else:
        get_db(config).setnx(key, ujson.dumps(item))


def get_by_key(model_type, key_value):
    config = TABLE_CONFIG[model_type]
    schema = config['schema'](strict=True)

    item = get_db(config).get(key_value)

    if item:
        model, _ = schema.load(ujson.loads(item))
        return model


def delete(model):
    config = TABLE_CONFIG[type(model)]
    key = getattr(model, config['key_field'])

    get_db(config).delete(key)


def get_db(config):
    return current_app.eq['redis'][config['db_index']]
