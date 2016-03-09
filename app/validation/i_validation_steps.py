from abc import ABCMeta, abstractmethod


class IValidationSteps(metaclass=ABCMeta):

    @abstractmethod
    def validation_steps(self, container, validating, validation_store):
        raise NotImplementedError()
