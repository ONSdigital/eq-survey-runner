from flask_login import current_user
from abc import ABCMeta, abstractmethod

RESPONSES = "resp"


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

    @abstractmethod
    def clear_responses(self):
        raise NotImplementedError()


class FlaskResponseStore(AbstractResponseStore):

    def store_response(self, key, value):
        data = current_user.get_questionnaire_data()
        if RESPONSES not in data:
            responses = {key: value}
            data[RESPONSES] = responses
        else:
            data[RESPONSES][key] = value

    def get_response(self, key):
        data = current_user.get_questionnaire_data()
        if RESPONSES not in data.keys():
            data[RESPONSES] = {}
            return None
        if key not in data[RESPONSES].keys():
            return None
        return data[RESPONSES][key]

    def get_responses(self):
        data = current_user.get_questionnaire_data()
        if RESPONSES not in data.keys():
            data[RESPONSES] = {}
        return data[RESPONSES]

    def clear_responses(self):
        data = current_user.get_questionnaire_data()
        if RESPONSES in data.keys():
            del data[RESPONSES]
