from abc import abstractmethod

class IValidator(object):

    @abstractmethod
    def validate(self):
        raise NotImplementedError()
