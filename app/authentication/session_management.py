from flask import session


class SessionManagement(object):
    def add_token(self, jwt):
        pass

    def has_token(self):
        pass

    def remove_token(self):
        pass


class FlaskSessionManager(SessionManagement):
    def add_token(self, jwt):
        if 'jwt' not in session:
            session['jwt'] = jwt
            session.permanent = True

    def has_token(self):
        return 'jwt' in session

    def remove_token(self):
        if 'jwt' in session:
            del session['jwt']

session_manager = FlaskSessionManager()
