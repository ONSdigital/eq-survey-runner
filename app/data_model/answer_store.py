from jinja2 import escape
from structlog import get_logger
import simplejson as json

from app.data_model.answer import Answer

logger = get_logger()


class AnswerStore:
    """
    An object that stores and updates a collection of answers, ready for serialisation
    via the Questionnaire Store.
    """

    def __init__(self, existing_answers=None):
        if isinstance(existing_answers, list):
            self.answer_map = self._build_map(existing_answers or [])
        else:
            self.answer_map = existing_answers or {}

    def __iter__(self):
        return iter(self.answer_map.values())

    def __len__(self):
        return len(self.answer_map)

    def __eq__(self, other):
        return self.answer_map == other.answer_map

    @staticmethod
    def _build_map(answers):
        answer_map = {}

        for answer in answers:
            answer_map[answer['answer_id']] = answer

        return answer_map

    @staticmethod
    def _validate(answer):
        if not isinstance(answer, Answer):
            raise TypeError('Method only supports Answer argument type')

    def copy(self):
        """
        Create a new instance of answer_store with the same values.
        """
        return self.__class__(self.answer_map.copy())

    def add_or_update(self, answer):
        """
        Add a new answer into the answer store, or update if it exists.

        :param answer: An answer object.
        """
        self._validate(answer)

        answer_to_add = vars(answer).copy()
        self.answer_map[answer.answer_id] = answer_to_add

    def count(self):
        """
        Count of the number of answers in the answer store.
        NB: can be combined with `filter` method to find count of an answer, e.g.:

            `answer_store.filter(answer_id=example_id).count()`

        :return: Number of answers in this store.
        """
        return len(self)

    def values(self):
        """
        Return a flat list of all values in the answer store.

        :return: Return a list of answer values
        """
        return [answer['value'] for answer in self]

    def escaped(self):
        """
        Escape all answer values and return a new AnswerStore instance.

        :return: Return a new AnswerStore object with escaped answers for chaining
        """
        escaped = []
        for answer in self:
            answer = answer.copy()
            if isinstance(answer['value'], str):
                answer['value'] = escape(answer['value'])
            escaped.append(answer)
        return self.__class__(existing_answers=escaped)

    def filter(self, answer_ids):
        """
        Find all answers in the answer store for a given set of filter parameter matches.

        :param answer_ids: The answer ids to filter results by
        :return: Return a new AnswerStore object with filtered answers for chaining
        """
        answers = [v for k, v in self.answer_map.items() if k in answer_ids]

        return self.__class__(existing_answers=answers)

    def clear(self):
        """
        Clears answers *in place*
        """
        self.answer_map.clear()

    def remove(self, answer_ids=None):
        """
        Removes answer(s) *in place* from the answer store.

        :param answer_ids: The answer ids to remove
        """
        for answer_id in answer_ids:
            if answer_id in self.answer_map:
                del self.answer_map[answer_id]

    def remove_answer(self, answer):
        """
        Removes answer *in place* from the answer store.

        :param answer: The answer to remove
        """

        if answer['answer_id'] in self.answer_map:
            del self.answer_map[answer['answer_id']]

    def get_hash(self):
        """
        Gets unique hash from answers contained within this AnswerStore

        :return: Return a unique hash value
        """
        return hash(json.dumps(self.answer_map, sort_keys=True))
