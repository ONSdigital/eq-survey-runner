from structlog import get_logger

from flask import current_app as app
from app.data_model import models, db_models
from app.globals import is_dynamodb_enabled
from app.storage import dynamo_api

logger = get_logger()


TABLE_CONFIG = {
    db_models.QuestionnaireState: {
        'table_name_key': 'EQ_QUESTIONNAIRE_STATE_TABLE_NAME',
        'key_field': 'user_id',
        'schema': db_models.QuestionnaireStateSchema,
        'sql_model': models.QuestionnaireState,
    },
    db_models.EQSession: {
        'table_name_key': 'EQ_SESSION_TABLE_NAME',
        'key_field': 'eq_session_id',
        'schema': db_models.EQSessionSchema,
        'sql_model': models.EQSession,
    },
    db_models.UsedJtiClaim: {
        'table_name_key': 'EQ_USED_JTI_CLAIM_TABLE_NAME',
        'key_field': 'jti_claim',
        'schema': db_models.UsedJtiClaimSchema,
        'sql_model': models.UsedJtiClaim,
    },
    db_models.SubmittedResponse: {
        'table_name_key': 'EQ_SUBMITTED_RESPONSES_TABLE_NAME',
        'key_field': 'tx_id',
        'schema': db_models.SubmittedResponseSchema,
        'sql_model': None  # submitted responses aren't stored in RDS
    }
}


def get_by_key(model_type, key_value, force_rds=False):
    """Gets a given model by its key

    :param model: the type of the app model to fetch
    :param key_value: the value of the model's key
    :param force_rds: if true will forcibly try and get object from RDS
    """
    config = TABLE_CONFIG[model_type]
    schema = config['schema'](strict=True)
    key_name = config['key_field']

    model = None
    key = {key_name: key_value}

    if is_dynamodb_enabled() and not force_rds:
        # find in dynamo
        table_name = _get_table_name(config)
        returned_data = dynamo_api.get_item(table_name, key)
        if returned_data:
            model, _ = schema.load(returned_data)
        else:
            logger.debug(
                'could not find item in dynamodb',
                table_name=table_name,
                key_value=key_value)

    if not model:
        # find in RDS
        sql_model = config['sql_model']
        if not sql_model:
            return

        returned_data = sql_model.query.filter_by(**key).first()
        if returned_data:
            model, _ = schema.load_object(returned_data)
            model._use_rds = True

    return model


def put(model, overwrite=True, force_rds=False):
    """Inserts or updates the given app model

    :param model: the app model to be saved
    :param overwrite: if true then the object may overwrite an existing object
        with the same ID. if not a `boto3.ClientError` will be raised
    :param force_rds: if true will forcibly try and save object to RDS
    """
    config = TABLE_CONFIG[type(model)]
    schema = config['schema'](strict=True)

    if (
            force_rds or
            getattr(model, '_use_rds', False) or
            not is_dynamodb_enabled()):
        if config['sql_model']:
            sql_model = config['sql_model'].from_new_model(model)

            if overwrite:
                models.db.session.merge(sql_model)
            else:
                models.db.session.add(sql_model)
            models.db.session.commit()
    else:
        item, _ = schema.dump(model)

        # TODO: update updated_at time
        # TODO: set created_at time
        table_name = _get_table_name(config)
        dynamo_api.put_item(
            table_name,
            item,
            overwrite=overwrite)


def delete(model, force_rds=False):
    """Deletes the given app model

    :param model: the app model to be deleted
    :param force_rds: if true will forcibly try and delete object from RDS
    """
    config = TABLE_CONFIG[type(model)]
    key_name = config['key_field']
    key = {key_name: getattr(model, key_name)}

    if (
            force_rds or
            getattr(model, '_use_rds', False) or
            not is_dynamodb_enabled()):
        if config['sql_model']:
            sql_model = config['sql_model'].from_new_model(model)
            sql_model = models.db.session.merge(sql_model)
            models.db.session.delete(sql_model)
            models.db.session.commit()
    else:
        table_name = _get_table_name(config)
        dynamo_api.delete_item(table_name, key)


def flush_all_data():
    """Deletes all data in DynamoDB
    """
    for config in TABLE_CONFIG.values():
        table_name = _get_table_name(config)
        dynamo_api.delete_all(table_name)


def _get_table_name(config):
    return app.config[config['table_name_key']]
