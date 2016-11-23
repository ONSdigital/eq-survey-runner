import logging
from uuid import uuid4

from app.data_model.database import EQSession, commit_or_rollback
from app.data_model.database import db_session

from flask import session

USER_ID = "user_id"
USER_IK = "user_ik"
EQ_SESSION_ID = "eq-session-id"

logger = logging.getLogger(__name__)


class SessionManager:

    def store_user_id(self, user_id):
        """
        Store a user's id for retrieval later
        :param user_id: the user id
        """
        logger.debug("SessionManager store_user_id() - session %s", session)
        if EQ_SESSION_ID not in session:
            eq_session_id = str(uuid4())
            logger.debug("Created new eq session id %s", eq_session_id)
            session[EQ_SESSION_ID] = eq_session_id
            eq_session = EQSession(eq_session_id, user_id)
            logger.debug("Constructed EQ Session object %s", eq_session)
        else:
            eq_session_id = session[EQ_SESSION_ID]
            logger.debug("Found eq_session_id %s in session", eq_session_id)
            eq_session = self._get_object(eq_session_id)
            logger.debug("Loaded object eq session %s", eq_session)

        logger.debug("About to commit to database")
        with commit_or_rollback(db_session):
            db_session.add(eq_session)

    def has_user_id(self):
        """
        Checks if a user has a stored id
        :return: boolean value
        """
        logger.debug("SessionManager has_user_id() - session %s", session)
        if EQ_SESSION_ID in session:
            eq_session_id = session[EQ_SESSION_ID]

            count = self.run_count(eq_session_id)
            logger.debug("Number of entries for eq session id %s is %s", eq_session_id, count)
            return count > 0

    def clear(self):
        """
        Removes a user id from the session
        """
        logger.debug("SessionManager remove_user_id() - session %s", session)
        if EQ_SESSION_ID in session:
            eq_session_id = session[EQ_SESSION_ID]
            eq_session = self._get_object(eq_session_id)
            logger.debug("About to delete entry from eq_session table %s", eq_session)

            with commit_or_rollback(db_session):
                db_session.delete(eq_session)
        else:
            logger.warning("No eq session id exists")

    def get_user_id(self):
        """
        Retrieves a user's id
        :return: the user's JWT
        """
        logger.debug("SessionManager get_user_id() - session %s", session)
        if EQ_SESSION_ID in session:
            eq_session_id = session[EQ_SESSION_ID]
            eq_session = self._get_object(eq_session_id)
            return eq_session.user_id
        else:
            return None

    @staticmethod
    def _get_object(eq_session_id):
        logger.debug("Get the EQ Session object for eq session id %s", eq_session_id)
        return EQSession.query.filter(EQSession.eq_session_id == eq_session_id).first()

    @staticmethod
    def run_count(eq_session_id):
        logger.debug("Running count query for eq session id %s", eq_session_id)
        count = EQSession.query.filter(EQSession.eq_session_id == eq_session_id).count()
        return count

    @staticmethod
    def store_user_ik(user_ik):
        """
        Store a user's ik in the cookie for retrieval later
        :param user_ik: the user ik
        """
        logger.debug("SessionManager store_user_ik() - session %s", session)
        if USER_IK not in session:
            session[USER_IK] = user_ik

    @staticmethod
    def has_user_ik():
        """
        Checks if a user has a stored ik
        :return: boolean value
        """
        logger.debug("SessionManager has_user_ik() - session %s", session)
        if USER_IK in session:
            return session[USER_IK] is not None
        else:
            return False

    def get_user_ik(self):
        """
        Retrieves a user's id
        :return: the user's JWT
        """
        logger.debug("SessionManager get_user_ik() - session %s", session)
        if self.has_user_ik():
            return session[USER_IK]
        else:
            return None


session_manager = SessionManager()
