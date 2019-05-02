from flask import current_app
from gcloud.aio import datastore
from structlog import get_logger

from app.data_model import app_models

import os

logger = get_logger()

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


class AsyncDatastoreStorage:

    def __init__(self, client):
        self.client = client
        self.project = os.getenv('EQ_DATASTORE_PROJECT_ID')

    async def put(self, model, overwrite=True):
        logger.info("Async PUT")
        if not overwrite:
            raise NotImplementedError('Unique key checking not supported')

        config = TABLE_CONFIG[type(model)]
        schema = config['schema'](strict=True)
        item, _ = schema.dump(model)

        key_value = getattr(model, config['key_field'])
        table_name = current_app.config[config['table_name_key']]
        key = datastore.Key(self.project, [datastore.PathElement(kind=table_name, name=key_value)])

        await self.client.upsert(key, item)

    async def get_by_key(self, model_type, key_value):
        logger.info("Async GET")
        config = TABLE_CONFIG[model_type]
        schema = config['schema'](strict=True)

        table_name = current_app.config[config['table_name_key']]
        key = datastore.Key(self.project, [datastore.PathElement(kind=table_name, name=key_value)])

        results = await self.client.lookup([key])

        if results['found']:
            item = results['found'][0]
            model, _ = schema.load(item.entity.properties)
            return model

    async def delete(self, model):
        logger.info("Async DELETE")
        config = TABLE_CONFIG[type(model)]

        key_value = getattr(model, config['key_field'])
        table_name = current_app.config[config['table_name_key']]
        key = datastore.Key(self.project, [datastore.PathElement(kind=table_name, name=key_value)])

        return await self.client.delete(key)
