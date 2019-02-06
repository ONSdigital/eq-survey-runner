from structlog import get_logger

from botocore.exceptions import ClientError
from flask import current_app as app
from sqlalchemy.exc import IntegrityError

from app.data_model import models, app_models
from app.storage import dynamo_api

logger = get_logger()


TABLE_CONFIG = {
    app_models.SubmittedResponse: {
        'table_name_key': 'EQ_SUBMITTED_RESPONSES_TABLE_NAME',
        'key_field': 'tx_id',
        'schema': app_models.SubmittedResponseSchema,
    },
    app_models.QuestionnaireState: {
        'table_name_key': 'EQ_QUESTIONNAIRE_STATE_TABLE_NAME',
        'dynamo_read_key': 'EQ_QUESTIONNAIRE_STATE_DYNAMO_READ',
        'dynamo_write_key': 'EQ_QUESTIONNAIRE_STATE_DYNAMO_WRITE',
        'key_field': 'user_id',
        'schema': app_models.QuestionnaireStateSchema,
        'sql_model': models.QuestionnaireState,
    },
    app_models.EQSession: {
        'table_name_key': 'EQ_SESSION_TABLE_NAME',
        'key_field': 'eq_session_id',
        'schema': app_models.EQSessionSchema,
    },
    app_models.UsedJtiClaim: {
        'table_name_key': 'EQ_USED_JTI_CLAIM_TABLE_NAME',
        'key_field': 'jti_claim',
        'schema': app_models.UsedJtiClaimSchema,
    },
}


class ItemAlreadyExistsError(Exception):
    pass


def get_by_key(model_type, key_value):
    """Gets a given model by its key

    :param model: the type of the app model to fetch
    :param key_value: the value of the model's key
    """

    config = TABLE_CONFIG[model_type]
    schema = config['schema'](strict=True)
    key_field = config['key_field']

    model = None
    key = {key_field: key_value}

    if is_dynamodb_read_enabled(config):
        # find in dynamo
        table_name = get_table_name(config)
        returned_data = dynamo_api.get_item(table_name, key)
        if returned_data:
            model, _ = schema.load(returned_data)
            setattr(model, '_use_dynamo', True)
        else:
            logger.debug(
                'could not find item in dynamodb',
                table_name=table_name,
                key_value=key_value)

    if not model:
        # find in RDS
        if 'sql_model' in config:
            returned_data = config['sql_model'].query.filter_by(**key).first()
            if returned_data:
                model = returned_data.to_app_model()
                setattr(model, '_use_dynamo', False)

    return model


def put(model, overwrite=True):
    """Inserts or updates the given app model

    :param model: the app model to be saved
    :param overwrite: if true then the object may overwrite an existing object
        with the same ID. if not a `ItemAlreadyExistsError` will be raised
    """
    config = TABLE_CONFIG[type(model)]
    schema = config['schema'](strict=True)
    key_field = config['key_field']

    if getattr(model, '_use_dynamo', is_dynamodb_write_enabled(config)):
        item, _ = schema.dump(model)

        table_name = get_table_name(config)
        try:
            dynamo_api.put_item(table_name, key_field, item, overwrite=overwrite)
        except ClientError as e:
            if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
                raise ItemAlreadyExistsError() from e

            raise
    else:
        if 'sql_model' in config:
            sql_model = config['sql_model'].from_app_model(model)

            try:
                # pylint: disable=maybe-no-member
                if overwrite:
                    models.db.session.merge(sql_model)
                else:
                    models.db.session.add(sql_model)

                models.db.session.commit()
            except IntegrityError as e:
                raise ItemAlreadyExistsError() from e


def delete(model):
    """Deletes the given app model

    :param model: the app model to be deleted
    """
    config = TABLE_CONFIG[type(model)]
    key_field = config['key_field']
    key = {key_field: getattr(model, key_field)}

    if getattr(model, '_use_dynamo', is_dynamodb_write_enabled(config)):
        table_name = get_table_name(config)
        dynamo_api.delete_item(table_name, key)
    else:
        if 'sql_model' in config:
            sql_model = config['sql_model'].from_app_model(model)

            # pylint: disable=maybe-no-member
            sql_model = models.db.session.merge(sql_model)
            models.db.session.delete(sql_model)
            models.db.session.commit()


def get_table_name(config):
    return app.config[config['table_name_key']]


def is_dynamodb_read_enabled(config):
    # If we do not have a config key, assume dynamo is enabled
    if 'dynamo_read_key' not in config:
        return True

    return app.config[config['dynamo_read_key']]


def is_dynamodb_write_enabled(config):
    # Only allow writing if we also allow reading
    if not is_dynamodb_read_enabled(config):
        return False

    # If we do not have a config key, assume dynamo is enabled
    if 'dynamo_write_key' not in config:
        return True

    return app.config[config['dynamo_write_key']]
