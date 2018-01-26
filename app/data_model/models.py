import datetime

from flask_sqlalchemy import SQLAlchemy
from structlog import get_logger

logger = get_logger()
db = SQLAlchemy()


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


# pylint: disable=maybe-no-member
class EQSession(db.Model):
    __tablename__ = 'eq_session'
    eq_session_id = db.Column('eq_session_id', db.String, primary_key=True)
    user_id = db.Column('user_id', db.String, primary_key=True)
    session_data = db.Column('session_data', db.String)
    created_at = db.Column('created_at', db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column('updated_at', db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    def __init__(self, eq_session_id, user_id):
        self.eq_session_id = eq_session_id
        self.user_id = user_id
        self.session_data = None


# pylint: disable=maybe-no-member
class UsedJtiClaim(db.Model):
    __tablename__ = 'used_jti_claim'
    jti_claim = db.Column('jti_claim', db.String, primary_key=True)
    used_at = db.Column('used_at', db.DateTime)

    def __init__(self, jti_claim):
        self.jti_claim = jti_claim
        self.used_at = datetime.datetime.now()
