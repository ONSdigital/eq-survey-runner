import re

from collections import OrderedDict


class AnswerStore(object):
    """
    An object that stores the flattened structure of AnswerStates.
    It is referenced by the answers property in the QuestionnaireStore.
    """

    def __init__(self, existing_answers=None):
        self.answers = existing_answers if existing_answers is not None else []

    def add(self, answer):
        """
        Add a new answer into the answer store.

        :param answer: A dict of flattened answer details.
        :return: None.
        """
        answer_to_add = answer.copy()

        if self.exists(answer_to_add):
            self.update(answer)
        else:
            self.answers.append(answer_to_add)

    def update(self, answer):
        """
        Update the value of an answer already in the answer store.

        :param answer: A dict of flattened answer details.
        :return:
        """
        for index, existing in enumerate(self.answers):
            if self.same(existing, answer):
                self.answers[index]['value'] = answer['value']
                break

    def remove(self, answer):
        """
        Removes an answer from the answer store.

        :param answer: A dict of flattened answer details.
        """
        found_answers = self.find(answer)
        for found in found_answers:
            self.answers.remove(found)

    def find(self, answer):
        """
        Finds all instances of an answer.

        :param answer: A dict of flattened answer details.
        :return:
        """
        found = []
        for existing in self.answers:
            if self.same(answer, existing):
                found.append(existing)

        return found

    def exists(self, answer):
        """
        Checks to see if an answer exists in the answer store.

        :param answer: A dict of flattened answer details.
        :return: True if the answer is in the store, False if not.
        """
        return self.count(answer) > 0

    def count(self, answer):
        """
        Count of the number of instances of an answer in the answer store.

        :param answer: A dict of flattened answer details.
        :return: 0 if the answer doesn't exist, otherwise the number of instances.
        """
        return len(self.find(answer))

    @staticmethod
    def same(first, second):
        """
        Check to see if two answers are the same.
        Two answers are considered the same if they share the same block, question, answer and instance Id.

        :param first: A dict of flattened answer details
        :param second: A dict of flattened answer details.
        :return: True if both answers are the same, otherwise False.
        """
        return (first['block_id'] == second['block_id'] and
                first['question_id'] == second['question_id'] and
                first['answer_id'] == second['answer_id'] and
                first['answer_instance'] == second['answer_instance'])

    def filter(self, filter_vars):
        """
        Find all answers in the answer store for a given set of filter parameter matches.

        :param filter_vars: The filter parameters to match against.
        :return: A list of answer instances that match the filter.
        """
        filtered = []
        for answer in self.answers:
            matches = True
            for k, v in filter_vars.items():
                if k in ['block_id', 'question_id', 'answer_id', 'answer_instance']:
                    matches = matches and answer[k] == v
            if matches:
                filtered.append(answer)
        return filtered

    def clear(self):
        self.answers.clear()

    def map(self, filter_vars=None):
        """
        Maps the answers in this store to a dictionary of key, value answers. Keys include instance
        id's when the instance id is non zero.

        :param filter_vars:
        :return:
        """
        result = {}

        answers = self.filter(filter_vars) if filter_vars else self.answers

        for answer in answers:
            answer_id = answer['answer_id']
            answer_id += "_" + str(answer['answer_instance']) if answer['answer_instance'] > 0 else ''

            result[answer_id] = answer['value']

        return OrderedDict(sorted(result.items(), key=lambda t: natural_order(t[0])))


def atoi(text):
    return int(text) if text.isdigit() else text


def natural_order(key):
    return [atoi(c) for c in re.split('(\d+)', key)]
