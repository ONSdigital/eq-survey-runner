import datetime
import json
import time

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from structlog import get_logger

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


class UsedJtiClaim(base):
    __tablename__ = "used_jti_claim"
    jti_claim = Column("jti_claim", String, primary_key=True)
    used_at = Column("used_at", DateTime)

    def __init__(self, jti_claim):
        self.jti_claim = jti_claim
        self.used_at = datetime.datetime.now()

    def __repr__(self):
        return "<UsedJtiClaim('%s', '%s')>" % (self.jti_claim, self.used_at)


class Database:

    def __init__(self, database_url, database_setup_retry_count, database_setup_retry_delay):

        self.database_url = database_url
        self.database_setup_retry_count = database_setup_retry_count
        self.database_setup_retry_delay = database_setup_retry_delay

        self._db_session = self._create_session_and_engine_with_retry()

    def _create_session_and_engine(self):
        logger.info("setting up database...")
        logger.debug("creating database engine")
        eng = create_engine(self.database_url, convert_unicode=True)
        logger.debug("creating database session")
        session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=eng))
        base.query = session.query_property()
        logger.debug("creating database and tables")
        base.metadata.create_all(eng)
        logger.info('database setup complete.')
        return session

    def _create_session_and_engine_with_retry(self):
        last_exception = None

        for i in range(self.database_setup_retry_count):
            try:
                return self._create_session_and_engine()
            except Exception as e:  # pylint: disable=broad-except
                # Accept catching of Exception here as we re-throw it below if the retry fails.
                last_exception = e
                logger.error('error setting up database', exc_info=e, attempt=i)
                time.sleep(self.database_setup_retry_delay)
        else:  # pylint: disable=useless-else-on-loop
            logger.error('failed to setup database, aborting', exc_info=last_exception)
            raise TimeoutError('failed to setup database') from last_exception

    def remove(self):
        self._db_session.remove()

    def add(self, item_to_add):
        # pylint: disable=maybe-no-member
        self._db_session.add(item_to_add)
        # pylint: disable=maybe-no-member
        self._db_session.commit()

    def delete(self, item_to_delete):
        # pylint: disable=maybe-no-member
        self._db_session.delete(item_to_delete)
        # pylint: disable=maybe-no-member
        self._db_session.commit()
