from flask import session


class ResponseStore(object):

    def store_response(self, key, value):
        raise NotImplementedError()

    def get_response(self, key):
        raise NotImplementedError()


class FlaskResponseStore(ResponseStore):

    def store_response(self, key, value):
        session[key] = value
        session.permanent = True

    def get_response(self, key):
        return session[key]
