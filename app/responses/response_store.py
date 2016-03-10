from flask import session


class ResponseStoreFactory(object):
    @staticmethod
    def create_response_store():
        return FlaskResponseStore()


class IResponseStore(object):

    def store_response(self, key, value):
        raise NotImplementedError()

    def get_response(self, key):
        raise NotImplementedError()


class FlaskResponseStore(IResponseStore):

    def store_response(self, key, value):
        session[key] = value
        session.permanent = True

    def get_response(self, key):
        return session[key]
