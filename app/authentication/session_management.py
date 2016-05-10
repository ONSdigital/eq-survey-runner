from flask import session
import logging

USER_ID = "user_id"


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


class FlaskSessionManager(SessionManagement):
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def store_user_id(self, jwt):
        if USER_ID not in session:
            session[USER_ID] = jwt
            session.permanent = True

    def has_user_id(self):
        self.logger.debug(session)
        if USER_ID in session:
            return session[USER_ID] is not None
        else:
            return False

    def remove_user_id(self):
        if USER_ID in session:
            del session[USER_ID]

    def get_user_id(self):
        if self.has_user_id():
            return session[USER_ID]
        else:
            return None

session_manager = FlaskSessionManager()
