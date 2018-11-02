import itertools
from collections import OrderedDict

from flask_babel import force_locale

from app.questionnaire.answer_dependencies import get_answer_dependencies
from app.questionnaire.group_dependencies import get_group_dependencies
from app.validation.error_messages import error_messages

DEFAULT_LANGUAGE_CODE = 'en'


class QuestionnaireSchema:  # pylint: disable=too-many-public-methods
    def __init__(self, questionnaire_json, language_code=DEFAULT_LANGUAGE_CODE):
        self.json = questionnaire_json
        self.language_code = language_code
        self._parse_schema()

    @property
    def sections(self):
        return self._sections_by_id.values()

    @property
    def groups(self):
        return self._groups_by_id.values()

    @property
    def blocks(self):
        return self._blocks_by_id.values()

    @property
    def questions(self):
        return self._questions_by_id.values()

    @property
    def answers(self):
        return self._answers_by_id.values()

    @property
    def answer_dependencies(self):
        return self._answer_dependencies

    @property
    def group_dependencies(self):
        return self._group_dependencies.group_dependencies

    def get_section(self, section_id):
        return self._sections_by_id.get(section_id)

    def get_group(self, group_id):
        return self._groups_by_id.get(group_id)

    def get_block(self, block_id):
        return self._blocks_by_id.get(block_id)

    def get_question(self, question_id):
        return self._questions_by_id.get(question_id)

    def get_answer(self, answer_id):
        return self._answers_by_id.get(answer_id)

    def get_section_by_block_id(self, block_id):
        block = self.get_block(block_id)
        group = self.get_group(block['parent_id'])
        return self.get_section(group['parent_id'])

    def get_groups_that_repeat_with_answer_id(self, answer_id):
        for group in self.groups:
            repeating_rule = self.get_repeat_rule(group)
            if repeating_rule:
                if repeating_rule.get('answer_id') == answer_id:
                    yield group

    def group_has_questions(self, group_id):
        for block in self.get_group(group_id)['blocks']:
            if block['type'] == 'Question':
                return True

        return False

    def get_first_block_id_for_group(self, group_id):
        group = self.get_group(group_id)
        if group:
            return group['blocks'][0]['id']

    def get_answer_ids_for_group(self, group_id):
        answer_ids = []
        group = self.get_group(group_id)
        for block in group['blocks']:
            answer_ids.extend(self.get_answer_ids_for_block(block['id']))

        return answer_ids

    def get_answers_by_id_for_block(self, block_id):
        block = self.get_block(block_id)
        if block:
            answer_lists = (
                question.get('answers', [])
                for question in block.get('questions', [])
            )
            return {
                answer['id']: answer
                for answer in itertools.chain.from_iterable(answer_lists)
            }

        return {}

    def get_answer_ids_for_block(self, block_id):
        return list(self.get_answers_by_id_for_block(block_id).keys())

    def get_answers_for_block(self, block_id):
        return list(self.get_answers_by_id_for_block(block_id).values())

    def get_answers_that_repeat_in_block(self, block_id):
        block = self.get_block(block_id)

        for question in block.get('questions', []):
            if question['type'] == 'RepeatingAnswer':
                for answer in question['answers']:
                    yield answer

    def get_summary_and_confirmation_blocks(self):
        return [
            block['id'] for block in self.blocks
            if block['type'] in ('Summary', 'Confirmation')
        ]

    def get_parent_options_for_block(self, block_id):
        options_with_children = {}

        for answer_json in self.get_answers_for_block(block_id):
            if answer_json['type'] in ['Checkbox', 'Radio']:
                answer_options_with_children = {
                    answer_json['id']: {
                        'index': index,
                        'child_answer_id': o['child_answer_id'],
                    }
                    for index, o in enumerate(answer_json['options']) if 'child_answer_id' in o}

                options_with_children.update(answer_options_with_children)
        return options_with_children

    def get_group_dependencies(self, group_id):
        return self.group_dependencies.get(group_id)

    def get_group_dependencies_group_drivers(self):
        return self.group_dependencies['group_drivers']

    def get_group_dependencies_block_drivers(self):
        return self.group_dependencies['block_drivers']

    def location_requires_group_instance(self, location):
        return bool(self.group_dependencies.get(location.group_id)
                    or location.group_id in self.get_group_dependencies_group_drivers()
                    or location.block_id in self.get_group_dependencies_group_drivers()
                    or location.block_id in self.get_group_dependencies_block_drivers())

    def block_has_question_type(self, block_id, question_type):
        block = self.get_block(block_id)
        for question in block.get('questions', []):
            if question['type'] == question_type:
                return True
        return False

    @staticmethod
    def get_repeat_rule(group):
        if 'routing_rules' in group:
            for rule in group['routing_rules']:
                if 'repeat' in rule.keys():
                    return rule['repeat']

    @staticmethod
    def get_questions_for_block(block_json):
        for question_json in block_json.get('questions', []):
            yield question_json

    @staticmethod
    def is_summary_section(section):
        for group in section['groups']:
            if QuestionnaireSchema.is_summary_group(group):
                return True

        return False

    @staticmethod
    def is_summary_group(group):
        for block in group['blocks']:
            if block['type'] == 'Summary':
                return True

        return False

    @staticmethod
    def is_confirmation_section(section):
        for group in section['groups']:
            if QuestionnaireSchema.is_confirmation_group(group):
                return True

        return False

    @staticmethod
    def is_confirmation_group(group):
        for block in group['blocks']:
            if block['type'] == 'Confirmation':
                return True

        return False

    def is_repeating_answer_type(self, answer_id):
        answer = self.get_answer(answer_id)
        question = self.get_question(answer['parent_id'])
        return answer.get('type') == 'Checkbox' or question['type'] == 'RepeatingAnswer'

    def block_drives_multiple_groups(self, block_id):
        driver_count = 0

        for driven_group in self.group_dependencies:
            if driven_group in ['group_drivers', 'block_drivers']:
                continue

            if block_id in self.group_dependencies[driven_group]:
                driver_count += 1

        return driver_count > 1

    def answer_is_in_repeating_group(self, answer_id):
        answer = self.get_answer(answer_id)
        question = self.get_question(answer['parent_id'])
        block = self.get_block(question['parent_id'])
        group = self.get_group(block['parent_id'])

        repeat_rule = self.get_repeat_rule(group)
        return repeat_rule

    def _parse_schema(self):
        self._sections_by_id = self._get_sections_by_id()
        self._groups_by_id = get_nested_schema_objects(self._sections_by_id, 'groups')
        self._blocks_by_id = get_nested_schema_objects(self._groups_by_id, 'blocks')
        self._questions_by_id = get_nested_schema_objects(self._blocks_by_id, 'questions')
        self._answers_by_id = get_nested_schema_objects(self._questions_by_id, 'answers')
        self.error_messages = self._get_error_messages()
        self._answer_dependencies = get_answer_dependencies(self)
        self._group_dependencies = get_group_dependencies(self)

    def _get_sections_by_id(self):
        return OrderedDict(
            (section['id'], section)
            for section in self.json.get('sections', [])
        )

    def _get_error_messages(self):
        # Force translation of global error messages (stored as LazyString's) into the language of the schema.
        with force_locale(self.language_code):
            messages = {k: str(v) for k, v in error_messages.items()}

        if 'messages' in self.json:
            messages.update(self.json['messages'])

        return messages

    def _get_answers_by_id_for_question(self, question_id):
        question = self.get_question(question_id)

        return {
            answer['id']: answer
            for answer in question.get('answers', [])
        }

    def get_answer_ids_for_question(self, question_id):
        """ get answer ids associated with a specific question_id """
        return list(self._get_answers_by_id_for_question(question_id).keys())

    def get_block_id_for_answer_id(self, answer_id):
        answer = self.get_answer(answer_id)
        question = self.get_question(answer['parent_id'])
        block = self.get_block(question['parent_id'])

        return block['id']


def get_nested_schema_objects(parent_object, list_key):
    """
    Generic method to extract a flattened list of child objects from a parent
    object and return an ID-keyed dictionary of those child objects.

    This method also patches on a `parent_id` attribute to each child object.

    :param parent_object: dict containing a list
    :param list_key: key of the nested list to extract
    """
    nested_objects = OrderedDict()

    for parent_id, child_object in parent_object.items():
        for child_list_object in child_object.get(list_key, []):
            # patch the ID of the parent onto the object
            child_list_object['parent_id'] = parent_id
            nested_objects[child_list_object['id']] = child_list_object

    return nested_objects
