from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, create_engine
from app.storage.abstract_server_storage import AbstractServerStorage
from app import settings
import logging
import json

logger = logging.getLogger(__name__)

engine = create_engine(settings.EQ_SERVER_SIDE_STORAGE_DATABASE_URL, convert_unicode=True)

Base = declarative_base()

db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base.query = db_session.query_property()


class QuestionnaireState(Base):
    __tablename__ = 'questionnaire_state'
    user_id = Column('userid', String, primary_key=True)
    state = Column('questionnaire_data', String)

    def __init__(self, user_id, data):
        self.user_id = user_id
        self.state = json.dumps(data)

    def set_data(self, data):
        logger.debug("Setting data for questionnaire state %s", data)
        self.state = json.dumps(data)

    def get_data(self):
        data = json.loads(self.state)
        logger.debug("Loading questionnaire state %s", data)
        return data

    def __repr__(self):
        return "<QuestionnaireState('%s','%s')>" % (self.user_id, self.state)

Base.metadata.create_all(engine)


class DatabaseStore(AbstractServerStorage):
    '''
    Server side storage using an RDS database (where one column is the entire JSON representation of the questionnaire state)
    '''
    def store(self, user_id, data):
        logger.debug("About to store data %s for user %s", data, user_id)
        if self.has_data(user_id):
            logger.debug("Loading previous data for user %s", user_id)
            questionnaire_state = self._get_object(user_id)
            logger.debug("Loaded %s", questionnaire_state)
            questionnaire_state.set_data(data)
        else:
            logger.debug("Creating questionnaire state for user %s with data %s", user_id, data)
            questionnaire_state = QuestionnaireState(user_id, data)

        logger.debug("Committing questionnaire state")
        db_session.add(questionnaire_state)
        db_session.commit()
        logger.debug("Committed")

    def get(self, user_id):
        logger.debug("Loading questionnaire state for user %s", user_id)
        questionnaire_state = self._get_object(user_id)
        if questionnaire_state:
            data = questionnaire_state.get_data()
            logger.debug("Loaded data %s", data)
            return questionnaire_state.get_data()
        else:
            logger.debug("Return None from get")
            return None

    def _get_object(self, user_id):
        logger.debug("Get the questionnaire object for user %s", user_id)
        return QuestionnaireState.query.filter(QuestionnaireState.user_id == user_id).first()

    def has_data(self, user_id):
        logger.debug("Running count query for user %s", user_id)
        count = QuestionnaireState.query.filter(QuestionnaireState.user_id == user_id).count()
        logger.debug("Number of entries for user %s", user_id)
        return count > 0

    def delete(self, user_id):
        logger.debug("About to delete users %s data", user_id)
        if self.has_data(user_id):
            questionnaire_state = self._get_object(user_id)
            db_session.delete(questionnaire_state)
            db_session.commit()
            logger.debug("Deleted")

    def clear(self):
        logger.warning("About to delete all questionnaire data")
        QuestionnaireState.query.delete()
        logger.warning("Deleted all questionnaire data")
