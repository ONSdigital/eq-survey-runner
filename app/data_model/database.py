import datetime
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

    def __init__(self, user_id, state):
        self.user_id = user_id
        self.state = state

    def __repr__(self):
        return "<QuestionnaireState('%s','%s')>" % (self.user_id, self._state)


class EQSession(base):
    __tablename__ = 'eq_session'
    eq_session_id = Column('eq_session_id', String, primary_key=True)
    user_id = Column('user_id', String, primary_key=True)
    timestamp = Column('timestamp', DateTime)

    def __init__(self, eq_session_id, user_id):
        self.eq_session_id = eq_session_id
        self.user_id = user_id
        self.timestamp = datetime.datetime.now()

    def __repr__(self):
        return "<EQSession('%s', '%s', '%s')>" % (self.eq_session_id, self.user_id, self.timestamp)


class UsedJtiClaim(base):
    __tablename__ = 'used_jti_claim'
    jti_claim = Column('jti_claim', String, primary_key=True)
    used_at = Column('used_at', DateTime)

    def __init__(self, jti_claim):
        self.jti_claim = jti_claim
        self.used_at = datetime.datetime.now()

    def __repr__(self):
        return "<UsedJtiClaim('%s', '%s')>" % (self.jti_claim, self.used_at)


SETUP_ATTEMPTS = 10
SETUP_RETRY_DELAY_SECONDS = 6


class Database:

    def __init__(self, driver, database_name, host=None, port=None,
                 username=None, password=None, setup_attempts=SETUP_ATTEMPTS,
                 setup_retry_delay=SETUP_RETRY_DELAY_SECONDS):

        if driver == 'sqlite':
            self._database_url = '{driver}://{name}'.format(driver=driver,
                                                            name=database_name)
        else:
            self._database_url = '{driver}://{username}:{password}@{host}:{port}/{name}'.format(driver=driver,
                                                                                                username=username,
                                                                                                password=password,
                                                                                                host=host,
                                                                                                port=port,
                                                                                                name=database_name)

        self._setup_attempts = setup_attempts
        self._setup_retry_delay = setup_retry_delay

        self._db_session = self._create_session_and_engine_with_retry()

    def _create_session_and_engine(self):
        logger.info('setting up database...')
        logger.debug('creating database engine')
        eng = create_engine(self._database_url, convert_unicode=True)
        logger.debug('creating database session')
        session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=eng))
        base.query = session.query_property()
        logger.debug('creating database and tables')
        base.metadata.create_all(eng)
        logger.info('database setup complete.')
        return session

    def _create_session_and_engine_with_retry(self):
        last_exception = None

        for i in range(self._setup_attempts):
            try:
                return self._create_session_and_engine()
            except Exception as e:  # pylint: disable=broad-except
                # Accept catching of Exception here as we re-throw it below if the retry fails.
                last_exception = e
                logger.error('error setting up database', exc_info=e, attempt=i)
                time.sleep(self._setup_retry_delay)
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
