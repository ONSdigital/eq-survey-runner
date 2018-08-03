from azure.common import AzureConflictHttpError, AzureMissingResourceHttpError
from flask import current_app

from app.data_model import app_models
from app.storage.errors import ItemAlreadyExistsError


TABLE_CONFIG = {
    app_models.SubmittedResponse: {
        'row_key_field': 'tx_id',
        'table_name_key': 'EQ_SUBMITTED_RESPONSES_TABLE_NAME',
        'schema': app_models.SubmittedResponseSchema,
    },
    app_models.QuestionnaireState: {
        'row_key_field': 'user_id',
        'table_name_key': 'EQ_QUESTIONNAIRE_STATE_TABLE_NAME',
        'schema': app_models.QuestionnaireStateSchema,
    },
    app_models.EQSession: {
        'row_key_field': 'eq_session_id',
        'table_name_key': 'EQ_SESSION_TABLE_NAME',
        'schema': app_models.EQSessionSchema,
    },
    app_models.UsedJtiClaim: {
        'row_key_field': 'jti_claim',
        'table_name_key': 'EQ_USED_JTI_CLAIM_TABLE_NAME',
        'schema': app_models.UsedJtiClaimSchema,
    },
}


def put(model, overwrite):
    config = TABLE_CONFIG[type(model)]
    schema = config['schema'](strict=True)
    table_name = _get_table_name(config)
    row_key_field = config['row_key_field']

    entity, _ = schema.dump(model)
    entity['RowKey'] = row_key = entity[row_key_field]
    entity['PartitionKey'] = _get_partition_key(config, row_key)

    service = get_service()

    if overwrite:
        service.insert_or_replace_entity(table_name, entity)
    else:
        try:
            service.insert_entity(table_name, entity)
        except AzureConflictHttpError as e:
            raise ItemAlreadyExistsError() from e


def get_by_key(model_type, key_value):
    config = TABLE_CONFIG[model_type]
    schema = config['schema'](strict=True)
    table_name = _get_table_name(config)
    partition_key = _get_partition_key(config, key_value)
    
    service = get_service()

    try:
        entity = service.get_entity(table_name, partition_key, key_value)
    except AzureMissingResourceHttpError:
        return
    else:
        model, _ = schema.load(entity)
        return model


def delete(model):
    config = TABLE_CONFIG[type(model)]
    schema = config['schema'](strict=True)
    table_name = _get_table_name(config)
    row_key = getattr(model, config['row_key_field'])

    partition_key = _get_partition_key(config, row_key)

    service = get_service()

    service.delete_entity(table_name, partition_key, row_key)


def get_service():
    return current_app.eq['cosmosdb']


def _get_table_name(config):
    return current_app.config[config['table_name_key']]


def _get_partition_key(config, row_key):
    return 'A'  # TODO: shared strategy?
