from abc import ABCMeta, abstractmethod


class AbstractValidator(metaclass=ABCMeta):

    @abstractmethod
    def validate(self, user_answer):
        raise NotImplementedError()
