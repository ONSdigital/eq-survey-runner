from abc import ABCMeta, abstractmethod


class AbstractValidator(metaclass=ABCMeta):
    # Some constants for error codes
    NOT_INTEGER = 'NOT_INTEGER'
    NOT_STRING = 'NOT_STRING'
    NEGATIVE_INTEGER = "NEGATIVE_INTEGER"
    MANDATORY = "MANDATORY"
    INVALID_DATE = "INVALID_DATE"

    @abstractmethod
    def validate(self, user_answer):
        raise NotImplementedError()
