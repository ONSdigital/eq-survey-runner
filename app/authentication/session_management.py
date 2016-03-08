from flask import session
import logging


class SessionManagement(object):
    def add_token(self, jwt):
        pass

    def has_token(self):
        pass

    def remove_token(self):
        pass

    def get_token(self):
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
        return session['jwt']

session_manager = FlaskSessionManager()
