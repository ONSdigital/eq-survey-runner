from uuid import uuid4

from flask import session
from structlog import get_logger

from app.data_model.database import EQSession

USER_ID = "user_id"
USER_IK = "user_ik"
SURVEY_COMPLETED_METADATA = "survey_completed_metadata"
EQ_SESSION_ID = "eq-session-id"

logger = get_logger()


class SessionStorage:

    def __init__(self, database):
        self._database = database

    def store_user_id(self, user_id):
        """
        Create a new eq_session_id and associate it with the user_id specified
        """
        eq_session_id = str(uuid4())
        session[EQ_SESSION_ID] = eq_session_id
        eq_session = EQSession(eq_session_id, user_id)

        logger.debug("Adding eq_session to database", eq_session_id=eq_session_id, user_id=user_id)
        self._database.add(eq_session)

    def delete_session_from_db(self):
        """
        deletes user session from database
        """
        if EQ_SESSION_ID in session:
            eq_session_id = session[EQ_SESSION_ID]
            eq_session = self._get_user_session(eq_session_id)
            if eq_session is not None:
                self._database.delete(eq_session)
            else:
                logger.debug("eq_session_id from user's cookie not found in database")
        else:
            logger.debug("eq_session_id does not exist in user's cookie")

    def get_user_id(self):
        """
        Retrieves a user's id
        :return: the user's JWT
        """
        user_id = None
        if EQ_SESSION_ID in session:
            eq_session_id = session[EQ_SESSION_ID]
            eq_session = self._get_user_session(eq_session_id)
            if eq_session is not None:
                user_id = eq_session.user_id

        return user_id

    @staticmethod
    def _get_user_session(eq_session_id):
        logger.debug("finding eq_session_id in database", eq_session_id=eq_session_id)

        # pylint: disable=maybe-no-member
        # SQLAlchemy doing declarative magic which makes session scope query property available
        eq_session = EQSession.query.filter(EQSession.eq_session_id == eq_session_id).first()

        if eq_session is not None:
            logger.debug("found matching eq_session for eq_session_id in database",
                         session_id=eq_session.eq_session_id,
                         user_id=eq_session.user_id,
                         timestamp=eq_session.timestamp.isoformat())
        else:
            logger.debug("eq_session_id not found in database", eq_session_id=eq_session_id)

        return eq_session

    @staticmethod
    def store_user_ik(user_ik):
        """
        Store a user's ik in the cookie for retrieval later
        :param user_ik: the user ik
        """
        session[USER_IK] = user_ik

    @staticmethod
    def store_survey_completed_metadata(tx_id, period_str, ru_ref):
        """
        Store survey_completed_metadata in the cookie for retrieval later
        """
        session[SURVEY_COMPLETED_METADATA] = {
            'tx_id': tx_id,
            'period_str': period_str,
            'ru_ref': ru_ref,
        }

    @staticmethod
    def has_survey_completed_metadata():
        """
        Checks if a user has survey completed metadata
        :return: boolean value
        """

        if SURVEY_COMPLETED_METADATA in session:
            return session[SURVEY_COMPLETED_METADATA] is not None
        else:
            return False

    @staticmethod
    def has_user_ik():
        """
        Checks if a user has a stored ik
        :return: boolean value
        """
        if USER_IK in session:
            return session[USER_IK] is not None
        else:
            return False

    def remove_user_ik(self):
        """
        Removes a user's ik from the session
        """

        if self.has_user_ik():
            session.pop(USER_IK)

    def get_survey_completed_metadata(self):
        """
        Retrieves survey completed metadata
        :return: the survey completed metadata
        """
        if self.has_survey_completed_metadata():
            return session[SURVEY_COMPLETED_METADATA]
        else:
            return None

    def get_user_ik(self):
        """
        Retrieves a user's id
        :return: the user's JWT
        """
        if self.has_user_ik():
            return session[USER_IK]
        else:
            return None
