from flask import session


class SessionManagement(object):
    def link_session(self, jwt):
        pass

    def has_session(self):
        pass

    def unlink_session(self):
        pass


class FlaskSessionManager(SessionManagement):
    def link_session(self, jwt):
        if 'jwt' not in session:
            session['jwt'] = jwt

    def has_session(self):
        return 'jwt' in session

    def unlink_session(self):
        if 'jwt' in session:
            session['jwt'] = None


class SessionManagementFactory(object):

    @staticmethod
    def get_session_management():
        return FlaskSessionManager()
