import datetime

from dateutil.tz import tzutc
from marshmallow import Schema, fields, post_load, pre_dump


class QuestionnaireState:
    def __init__(self, user_id, state_data, version):
        self.user_id = user_id
        self.state_data = state_data
        self.version = version
        self.created_at = datetime.datetime.now(tz=tzutc())
        self.updated_at = datetime.datetime.now(tz=tzutc())


class EQSession:
    def __init__(self, eq_session_id, user_id, session_data=None):
        self.eq_session_id = eq_session_id
        self.user_id = user_id
        self.session_data = session_data
        self.created_at = datetime.datetime.now(tz=tzutc())
        self.updated_at = datetime.datetime.now(tz=tzutc())


class UsedJtiClaim:
    def __init__(self, jti_claim, used_at, expires):
        self.jti_claim = jti_claim
        self.used_at = used_at
        self.expires = expires


class SubmittedResponse:
    def __init__(self, tx_id, data, valid_until):
        self.tx_id = tx_id
        self.data = data
        self.valid_until = valid_until


# pylint: disable=no-self-use
class Timestamp(fields.Field):
    def _serialize(self, value, attr, obj):
        return int(value.strftime('%s'))

    def _deserialize(self, value, attr, data):
        return datetime.datetime.utcfromtimestamp(value).replace(tzinfo=tzutc())


class PermissiveDateTimeField(fields.DateTime):
    """Overrides the standard DateTime field to allow
    deserializing of values that have already been
    deserialized
    """
    def _deserialize(self, value, attr, data):
        if isinstance(value, datetime.datetime):
            return value
        return super()._deserialize(value, attr, data)


class DateTimeSchemaMixin:
    created_at = PermissiveDateTimeField()
    updated_at = PermissiveDateTimeField()

    @pre_dump
    def set_date(self, data):
        data.updated_at = datetime.datetime.now(tz=tzutc())
        return data


class QuestionnaireStateSchema(Schema, DateTimeSchemaMixin):
    user_id = fields.Str()
    state_data = fields.Str()
    version = fields.Integer()

    @post_load
    def make_model(self, data):
        created_at = data.pop('created_at', None)
        updated_at = data.pop('updated_at', None)
        model = QuestionnaireState(**data)
        model.created_at = created_at
        model.updated_at = updated_at
        return model


class EQSessionSchema(Schema, DateTimeSchemaMixin):
    eq_session_id = fields.Str()
    user_id = fields.Str()
    session_data = fields.Str()

    @post_load
    def make_model(self, data):
        created_at = data.pop('created_at', None)
        updated_at = data.pop('updated_at', None)
        model = EQSession(**data)
        model.created_at = created_at
        model.updated_at = updated_at
        return model


class UsedJtiClaimSchema(Schema):
    jti_claim = fields.Str()
    used_at = fields.DateTime()
    expires = Timestamp()

    @post_load
    def make_model(self, data):
        return UsedJtiClaim(**data)


class SubmittedResponseSchema(Schema):
    tx_id = fields.Str()
    data = fields.Str()
    valid_until = Timestamp()

    @post_load
    def make_model(self, data):
        return SubmittedResponse(**data)
