from abc import ABCMeta, abstractmethod


class IValidationSteps(object):

    @abstractmethod
    def validation_steps(self, container, validating, validation_store):
        raise NotImplementedError()
