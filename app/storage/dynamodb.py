from botocore.exceptions import ClientError
from flask import current_app

from app.data_model import app_models
from app.storage.errors import ItemAlreadyExistsError
from app.decorators.opencensus_decorators import capture_trace

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


class DynamodbStorage:

    def __init__(self, dynamodb):
        self.dynamodb = dynamodb

    @capture_trace
    def put(self, model, overwrite=True):
        config = TABLE_CONFIG[type(model)]
        schema = config['schema'](strict=True)
        table = self.get_table(config)
        key_field = config['key_field']

        item, _ = schema.dump(model)
        put_kwargs = {'Item': item}
        if not overwrite:
            put_kwargs['ConditionExpression'] = 'attribute_not_exists({key_field})'.format(key_field=key_field)

        try:
            response = table.put_item(**put_kwargs)['ResponseMetadata']['HTTPStatusCode']
            return response == 200
        except ClientError as e:
            if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
                raise ItemAlreadyExistsError() from e

            raise  # pragma: no cover

    @capture_trace
    def get_by_key(self, model_type, key_value):
        config = TABLE_CONFIG[model_type]
        schema = config['schema'](strict=True)
        table = self.get_table(config)
        key = {config['key_field']: key_value}

        response = table.get_item(Key=key, ConsistentRead=True)
        item = response.get('Item', None)

        if item:
            model, _ = schema.load(item)
            return model

    @capture_trace
    def delete(self, model):
        config = TABLE_CONFIG[type(model)]
        table = self.get_table(config)
        key_field = config['key_field']
        key = {key_field: getattr(model, key_field)}

        response = table.delete_item(Key=key)
        item = response.get('Item', None)
        return item

    def get_table(self, config):
        table_name = current_app.config[config['table_name_key']]
        return self.dynamodb.Table(table_name)
