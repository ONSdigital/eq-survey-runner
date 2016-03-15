from flask import session
from abc import ABCMeta, abstractmethod
from app.validation.validation_result import ValidationResult

RESULTS = 'val'


class AbstractValidationStore(metaclass=ABCMeta):
    # keys are in the format...
    # group:block:section:question:response:<repetition>
    @abstractmethod
    def store_result(self, key, value):
        raise NotImplementedError()

    @abstractmethod
    def get_result(self, key):
        raise NotImplementedError()


class FlaskValidationStore(AbstractValidationStore):

    def store_result(self, key, value):
        if RESULTS not in session:
            responses = {key: value.to_dict()}
            session[RESULTS] = responses
        else:
            session[RESULTS][key] = value.to_dict()
        session.permanent = True

    def get_result(self, key):
        if RESULTS not in session.keys():
            session[RESULTS] = {}
            return None
        if key in session[RESULTS].keys():
            result = ValidationResult()
            result.from_dict(session[RESULTS][key])
            return result
        return None
