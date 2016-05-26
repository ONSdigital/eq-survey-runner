from flask import session
from app import settings
from app.data_model.database import db_session, EQSession
import logging
from uuid import uuid4

USER_ID = "user_id"
EQ_SESSION_ID = "eq-session-id"
logger = logging.getLogger(__name__)


class SessionManagement(object):
    def store_user_id(self, jwt):
        """
        Store a user's id for retrieval later
        :param jwt: the user JWT
        """
        pass

    def has_user_id(self):
        """
        Checks if a user has a stored id
        :return: boolean value
        """
        pass

    def remove_user_id(self):
        """
        Removes a user id from the session
        """
        pass

    def get_user_id(self):
        """
        Retrieves a user's token
        :return: the user's JWT
        """
        pass


class DatabaseSessionManager(SessionManagement):

    def store_user_id(self, user_id):
        logger.debug("DatabaseSessionManager store_user_id() - session %s", session)
        if EQ_SESSION_ID not in session:
            eq_session_id = self.create_session_id()
            logger.debug("Created new eq session id %s", eq_session_id)
            session[EQ_SESSION_ID] = eq_session_id
            session.permanent = True
            eq_session = EQSession(eq_session_id, user_id)
            logger.debug("Constructed EQ Session object %s", eq_session)
        else:
            eq_session_id = session[EQ_SESSION_ID]
            logger.debug("Found eq_session_id %s in session", eq_session_id)
            eq_session = self._get_object(eq_session_id)
            logger.debug("Loaded object eq session %s", eq_session)
        logger.debug("About to commit to database")
        db_session.add(eq_session)
        db_session.commit()
        logger.debug("Committed")

    def has_user_id(self):
        logger.debug("DatabaseSessionManager has_user_id() - session %s", session)
        if EQ_SESSION_ID in session:
            eq_session_id = session[EQ_SESSION_ID]

            count = self.run_count(eq_session_id)
            logger.debug("Number of entries for eq session id %s is %s", eq_session_id, count)
            return count > 0

    def remove_user_id(self):
        logger.debug("DatabaseSessionManager remove_user_id() - session %s", session)
        if EQ_SESSION_ID in session:
            eq_session_id = session[EQ_SESSION_ID]
            eq_session = self._get_object(eq_session_id)
            logger.debug("About to delete entry from eq_session table %s", eq_session)
            db_session.delete(eq_session)
            db_session.commit()
        else:
            logger.warning("No eq session id exists")

    def get_user_id(self):
        logger.debug("DatabaseSessionManager get_user_id() - session %s", session)
        if EQ_SESSION_ID in session:
            eq_session_id = session[EQ_SESSION_ID]
            eq_session = self._get_object(eq_session_id)
            return eq_session.user_id
        else:
            return None

    def create_session_id(self):
        while True:
            new_session_id = str(uuid4())
            if self.check_unique(new_session_id):
                break
        return new_session_id

    def check_unique(self, new_session_id):
        return self.run_count(new_session_id) == 0

    def _get_object(self, eq_session_id):
        logger.debug("Get the EQ Session object for eq session id %s", eq_session_id)
        return EQSession.query.filter(EQSession.eq_session_id == eq_session_id).first()

    def run_count(self, eq_session_id):
        logger.debug("Running count query for eq session id %s", eq_session_id)
        count = EQSession.query.filter(EQSession.eq_session_id == eq_session_id).count()
        return count


class FlaskSessionManager(SessionManagement):
    def store_user_id(self, user_id):
        logger.debug("FlaskSessionManager store_user_id() - session %s", session)
        if USER_ID not in session:
            session[USER_ID] = user_id
            session.permanent = True

    def has_user_id(self):
        logger.debug("FlaskSessionManager has_user_id() - session %s", session)
        if USER_ID in session:
            return session[USER_ID] is not None
        else:
            return False

    def remove_user_id(self):
        logger.debug("FlaskSessionManager remove_user_id() - session %s", session)
        if USER_ID in session:
            del session[USER_ID]

    def get_user_id(self):
        logger.debug("FlaskSessionManager get_user_id() - session %s", session)
        if self.has_user_id():
            return session[USER_ID]
        else:
            return None

if settings.EQ_SERVER_SIDE_STORAGE:
    session_manager = DatabaseSessionManager()
else:
    session_manager = FlaskSessionManager()
