from abc import ABCMeta, abstractmethod


class IValidator(metaclass=ABCMeta):

    @abstractmethod
    def validate(self, user_answer):
        raise NotImplementedError()
