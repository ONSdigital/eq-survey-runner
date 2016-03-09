from abc import ABCMeta, abstractmethod


class IValidator(object):

    @abstractmethod
    def validate(self):
        raise NotImplementedError()
