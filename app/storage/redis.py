import json
from datetime import datetime
from dateutil.tz import tzutc

from app.data_model import app_models
from app.storage.errors import ItemAlreadyExistsError

TABLE_CONFIG = {
    app_models.SubmittedResponse: {
        'key_field': 'tx_id',
        'name_key_prefix': 'SUBMITTED_RESPONSES_',
        'schema': app_models.SubmittedResponseSchema,
        'expire_field': 'valid_until',
    },
    app_models.EQSession: {
        'key_field': 'eq_session_id',
        'name_key_prefix': 'SESSION_',
        'schema': app_models.EQSessionSchema,
        'expire_field': 'expires_at'
    },
    app_models.UsedJtiClaim: {
        'key_field': 'jti_claim',
        'name_key_prefix': 'JTI_',
        'schema': app_models.UsedJtiClaimSchema,
        'expire_field': 'expires'
    },
}


class RedisStorage:

    def __init__(self, redis):
        self.redis = redis

    def put_jti(self, jti):
        record_created = self.redis.set(name=jti.jti_claim,
                                        value=int(jti.used_at.timestamp()),
                                        ex=int((jti.expires - jti.used_at).total_seconds()),
                                        nx=True)

        if not record_created:
            raise ItemAlreadyExistsError()

    def put(self, model, overwrite=True):
        if not overwrite:
            raise NotImplementedError('Unique key checking not supported')

        config = TABLE_CONFIG[type(model)]

        schema = config['schema'](strict=True)
        item, _ = schema.dump(model)

        key_value = getattr(model, config['key_field'])
        name_key_prefix = config['name_key_prefix']

        expires_at = getattr(model, config['expire_field'])
        now = datetime.now(tz=tzutc())

        record_created = self.redis.set(name="{}{}".format(name_key_prefix, key_value),
                                        value=json.dumps(item),
                                        ex=int((expires_at - now).total_seconds()),
                                        nx=(not overwrite))

        if not overwrite and not record_created:
            raise ItemAlreadyExistsError()

    def get_by_key(self, model_type, key_value):
        config = TABLE_CONFIG[model_type]

        name_key_prefix = config['name_key_prefix']

        schema = config['schema'](strict=True)

        item = self.redis.get("{}{}".format(name_key_prefix, key_value))

        if item:
            model, _ = schema.load(json.loads(item))
            return model

    def delete(self, model):
        config = TABLE_CONFIG[type(model)]

        key_value = getattr(model, config['key_field'])
        name_key_prefix = config['name_key_prefix']

        return self.redis.delete("{}{}".format(name_key_prefix, key_value))
