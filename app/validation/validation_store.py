from flask import session
from abc import ABCMeta, abstractmethod
from app.validation.validation_result import ValidationResult

<<<<<<< HEAD

class ValidationStoreFactory(object):
    @staticmethod
    def create_validation_store():
        return FlaskValidationStore()


class IValidationStore(metaclass=ABCMeta):
    # keys are in the format...
    # group:block:section:question:response:<repetition>
    @abstractmethod
=======
class ValidationStore(object):

    def __init__(self):
        self.validation_results = {}

>>>>>>> eq-1 validation basics
    def store_result(self, key, value):
        self.validation_results.update({key: value})

    @abstractmethod
    def get_result(self, key):
<<<<<<< HEAD
<<<<<<< HEAD
        raise NotImplementedError()


class FlaskValidationStore(IValidationStore):

    def store_result(self, key, value):
        session[key] = value.to_dict()
        session.permanent = True

    def get_result(self, key):
        result = ValidationResult()
        result.from_dict(session[key])
        return result
=======
        return self.validation_results.get(key, "No validated")
<<<<<<< HEAD


>>>>>>> eq-1 validation basics
=======
>>>>>>> Tidying up various source code issues
=======
        return self.validation_results.get(key, "Not validated")
<<<<<<< HEAD

>>>>>>> eq-1 update validation with questionnaire model
=======
>>>>>>> eq-1 fix code style errors
