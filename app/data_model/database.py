import datetime
import json
import logging
from contextlib import contextmanager

from app import settings

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import String
from sqlalchemy import create_engine
from sqlalchemy import exc
from sqlalchemy import event
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

logger = logging.getLogger(__name__)

base = declarative_base()


class QuestionnaireState(base):
    __tablename__ = 'questionnaire_state'
    user_id = Column('userid', String, primary_key=True)
    state = Column('questionnaire_data', String)

    def __init__(self, user_id, data):
        self.user_id = user_id
        self.state = json.dumps(data)

    def set_data(self, data):
        logger.debug("Setting data for questionnaire state")
        self.state = json.dumps(data)

    def get_data(self):
        data = json.loads(self.state)
        logger.debug("Loading questionnaire state")
        return data

    def __repr__(self):
        return "<QuestionnaireState('%s','%s')>" % (self.user_id, self.state)


class EQSession(base):
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
base.query = db_session.query_property()

base.metadata.create_all(engine)


@event.listens_for(engine, "engine_connect")
def test_connection(connection, branch):
    if branch:
        # "branch" refers to a sub-connection of a connection,
        # we don't want to bother testing on these.
        return

    save_should_close_with_result = connection.should_close_with_result
    connection.should_close_with_result = False
    try:
        # Run a SELECT 1 to test the database connection
        connection.scalar(select([1]))
    except exc.DBAPIError:
        try:
            # try it again, this will recreate a stale or broke connection
            connection.scalar(select([1]))
        except exc.DBAPIError:
            # However if we get a database err again, forcibly close the connection
            connection.close()

    finally:
        # restore "close with result"
        connection.should_close_with_result = save_should_close_with_result


@contextmanager
def commit_or_rollback(database_session):
    try:
        yield database_session
        database_session.commit()
        logger.debug("Committed")
    except SQLAlchemyError:
        database_session.rollback()
        raise
