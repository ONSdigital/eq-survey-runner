from flask import session
from app.data_model.database import db_session, EQSession
import logging
from uuid import uuid4

USER_ID = "user_id"
USER_IK = "user_ik"
EQ_SESSION_ID = "eq-session-id"
MAX_RETRY = 10

logger = logging.getLogger(__name__)


class NoUniqueIDError(RuntimeError):
    pass


class SessionManagement(object):
    def store_user_id(self, user_id):
        """
        Store a user's id for retrieval later
        :param user_id: the user id
        """
        pass

    def has_user_id(self):
        """
        Checks if a user has a stored id
        :return: boolean value
        """
        pass

    def clear(self):
        """
        Removes a user id from the session
        """
        pass

    def get_user_id(self):
        """
        Retrieves a user's id
        :return: the user's JWT
        """
        pass

    def store_user_ik(self, user_ik):
        '''
        Store a user's ik in the cookie for retrieval later
        :param user_ik: the user ik
        '''
        pass

    def has_user_ik(self):
        """
        Checks if a user has a stored ik
        :return: boolean value
        """
        logger.debug("SessionManager has_user_ik() - session %s", session)
        pass

    def get_user_ik(self):
        """
        Retrieves a user's id
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

    def clear(self):
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
        for x in range(0, MAX_RETRY):
            new_session_id = str(uuid4())
            if self.check_unique(new_session_id):
                break
            else:
                new_session_id = None
        if new_session_id:
            return new_session_id
        else:
            logger.error("Unable to generate a unique session id before the retry count %s was reached", MAX_RETRY)
            raise NoUniqueIDError()

    def check_unique(self, new_session_id):
        return self.run_count(new_session_id) == 0

    def _get_object(self, eq_session_id):
        logger.debug("Get the EQ Session object for eq session id %s", eq_session_id)
        return EQSession.query.filter(EQSession.eq_session_id == eq_session_id).first()

    def run_count(self, eq_session_id):
        logger.debug("Running count query for eq session id %s", eq_session_id)
        count = EQSession.query.filter(EQSession.eq_session_id == eq_session_id).count()
        return count

    def store_user_ik(self, user_ik):
        '''
        Store a user's ik in the cookie for retrieval later
        :param user_ik: the user ik
        '''
        logger.debug("SessionManager store_user_ik() - session %s", session)
        if USER_IK not in session:
            session[USER_IK] = user_ik
            session.permanent = True

    def has_user_ik(self):
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

    def delete_all(self):
        """
        Clears all session mapping data. Use with caution
        :return:
        """
        logger.warning("About to delete all session data")
        EQSession.query.delete()
        logger.warning("Deleted all session data")


session_manager = DatabaseSessionManager()
