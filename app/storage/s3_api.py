import ujson

from botocore.exceptions import ClientError
from flask import current_app

from app.data_model import app_models

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
    config = TABLE_CONFIG[type(model)]
    schema = config['schema'](strict=True)
    table_name = current_app.config[config['table_name_key']]
    key = getattr(model, config['key_field'])

    item, _ = schema.dump(model)
    get_s3_client().put_object(Bucket=table_name, Key=key, Body=ujson.dumps(item))


def get_by_key(model_type, key_value):
    config = TABLE_CONFIG[model_type]
    schema = config['schema'](strict=True)
    table_name = current_app.config[config['table_name_key']]

    try:
        response = get_s3_client().get_object(Bucket=table_name, Key=key_value)
        item = response.get('Body', None)
        model, _ = schema.load(ujson.loads(item.read()))
        return model
    except ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchKey':
            return None

        raise e


def delete(model):
    config = TABLE_CONFIG[type(model)]
    table_name = current_app.config[config['table_name_key']]
    key = getattr(model, config['key_field'])

    get_s3_client().delete_object(Bucket=table_name, Key=key)


def get_s3_client():
    return current_app.eq['s3']
