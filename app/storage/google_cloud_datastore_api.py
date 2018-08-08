from google.cloud import datastore
from flask import current_app

from app.data_model import app_models
from app.storage.errors import ItemAlreadyExistsError


TABLE_CONFIG = {
    app_models.SubmittedResponse: {
        'key_field': 'tx_id',
        'table_name_key': 'EQ_SUBMITTED_RESPONSES_TABLE_NAME',
        'schema': app_models.SubmittedResponseSchema,
    },
    app_models.QuestionnaireState: {
        'key_field': 'user_id',
        'table_name_key': 'EQ_QUESTIONNAIRE_STATE_TABLE_NAME',
        'schema': app_models.QuestionnaireStateSchema,
    },
    app_models.EQSession: {
        'key_field': 'eq_session_id',
        'table_name_key': 'EQ_SESSION_TABLE_NAME',
        'schema': app_models.EQSessionSchema,
    },
    app_models.UsedJtiClaim: {
        'key_field': 'jti_claim',
        'table_name_key': 'EQ_USED_JTI_CLAIM_TABLE_NAME',
        'schema': app_models.UsedJtiClaimSchema,
    },
}


def put(model, overwrite):
    ds = get_client()
    config = TABLE_CONFIG[type(model)]
    schema = config['schema'](strict=True)
    table_name = current_app.config[config['table_name_key']]
    key_field = config['key_field']
    key = ds.Key(table_name, getattr(model, key_field))

    item, _ = schema.dump(model)
    entity = datastore.Entity(key=key)
    entity.update(item)

    if overwrite:
        ds.upsert(entity)
    else:
        ds.insert(entity)  # FIXME translate exception to ItemAlreadyExistsError


def get_by_key(model_type, key_value):
    ds = get_client()
    config = TABLE_CONFIG[model_type]
    schema = config['schema'](strict=True)
    table_name = current_app.config[config['table_name_key']]
    key_field = config['key_field']
    key = ds.Key(table_name, key_value)

    entity = ds.get(key)

    if entity:
        entity = entity.pop()
        entity[key_field] = entity.key.id
        model, _ = schema.load(entity)
        return model


def delete(model):
    ds = get_client()
    config = TABLE_CONFIG[type(model)]
    table_name = current_app.config[config['table_name_key']]
    key_field = config['key_field']
    key = ds.Key(table_name, getattr(model, key_field))

    ds.delete(key)


def get_client():
    return datastore.Client(current_app.config['PROJECT_ID'])  # FIXME configure client properly
