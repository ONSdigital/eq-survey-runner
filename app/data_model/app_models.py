from datetime import datetime

from dateutil.tz import tzutc
from marshmallow import Schema, fields, post_load, pre_dump


class QuestionnaireState:
    def __init__(self, user_id, state_data, version, collection_exercise_id, form_type, ru_ref, eq_id):
        self.user_id = user_id
        self.ru_ref = ru_ref
        self.collection_exercise_id = collection_exercise_id
        self.eq_id = eq_id
        self.form_type = form_type
        self.state_data = state_data
        self.version = version
        self.created_at = datetime.now(tz=tzutc())
        self.updated_at = datetime.now(tz=tzutc())


class EQSession:
    def __init__(self, eq_session_id, user_id, session_data=None, expires_at=None):
        self.eq_session_id = eq_session_id
        self.user_id = user_id
        self.session_data = session_data
        self.created_at = datetime.now(tz=tzutc())
        self.updated_at = datetime.now(tz=tzutc())
        self.expires_at = expires_at

        # Needed only when data is read from Postgres.
        # The Timestamp() class already handles this when reading from Dynamo.
        # Can be removed once only Dynamo is used.
        if expires_at:
            self.expires_at = expires_at.replace(tzinfo=tzutc())


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
        if value:
            # Timezone aware datetime to timestamp
            return int(value.replace(tzinfo=tzutc()).strftime('%s'))

    def _deserialize(self, value, attr, data):
        if value:
            # Timestamp to timezone aware datetime
            return datetime.utcfromtimestamp(value).replace(tzinfo=tzutc())


class DateTimeSchemaMixin:
    created_at = fields.DateTime()
    updated_at = fields.DateTime()

    @pre_dump
    def set_date(self, data):
        data.updated_at = datetime.now(tz=tzutc())
        return data


class QuestionnaireStateSchema(Schema, DateTimeSchemaMixin):
    user_id = fields.Str()
    collection_exercise_id = fields.Str()
    form_type = fields.Str()
    ru_ref = fields.Str()
    eq_id = fields.Str()
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
    expires_at = Timestamp(allow_none=True)  # To cater in flight data (Should never actually be None)

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
