from app.questionnaire_state.user_journey_manager import UserJourneyManager
from abc import ABCMeta, abstractmethod
import logging


ANSWERS = "ans"


logger = logging.getLogger(__name__)


class AbstractAnswerStore(metaclass=ABCMeta):
    @abstractmethod
    def store_answer(self, key, value):
        raise NotImplementedError()

    @abstractmethod
    def get_answer(self, key):
        raise NotImplementedError()

    @abstractmethod
    def get_answers(self):
        raise NotImplementedError()

    @abstractmethod
    def clear_answers(self):
        raise NotImplementedError()


class AnswerStore(AbstractAnswerStore):

    def store_answer(self, key, value):
        pass

    def get_answer(self, key):
        # ujm = UserJourneyManager.get_instance()
        # current_state = ujm.get_current_state()
        # answer = current_state.get_answer(key)
        # return answer.input
        #
        answers = self.get_answers()
        if key in answers:
            return answers[key]
        else:
            return None

    def get_answers(self):
        answers_dict = {}
        ujm = UserJourneyManager.get_instance()
        if ujm:
            page = ujm.get_first()
            answers = []
            while page:
                page_answers = page.page_state.get_answers()
                answers.extend(page_answers)
                page = page.next_page

            for answer in answers:
                id = answer.id
                value = answer.input
                answers_dict[id] = value
        return answers_dict

    def clear_answers(self):
        pass
