from flask_login import current_user
from abc import ABCMeta, abstractmethod

ANSWERS = "ans"


class AbstractAnswerStore(metaclass=ABCMeta):
    @abstractmethod
    def store_answer(self, key, value):
        raise NotImplementedError()

    @abstractmethod
    def get_answer(self, key):
        raise NotImplementedError()

    @abstractmethod
    def get_answers(self):
        raise NotImplementedError()

    @abstractmethod
    def clear_answers(self):
        raise NotImplementedError()


class AnswerStore(AbstractAnswerStore):

    def store_answer(self, key, value):
        data = current_user.get_questionnaire_data()
        if ANSWERS not in data:
            answers = {key: value}
            data[ANSWERS] = answers
        else:
            data[ANSWERS][key] = value

    def get_answer(self, key):
        data = current_user.get_questionnaire_data()
        if ANSWERS not in data.keys():
            data[ANSWERS] = {}
            return None
        if key not in data[ANSWERS].keys():
            return None
        return data[ANSWERS][key]

    def get_answers(self):
        data = current_user.get_questionnaire_data()
        if ANSWERS not in data.keys():
            data[ANSWERS] = {}
        return data[ANSWERS]

    def clear_answers(self):
        data = current_user.get_questionnaire_data()
        if ANSWERS in data.keys():
            del data[ANSWERS]
