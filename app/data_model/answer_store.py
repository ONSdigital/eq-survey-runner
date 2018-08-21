import itertools
import re

from collections import defaultdict
from datetime import datetime
from jinja2 import escape
import simplejson as json


class Answer:
    def __init__(self, answer_id, value, group_instance=0, answer_instance=0):
        if answer_id is None or value is None:
            raise ValueError("Both 'answer_id' and 'value' must be set for Answer")

        self.answer_id = answer_id
        self.group_instance = group_instance
        self.answer_instance = answer_instance
        self.value = value

    def matches(self, answer):
        """
        Check to see if two answers match.
        Two answers are considered to match if they share the same block_id, answer, answer_instance, group_id and group_instance.

        :param answer: An answer to compare
        :return: True if both answers match, otherwise False.
        """
        return self.answer_id == answer.answer_id and \
            self.group_instance == answer.group_instance and \
            self.answer_instance == answer.answer_instance

    def matches_dict(self, answer_dict):
        """
        Check to see if a dict describes an answer the same as this object.

        :param answer_dict: A dict providing
        :return:
        """

        return self.matches(Answer(
            answer_dict['answer_id'],
            answer_dict['value'],
            answer_dict['group_instance'],
            answer_dict['answer_instance'],
        ))


class AnswerStore:
    """
    An object that stores and updates a collection of answers, ready for serialisation
    via the Questionnaire Store.
    """

    EQ_MAX_NUM_REPEATS = 25

    def __init__(self, existing_answers=None):
        self.answers = existing_answers or []
        self.answer_map = self._build_map(self.answers)

    def __iter__(self):
        return iter(self.answers)

    def __getitem__(self, key):
        return self.answers[key]

    def __setattr__(self, key, value):
        super().__setattr__(key, value)

        if key == 'answers':
            self.answer_map = self._build_map(self.answers)

    def __len__(self):
        return len(self.answers)

    @staticmethod
    def _build_map(answers):
        answer_map = defaultdict(list)

        for answer in answers:
            answer_map[answer['answer_id']].append(answer)

        return answer_map

    @staticmethod
    def _validate(answer):
        if not isinstance(answer, Answer):
            raise TypeError('Method only supports Answer argument type')

    def add(self, answer):
        """
        Add a new answer into the answer store.

        :param answer: A dict of flattened answer details.
        """
        self._validate(answer)

        answer_to_add = answer.__dict__.copy()

        if self.find(answer) is not None:
            raise ValueError('Answer instance already exists in store')
        else:
            self.answers.append(answer_to_add)
            self.answer_map[answer_to_add['answer_id']].append(answer_to_add)

    def update(self, answer):
        """
        Update the value of an answer already in the answer store.

        :param answer: A dict of flattened answer details.
        """
        position = self.find(answer)

        if position is None:
            raise ValueError('Answer instance does not exist in store')
        else:
            self.answers[position]['value'] = answer.value

    def add_or_update(self, answer):
        """
        Add a new answer into the answer store, or update if it exists.

        :param answer: An answer object.
        """
        try:
            self.update(answer)
        except ValueError:
            self.add(answer)

    def find(self, answer):
        """
        Returns the position of an answer if it exists

        :param answer: The answer to search for
        :return: The position the answer exists at, None if it doesn't exist
        """
        self._validate(answer)

        for index, existing in enumerate(self.answers):
            if answer.matches_dict(existing):
                return index

        return None

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
        return [answer['value'] for answer in self.answers]

    def escaped(self):
        """
        Escape all answer values and return a new AnswerStore instance.

        :return: Return a new AnswerStore object with escaped answers for chaining
        """
        escaped = []
        for answer in self.answers:
            answer = answer.copy()
            if isinstance(answer['value'], str):
                answer['value'] = escape(answer['value'])
            escaped.append(answer)
        return self.__class__(existing_answers=escaped)

    def filter(self, answer_ids, group_instance=None, answer_instance=None,
               limit=None):
        """
        Find all answers in the answer store for a given set of filter parameter matches.
        If no filter parameters are passed it returns a copy of the instance.

        :param answer_ids: The answer ids to filter results by
        :param answer_instance: The answer instance to filter results by
        :param group_instance: The group instance to filter results by
        :param limit: True | False Limit the number of answers returned
        :return: Return a new AnswerStore object with filtered answers for chaining
        """
        filtered = []

        filter_vars = {
            'answer_id': answer_ids,
            'answer_instance': answer_instance,
            'group_instance': group_instance,
        }

        if answer_ids:
            answers = itertools.chain.from_iterable(self.answer_map[answer_id] for answer_id in answer_ids)
        else:
            answers = self.answers

        for answer in answers:
            matches = all(
                answer[key] in value if isinstance(value, list) else answer[key] == value
                for key, value in filter_vars.items()
                if value is not None
            )
            if matches:
                filtered.append(answer)
                if limit and len(filtered) == self.EQ_MAX_NUM_REPEATS:
                    break

        return self.__class__(existing_answers=filtered)

    def clear(self):
        """
        Clears answers *in place*
        """
        self.answers.clear()
        self.answer_map = defaultdict(list)

    def remove(self, answer_ids=None, group_instance=None, answer_instance=None):
        """
        Removes answer(s) *in place* from the answer store.

        :param answer_ids: The answer ids to filter results to remove
        :param answer_instance: The answer instance to filter results to remove
        :param group_instance: The group instance to filter results to remove
        """
        for answer in self.filter(answer_ids, group_instance, answer_instance):
            self.answer_map[answer['answer_id']].remove(answer)
            self.answers.remove(answer)

    def get_hash(self):
        """
        Gets unique hash from answers contained within this AnswerStore

        :return: Return a unique hash value
        """
        return hash(json.dumps(self.answers, sort_keys=True))

    def upgrade(self, current_version, schema):

        # Upgrade from version 0 to version 1
        if current_version == 0:
            # Update Date formats
            for answer in self.answers:
                answer_schema = schema.get_answer(answer['answer_id'])

                if answer_schema:
                    if answer_schema['type'] == 'Date':
                        answer['value'] = datetime.strptime(answer['value'], '%d/%m/%Y').strftime('%Y-%m-%d')
                        continue

                    if answer_schema['type'] == 'MonthYearDate':
                        answer['value'] = datetime.strptime(answer['value'], '%m/%Y').strftime('%Y-%m')
                        continue


def number_else_string(text):
    return int(text) if text.isdigit() else text


def natural_order(key):
    """
    Orders a set of items according to

    :param key:
    :return:
    """
    return [number_else_string(c) for c in re.split(r'(\d+)', key)]
