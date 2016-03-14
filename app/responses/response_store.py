from flask import session

RESPONSES = "resp"


class ResponseStoreFactory(object):
    @staticmethod
    def create_response_store():
        return FlaskResponseStore()


class IResponseStore(object):

    def store_response(self, key, value):
        raise NotImplementedError()

    def get_response(self, key):
        raise NotImplementedError()

    def get_responses(self):
        raise NotImplementedError()


class FlaskResponseStore(IResponseStore):

    def store_response(self, key, value):
        if RESPONSES not in session:
            responses = {key: value}
            session[RESPONSES] = responses
        else:
            session[RESPONSES][key] = value
        session.permanent = True

    def get_response(self, key):
        return session[RESPONSES][key]

    def get_responses(self):
        return session[RESPONSES]
