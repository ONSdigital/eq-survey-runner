from abc import ABCMeta, abstractmethod


class AbstractFormatter(metaclass=ABCMeta):

    @staticmethod
    @abstractmethod
    def format(schema_answers, state_answers, user_answer):
        raise NotImplementedError()
