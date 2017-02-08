import re

from collections import OrderedDict


class Answer(object):
    def __init__(self, group_id=None, block_id=None, answer_id=None, value=None, group_instance=0, answer_instance=0, location=None):
        valid = (group_id or answer_id or block_id or value) is not None

        if location:
            assert not (group_id or group_instance or block_id), \
                "Expected either a location object or one or more of group_id, group_instance, block_id params"

            group_id = location.group_id
            group_instance = location.group_instance
            block_id = location.block_id

        if not valid:
            raise ValueError("At least one of 'answer_id', 'group_id', 'block_id' or 'value' must be set for Answer")

        self.group_id = group_id
        self.block_id = block_id
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
        return self.group_id == answer.group_id and \
            self.block_id == answer.block_id and \
            self.answer_id == answer.answer_id and \
            self.group_instance == answer.group_instance and \
            self.answer_instance == answer.answer_instance

    def matches_dict(self, answer_dict):
        """
        Check to see if a dict describes an answer the same as this object.

        :param answer_dict: A dict providing
        :return:
        """

        return self.matches(Answer(
            answer_dict['group_id'],
            answer_dict['block_id'],
            answer_dict['answer_id'],
            "",
            answer_dict['group_instance'],
            answer_dict['answer_instance'],
        ))


class AnswerStore(object):
    """
    An object that stores and updates a collection of answers, ready for serialisation
    via the Questionnaire Store.
    """

    def __init__(self, existing_answers=None):
        self.answers = existing_answers or []

    @staticmethod
    def _validate(answer):
        if not isinstance(answer, Answer):
            raise TypeError("Method only supports Answer argument type")

    def add(self, answer):
        """
        Add a new answer into the answer store.

        :param answer: A dict of flattened answer details.
        """
        self._validate(answer)

        answer_to_add = answer.__dict__.copy()

        if self.exists(answer):
            raise ValueError("Answer instance already exists in store")
        else:
            self.answers.append(answer_to_add)

    def update(self, answer):
        """
        Update the value of an answer already in the answer store.

        :param answer: A dict of flattened answer details.
        """
        position = self.find(answer)

        if position is None:
            raise ValueError("Answer instance does not exist in store")
        else:
            self.answers[position]['value'] = answer.value

    def add_or_update(self, answer):
        """
        Add a new answer into the answer store, or update if it exists.

        :param answer: An answer object.
        """
        if self.exists(answer):
            self.update(answer)
        else:
            self.add(answer)

    def get(self, answer):
        """
        Returns the value of an answer.

        :param answer: The ids for the answer to return
        :return: The value of the answer found
        """
        position = self.find(answer)

        if position is None:
            raise ValueError("Answer instance does not exist in store")
        else:
            return self.answers[position]['value']

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

    def exists(self, answer):
        """
        Checks to see if an answer exists in the answer store.

        :param answer: A dict of flattened answer details.
        :return: True if the answer is in the store, False if not.
        """
        return self.find(answer) is not None

    def count(self, answer):
        """
        Count of the number of instances of an answer in the answer store.

        :param answer: A dict of flattened answer details.
        :return: 0 if the answer doesn't exist, otherwise the number of instances.
        """
        self._validate(answer)

        return len(self.filter(answer.group_id, answer.block_id, answer.answer_id, answer.group_instance, answer.answer_instance))

    def filter(self, group_id=None, block_id=None, answer_id=None, group_instance=None, answer_instance=None, location=None, limit=None):
        """
        Find all answers in the answer store for a given set of filter parameter matches.
        If no filter parameters are passed it returns a copy of the list of all answers.

        :param answer_id: The answer id to filter results by
        :param block_id: The block id to filter results by
        :param group_id: The group id to filter results by
        :param answer_instance: The answer instance to filter results by
        :param group_instance: The group instance to filter results by
        :param location: The location to filter results by (takes precedence over group_id, group_instance and block_id)
        :param limit: Limit the number of answers returned
        :return: Return a list of answers which satisfy the filter criteria
        """
        filtered = []
        filter_vars = {
            "answer_id": answer_id,
            "block_id": block_id,
            "group_id": group_id,
            "answer_instance": answer_instance,
            "group_instance": group_instance,
        }
        if location:
            assert not (group_id or group_instance or block_id), \
                "Expected either a location object or one or more of group_id, group_instance, block_id params"

            filter_vars['group_id'] = location.group_id
            filter_vars['group_instance'] = location.group_instance
            filter_vars['block_id'] = location.block_id

        for answer in self.answers:
            matches = True
            for k, v in filter_vars.items():
                if v is not None:
                    matches = matches and answer[k] == v
            if matches:
                filtered.append(answer)
                if limit and len(filtered) == limit:
                    break
        return filtered

    def clear(self):
        self.answers.clear()

    def map(self, group_id=None, block_id=None, answer_id=None, group_instance=None, answer_instance=None):
        """
        Maps the answers in this store to a dictionary of key, value answers. Keys include instance
        id's when the instance id is non zero.

        :param answer_id:
        :param block_id:
        :param group_id:
        :param answer_instance:
        :param group_instance:
        :return:
        """
        result = {}
        for answer in self.filter(group_id, block_id, answer_id, group_instance, answer_instance):
            answer_id = answer['answer_id']
            answer_id += "_" + str(answer['answer_instance']) if answer['answer_instance'] > 0 else ''

            result[answer_id] = answer['value']

        return OrderedDict(sorted(result.items(), key=lambda t: natural_order(t[0])))

    def remove_answer(self, answer):
        """
        Removes an answer from the answer store.

        :param answer: A dict of flattened answer details.
        """
        index = self.find(answer)
        if index is not None:
            del self.answers[index]

    def remove(self, group_id=None, block_id=None, answer_id=None, group_instance=None, answer_instance=None, location=None):
        """
        Removes answer(s) from the answer store.

        :param answer_id: The answer id to filter results to remove
        :param block_id: The block id to filter results to remove
        :param group_id: The group id to filter results to remove
        :param answer_instance: The answer instance to filter results to remove
        :param group_instance: The group instance to filter results to remove
        :param location: The location to filter results to remove (takes precedence over group_id, group_instance and block_id)
        """

        for answer in self.filter(group_id, block_id, answer_id, group_instance, answer_instance, location):
            self.answers.remove(answer)


def number_else_string(text):
    return int(text) if text.isdigit() else text


def natural_order(key):
    """
    Orders a set of items according to
    :param key:
    :return:
    """
    return [number_else_string(c) for c in re.split(r'(\d+)', key)]


def iterate_over_instance_ids(answer_instances):
    """
    Iterates over a collection of answer instances yielding the answer Id and answer instance Id.
    :param answer_instances: A list of raw answer_instance_ids
    :return: Tuple containing the answer Id and answer instance Id.
    """

    answer_instance_ids = sorted(answer_instances, key=natural_order)

    for answer_instance_id in answer_instance_ids:
        answer_id, answer_index = extract_answer_instance_id(answer_instance_id)
        yield answer_id, answer_index


def extract_answer_instance_id(answer_instance_id):
    matches = re.match(r'^(.+?)_(\d+)$', answer_instance_id)
    if matches:
        answer_id, index = matches.groups()
    else:
        answer_id = answer_instance_id
        index = 0

    return answer_id, int(index)
