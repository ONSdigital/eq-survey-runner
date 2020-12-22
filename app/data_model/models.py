import datetime

from flask_sqlalchemy import SQLAlchemy
from structlog import get_logger

from app.data_model import app_models

logger = get_logger()
db = SQLAlchemy()


# pylint: disable=maybe-no-member
class QuestionnaireState(db.Model):
    __tablename__ = 'questionnaire_state'
    user_id = db.Column('userid', db.String, primary_key=True)
    state = db.Column('questionnaire_data', db.String)
    version = db.Column('version', db.Integer)
    collection_exercise_id = db.Column('collection_exercise_id', db.String)
    form_type = db.Column('form_type', db.String)
    ru_ref = db.Column('ru_ref', db.String)
    eq_id = db.Column('eq_id', db.String)
    created_at = db.Column('created_at', db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column('updated_at', db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    def __init__(self, user_id, state, version, collection_exercise_id, form_type, ru_ref, eq_id):
        self.user_id = user_id
        self.state = state
        self.version = version
        self.collection_exercise_id = collection_exercise_id
        self.form_type = form_type
        self.ru_ref = ru_ref
        self.eq_id = eq_id

    def to_app_model(self):
        model = app_models.QuestionnaireState(self.user_id, self.state, self.version, self.collection_exercise_id, self.form_type, self.ru_ref, self.eq_id)
        model.created_at = self.created_at
        model.updated_at = self.updated_at
        return model

    @classmethod
    def from_app_model(cls, model):
        return cls(model.user_id, model.state_data, model.version, model.collection_exercise_id, model.form_type, model.ru_ref, model.eq_id)
