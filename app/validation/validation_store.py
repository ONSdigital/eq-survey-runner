from flask_login import current_user
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
        data = current_user.get_questionnaire_data()
        if RESULTS not in data:
            responses = {key: value.to_dict()}
            data[RESULTS] = responses
        else:
            data[RESULTS][key] = value.to_dict()

    def get_result(self, key):
        data = current_user.get_questionnaire_data()
        if RESULTS not in data.keys():
            data[RESULTS] = {}
            return None
        if key in data[RESULTS].keys():
            result = ValidationResult()
            result.from_dict(data[RESULTS][key])
            return result
        return None
