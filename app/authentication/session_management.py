from flask import session
import logging


class SessionManagement(object):
    def add_token(self, jwt):
        """
        Store a user's token for retrieval later
        :param jwt: the user JWT
        """
        pass

    def has_token(self):
        """
        Checks if a user has a stored token
        :return: boolean value
        """
        pass

    def remove_token(self):
        """
        Removes a user token
        """
        pass

    def get_token(self):
        """
        Retrieves a user's token
        :return: the user's JWT
        """
        pass


class FlaskSessionManager(SessionManagement):
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def add_token(self, jwt):
        if 'jwt' not in session:
            session['jwt'] = jwt
            session.permanent = True

    def has_token(self):
        self.logger.debug(session)
        if 'jwt' in session:
            return session['jwt'] is not None
        else:
            return False

    def remove_token(self):
        if 'jwt' in session:
            del session['jwt']

    def get_token(self):
        if self.has_token():
            return session['jwt']
        else:
            return None

session_manager = FlaskSessionManager()
