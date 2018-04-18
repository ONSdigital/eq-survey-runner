import itertools
from collections import OrderedDict, defaultdict
from app.validation.error_messages import error_messages


class QuestionnaireSchema(object):  # pylint: disable=too-many-public-methods
    def __init__(self, questionnaire_json):
        self.json = questionnaire_json
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

    def get_answer_dependencies_by_id(self, answer_id):
        return self._answer_dependencies.get(answer_id, [])

    def get_group_and_block_id_by_answer_id(self, answer_id):
        return self._answer_with_block_and_group_id.get(answer_id)

    def get_section_and_group_id_by_block_id(self, block_id):
        return self._block_with_group_and_section_id.get(block_id)

    def get_groups_that_repeat_with_answer_id(self, answer_id):
        for group in self.groups:
            repeating_rule = self.get_repeat_rule(group)
            if repeating_rule and repeating_rule['answer_id'] == answer_id:
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

    def _parse_schema(self):
        self._sections_by_id = self._get_sections_by_id()
        self._groups_by_id = get_nested_schema_objects(self._sections_by_id, 'groups')
        self._blocks_by_id = get_nested_schema_objects(self._groups_by_id, 'blocks')
        self._questions_by_id = get_nested_schema_objects(self._blocks_by_id, 'questions')
        self._answers_by_id = get_nested_schema_objects(self._questions_by_id, 'answers')
        self.error_messages = self._get_error_messages()
        self.aliases = self._get_aliases()
        self._answer_dependencies = self._get_answer_dependencies()
        self._answer_with_block_and_group_id = self._get_answer_block_group_ids()
        self._block_with_group_and_section_id = self._get_block_section_group_ids()

    def _get_sections_by_id(self):
        return OrderedDict(
            (section['id'], section)
            for section in self.json.get('sections', [])
        )

    def _get_error_messages(self):
        messages = error_messages.copy()
        if 'messages' in self.json:
            messages.update(self.json['messages'])

        return messages

    def _get_aliases(self):
        aliases = {}
        for question in self.questions:
            for answer in question.get('answers', []):
                if 'alias' in answer:
                    if answer['alias'] in aliases:
                        raise Exception(
                            'Duplicate alias found: ' + answer['alias'])
                    aliases[answer['alias']] = {
                        'answer_id': answer['id'],
                        'repeats': answer['type'] == 'Checkbox' or question['type'] == 'RepeatingAnswer',
                    }

        return aliases

    def _get_answer_dependencies(self):
        dependencies = defaultdict(list)
        # Answer level dependencies
        for answer in self.answers:
            dependency_id = answer['id']
            if 'min_value' in answer and 'answer_id' in answer['min_value']:
                answer_id = answer['min_value']['answer_id']
                dependencies[answer_id].append(dependency_id)
            if 'max_value' in answer and 'answer_id' in answer['max_value']:
                answer_id = answer['max_value']['answer_id']
                dependencies[answer_id].append(dependency_id)

        # Question level dependencies
        for question in self.questions:
            for calculation in question.get('calculations', []):
                answer_id = calculation.get('answer_id')
                if answer_id:
                    for dependency_id in calculation['answers_to_calculate']:
                        dependencies[answer_id].append(dependency_id)

        return dependencies

    def _get_answer_block_group_ids(self):
        answers_blocks_groups = {}
        for group in self.groups:
            for block in group['blocks']:
                block_group = {
                    'block': block['id'],
                    'group': group['id']
                }
                answer_ids = self.get_answer_ids_for_block(block['id'])
                for answer_id in answer_ids:
                    answers_blocks_groups[answer_id] = block_group

        return answers_blocks_groups

    def _get_block_section_group_ids(self):
        block_section_groups = {}
        for section in self.sections:
            for group in section['groups']:
                section_group = {
                    'section': section['id'],
                    'group': group['id']
                }
                block_ids = (block['id'] for block in group['blocks'])
                for block_id in block_ids:
                    block_section_groups[block_id] = section_group

        return block_section_groups


def get_nested_schema_objects(parent_object, list_key):
    """
    :param parent_object: dict containing a list
    :param list_key: key of the nested list to extract
    """
    lists = (
        obj.get(list_key, [])
        for obj in parent_object.values()
    )
    return OrderedDict(
        (nested_item['id'], nested_item)
        for nested_item in itertools.chain.from_iterable(lists)
    )
