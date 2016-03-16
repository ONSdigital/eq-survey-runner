from flask import session
from abc import ABCMeta, abstractmethod

RESPONSES = "resp"


class ResponseStoreFactory(object):
    @staticmethod
    def create_response_store():
        return FlaskResponseStore()


class AbstractResponseStore(metaclass=ABCMeta):
    @abstractmethod
    def store_response(self, key, value):
        raise NotImplementedError()

    @abstractmethod
    def get_response(self, key):
        raise NotImplementedError()

    @abstractmethod
    def get_responses(self):
        raise NotImplementedError()


class FlaskResponseStore(AbstractResponseStore):

    def store_response(self, key, value):
        if RESPONSES not in session:
            responses = {key: value}
            session[RESPONSES] = responses
        else:
            session[RESPONSES][key] = value
        session.permanent = True

    def get_response(self, key):
        if RESPONSES not in session.keys():
            session[RESPONSES] = {}
            return None
        if key not in session[RESPONSES].keys():
            return None
        return session[RESPONSES][key]

    def get_responses(self):
        if RESPONSES not in session.keys():
            session[RESPONSES] = {}
        return session[RESPONSES]
