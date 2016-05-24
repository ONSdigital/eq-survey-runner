from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime, create_engine
from app import settings
import datetime
import logging
import json

logger = logging.getLogger(__name__)

Base = declarative_base()


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


class EQSession(Base):
    __tablename__ = "eq_session"
    eq_session_id = Column("eq_session_id", String, primary_key=True)
    user_id = Column("user_id", String, primary_key=True)
    timestamp = Column("timestamp", DateTime)

    def __init__(self, eq_session_id, user_id):
        self.eq_session_id = eq_session_id
        self.user_id = user_id
        self.timestamp = datetime.datetime.now()

    def __repr__(self):
        return "<EQSession('%s', '%s', '%s')>" % (self.eq_session_id, self.user_id, self.timestamp)


def create_session_and_engine():
    try:
        logger.debug("About to create DB engine for %s", settings.EQ_SERVER_SIDE_STORAGE_DATABASE_URL)
        eng = create_engine(settings.EQ_SERVER_SIDE_STORAGE_DATABASE_URL, convert_unicode=True)
        logger.debug("Created engine")
        logger.debug("About to create DB session")
        session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=eng))
        logger.debug("Session created")
        return session, eng
    except Exception as e:
        logger.error("Error creating database connections")
        logger.exception(e)
        raise e


db_session, engine = create_session_and_engine()
Base.query = db_session.query_property()

Base.metadata.create_all(engine)
