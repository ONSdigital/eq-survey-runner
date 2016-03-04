from abc import ABCMeta, abstractmethod


class AbstractValidator(object):

    def __init__(self, context):
        self.context = context

    @abstractmethod
    def validate(self):
        raise NotImplementedError()
