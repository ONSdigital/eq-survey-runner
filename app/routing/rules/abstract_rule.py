from abc import ABCMeta, abstractmethod


class AbstractRule(metaclass=ABCMeta):

    def __init__(self, questionnaire_manager, rule):
        self._questionnaire_manager = questionnaire_manager
        self._rule = rule

    @abstractmethod
    def next_location(self):
        raise NotImplementedError()
