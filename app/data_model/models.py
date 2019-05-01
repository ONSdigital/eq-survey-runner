import datetime

from typing import Any

from flask_sqlalchemy import SQLAlchemy
from structlog import get_logger

from app.data_model import app_models

logger = get_logger()
db: Any = SQLAlchemy()


# pylint: disable=maybe-no-member
class QuestionnaireState(db.Model):
    __tablename__ = 'questionnaire_state'
    user_id = db.Column('userid', db.String, primary_key=True)
    state = db.Column('questionnaire_data', db.String)
    version = db.Column('version', db.Integer)
    created_at = db.Column('created_at', db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column('updated_at', db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    def __init__(self, user_id, state, version):
        self.user_id = user_id
        self.state = state
        self.version = version

    def to_app_model(self):
        model = app_models.QuestionnaireState(self.user_id, self.state, self.version)
        model.created_at = self.created_at
        model.updated_at = self.updated_at
        return model

    @classmethod
    def from_app_model(cls, model):
        return cls(model.user_id, model.state_data, model.version)


# pylint: disable=maybe-no-member
class EQSession(db.Model):
    __tablename__ = 'eq_session'
    eq_session_id = db.Column('eq_session_id', db.String, primary_key=True)
    user_id = db.Column('user_id', db.String, primary_key=True)
    session_data = db.Column('session_data', db.String)
    created_at = db.Column('created_at', db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column('updated_at', db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    expires_at = db.Column('expires_at', db.DateTime)

    def __init__(self, eq_session_id, user_id, session_data=None, expires_at=None):
        self.eq_session_id = eq_session_id
        self.user_id = user_id
        self.session_data = session_data
        self.expires_at = expires_at

    def to_app_model(self):
        model = app_models.EQSession(self.eq_session_id, self.user_id, self.session_data, self.expires_at)
        model.created_at = self.created_at
        model.updated_at = self.updated_at
        return model

    @classmethod
    def from_app_model(cls, model):
        return cls(model.eq_session_id, model.user_id, model.session_data, model.expires_at)


# pylint: disable=maybe-no-member
class UsedJtiClaim(db.Model):
    __tablename__ = 'used_jti_claim'
    jti_claim = db.Column('jti_claim', db.String, primary_key=True)
    used_at = db.Column('used_at', db.DateTime)

    def __init__(self, jti_claim, used_at=None):
        self.jti_claim = jti_claim
        self.used_at = used_at or datetime.datetime.now()

    def to_app_model(self):
        return app_models.UsedJtiClaim(self.jti_claim, self.used_at, None)

    @classmethod
    def from_app_model(cls, model):
        return cls(model.jti_claim, model.used_at)
