from abc import ABCMeta, abstractmethod


class IValidator(metaclass=ABCMeta):

    @abstractmethod
    def validate(self):
        raise NotImplementedError()
