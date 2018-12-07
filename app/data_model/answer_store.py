import itertools

from collections import defaultdict
from datetime import datetime
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

    EQ_MAX_NUM_REPEATS = 25

    def __init__(self, existing_answers=None):
        if isinstance(existing_answers, list):
            self.answer_map = self._build_map(existing_answers or [])
        else:
            self.answer_map = existing_answers or defaultdict(list)

    def __iter__(self):
        return iter((answer for answers in self.answer_map.values() for answer in answers))

    def __len__(self):
        return sum(len(answers) for answers in self.answer_map.values())

    def __eq__(self, other):
        return self.answer_map == other.answer_map

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
        position = self.find(answer)

        if position is None:
            answer_to_add = vars(answer).copy()
            self.answer_map[answer_to_add['answer_id']].append(answer_to_add)
        else:
            self.answer_map[answer.answer_id][position]['value'] = answer.value

    def find(self, answer):
        """
        Returns the position of an answer if it exists

        :param answer: The answer to search for
        :return: The position the answer exists at, None if it doesn't exist
        """
        self._validate(answer)

        if answer.answer_id in self.answer_map:
            for index, existing in enumerate(self.answer_map[answer.answer_id]):
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

    def filter(self, answer_ids=None, group_instance=None, group_instance_id=None, answer_instance=None, limit=None):
        """
        Find all answers in the answer store for a given set of filter parameter matches.
        If no filter parameters are passed it returns a copy of the instance.

        :param answer_ids: The answer ids to filter results by
        :param answer_instance: The answer instance to filter results by
        :param group_instance_id: The group instance ID to filter results by
        :param group_instance: The group instance to filter results by
        :param limit: True | False Limit the number of answers returned
        :return: Return a new AnswerStore object with filtered answers for chaining
        """
        filtered = []

        filter_vars = {
            'answer_id': answer_ids,
            'answer_instance': answer_instance,
            'group_instance_id': group_instance_id,
            'group_instance': group_instance,
        }

        if answer_ids:
            answers = itertools.chain.from_iterable(self.answer_map.get(answer_id, []) for answer_id in answer_ids)
        else:
            answers = self

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
        self.answer_map.clear()

    def remove(self, answer_ids=None, group_instance=None, answer_instance=None):
        """
        Removes answer(s) *in place* from the answer store.

        :param answer_ids: The answer ids to filter results to remove
        :param answer_instance: The answer instance to filter results to remove
        :param group_instance: The group instance to filter results to remove
        """
        for answer in self.filter(answer_ids, group_instance=group_instance, answer_instance=answer_instance):
            self.answer_map[answer['answer_id']].remove(answer)

    def remove_answer(self, answer):
        """
        Removes answer *in place* from the answer store.

        :param answer: The answer to remove
        """

        if answer in self.answer_map[answer['answer_id']]:
            self.answer_map[answer['answer_id']].remove(answer)

    def get_hash(self):
        """
        Gets unique hash from answers contained within this AnswerStore

        :return: Return a unique hash value
        """
        return hash(json.dumps(self.answer_map, sort_keys=True))

    def upgrade(self, current_version, schema):
        """
            Upgrade the answer_store to the latest version

            :param current_version: The current version integer of the answer store
            :param schema: The new schema
        """
        versions = sorted(list(UPGRADE_TRANSFORMS.keys()))

        # Find the next version in the list after the current version
        versions_to_upgrade_to = [v for v in versions if v > current_version]

        for upgrade_to_version in versions_to_upgrade_to:
            transform = UPGRADE_TRANSFORMS[upgrade_to_version]
            logger.info('Upgrading answer store version', current_version=current_version, new_version=upgrade_to_version, transform=transform.__name__)
            transform(self, schema)


def upgrade_0_to_1_update_date_formats(answer_store, schema):
    """ Updates the date format """
    for answer in answer_store:
        answer_schema = schema.get_answer(answer['answer_id'])

        if answer_schema:
            if answer_schema['type'] == 'Date':
                answer['value'] = datetime.strptime(answer['value'], '%d/%m/%Y').strftime('%Y-%m-%d')
                continue

            if answer_schema['type'] == 'MonthYearDate':
                answer['value'] = datetime.strptime(answer['value'], '%m/%Y').strftime('%Y-%m')
                continue


def upgrade_1_to_2_add_group_instance_id(answer_store, schema):
    """ Answers should have a `group_instance_id` ready for more complex group repeat rules. """
    from app.questionnaire.location import Location
    from app.helpers.schema_helpers import get_group_instance_id

    for answer in answer_store:
        # Happily, parent_id's are patched on to the schema for each nested level, so we can
        # retrieve the block_id and group_id for the answer we're processing here.
        answer_schema = schema.get_answer(answer['answer_id'])
        question = schema.get_question(answer_schema['parent_id'])
        block_id = question['parent_id']
        block = schema.get_block(question['parent_id'])
        group_id = block['parent_id']

        location = Location(
            group_id=group_id,
            group_instance=answer['group_instance'],
            block_id=block_id,
        )
        # `get_group_instance_id` handles providing a consistent group_instance_id
        answer['group_instance_id'] = get_group_instance_id(schema, answer_store, location, answer['answer_instance'])


def upgrade_3_to_4_remove_empty_answers(answer_store, schema):  # pylint: disable=unused-argument
    """ Previously, we stored [] and '' as answer values for unanswered, but completed answers.

    This was changed to avoid storing unanswered values entirely, so this upgrade will
    remove any answers in the store that have 'empty' answer values
    """
    answer_store_copy = answer_store.copy()

    for answer in answer_store:
        if answer['value'] in ('', [], None):
            answer_store_copy.remove_answer(answer)

    answer_store = answer_store_copy


# Dictionary specifying upgrade methods. Key should be the version to upgrade to.
UPGRADE_TRANSFORMS = {
    1: upgrade_0_to_1_update_date_formats,
    2: upgrade_1_to_2_add_group_instance_id,
    4: upgrade_3_to_4_remove_empty_answers,
}
