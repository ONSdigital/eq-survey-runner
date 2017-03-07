import datetime
import json
import time
from contextlib import contextmanager

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import String
from sqlalchemy import create_engine
from sqlalchemy import event
from sqlalchemy import exc
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from structlog import get_logger

from app import settings

logger = get_logger()

base = declarative_base()


class QuestionnaireState(base):
    __tablename__ = 'questionnaire_state'
    user_id = Column('userid', String, primary_key=True)
    state = Column('questionnaire_data', String)

    def __init__(self, user_id, data):
        self.user_id = user_id
        self.state = json.dumps(data)

    def set_data(self, data):
        logger.debug("setting data for questionnaire state")
        self.state = json.dumps(data)

    def get_data(self):
        data = json.loads(self.state)
        logger.debug("loading questionnaire state")
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


def _create_session_and_engine():
    logger.info("setting up database...")
    logger.debug("creating database engine")
    eng = create_engine(settings.EQ_SERVER_SIDE_STORAGE_DATABASE_URL, convert_unicode=True)
    logger.debug("creating database session")
    session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=eng))
    base.query = session.query_property()
    logger.debug("creating database and tables")
    base.metadata.create_all(eng)
    logger.info('database setup complete.')
    return session, eng


def _create_session_and_engine_with_retry():
    last_exception = None

    for i in range(settings.EQ_SERVER_SIDE_STORAGE_DATABASE_SETUP_RETRY_COUNT):
        try:
            return _create_session_and_engine()
        except Exception as e:  # pylint: disable=broad-except
            # Accept catching of Exception here as we re-throw it below if the retry fails.
            last_exception = e
            logger.error('error setting up database', exc_info=e, attempt=i)
            time.sleep(settings.EQ_SERVER_SIDE_STORAGE_DATABASE_SETUP_RETRY_DELAY_SECONDS)
    else:  # pylint: disable=useless-else-on-loop
        logger.error('failed to setup database, aborting', exc_info=last_exception)
        raise TimeoutError('failed to setup database') from last_exception


db_session, engine = _create_session_and_engine_with_retry()


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
    except SQLAlchemyError:
        database_session.rollback()
        raise
