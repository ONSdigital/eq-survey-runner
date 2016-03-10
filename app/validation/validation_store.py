from flask import session
from abc import ABCMeta, abstractmethod


class ValidationStoreFactory(object):
    @staticmethod
    def create_validation_store():
        return FlaskValidationStore()


class IValidationStore(metaclass=ABCMeta):
    # keys are in the format...
    # group:block:section:question:response:<repetition>
    @abstractmethod
    def store_result(self, key, value):
        raise NotImplementedError()

    @abstractmethod
    def get_result(self, key):
        raise NotImplementedError()


class FlaskValidationStore(IValidationStore):

    def store_result(self, key, value):
        session[key] = value
        session.permanent = True

    def get_result(self, key):
        return session[key]
