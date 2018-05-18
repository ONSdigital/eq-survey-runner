from structlog import get_logger

from app import settings
from app.data_model import models, db_models
from app.globals import is_dynamodb_enabled
from app.storage import dynamo_api

logger = get_logger()


TABLE_CONFIG = {
    db_models.QuestionnaireState: {
        'table_name': settings.EQ_QUESTIONNAIRE_STATE_TABLE_NAME,
        'key_field': 'user_id',
        'schema': db_models.QuestionnaireStateSchema,
        'sql_model': models.QuestionnaireState,
    },
    db_models.EQSession: {
        'table_name': settings.EQ_SESSION_TABLE_NAME,
        'key_field': 'eq_session_id',
        'schema': db_models.EQSessionSchema,
        'sql_model': models.EQSession,
    },
    db_models.UsedJtiClaim: {
        'table_name': settings.EQ_USED_JTI_CLAIM_TABLE_NAME,
        'key_field': 'jti_claim',
        'schema': db_models.UsedJtiClaimSchema,
        'sql_model': models.UsedJtiClaim,
    },
    db_models.SubmittedResponse: {
        'table_name': settings.EQ_SUBMITTED_RESPONSES_TABLE_NAME,
        'key_field': 'tx_id',
        'schema': db_models.SubmittedResponseSchema,
        'sql_model': None  # submitted responses aren't stored in RDS
    }
}


def get_by_key(model_type, key_value, force_rds=False):
    config = TABLE_CONFIG[model_type]
    schema = config['schema'](strict=True)
    key_name = config['key_field']

    model = None
    key = {key_name: key_value}

    if is_dynamodb_enabled() and not force_rds:
        # find in dynamo
        table_name = config['table_name']
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


def put(model, force_rds=False):
    config = TABLE_CONFIG[type(model)]
    schema = config['schema'](strict=True)

    if (
            force_rds or
            getattr(model, '_use_rds', False) or
            not is_dynamodb_enabled()):
        if config['sql_model']:
            sql_model = config['sql_model'].from_new_model(model)
            sql_model = models.db.session.merge(sql_model)
            models.db.session.commit()
    else:
        item, _ = schema.dump(model)

        # TODO: update updated_at time
        # TODO: set created_at time
        dynamo_api.put_item(config['table_name'], item)


def delete(model, force_rds=False):
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
        dynamo_api.delete_item(config['table_name'], key)
