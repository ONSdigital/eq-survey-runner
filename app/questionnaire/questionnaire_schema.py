from collections import OrderedDict, defaultdict

from flask_babel import force_locale

from app.validation.error_messages import error_messages

DEFAULT_LANGUAGE_CODE = 'en'
LIST_COLLECTOR_CHILDREN = ['ListAddQuestion', 'ListEditQuestion', 'ListRemoveQuestion']


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
    def answers(self):
        return self._answers_by_id.values()

    def get_section(self, section_id):
        return self._sections_by_id.get(section_id)

    def get_group(self, group_id):
        return self._groups_by_id.get(group_id)

    def get_block(self, block_id):
        return self._blocks_by_id.get(block_id)

    def get_block_for_answer_id(self, answer_id):
        answers = self.get_answers(answer_id)
        # All matching questions / answers must be within the same block
        questions = self.get_questions(answers[0]['parent_id'])
        return self.get_block(questions[0]['parent_id'])

    def get_questions(self, question_id):
        """ Return a list of questions matching some question id
        This includes all questions inside variants
        """
        return self._questions_by_id.get(question_id)

    def get_answers(self, answer_id):
        """ Return a list of answers matching some answer id
        This includes all matching answers inside variants
        """
        return self._answers_by_id.get(answer_id)

    def get_section_by_block_id(self, block_id):
        block = self.get_block(block_id)
        group = self.get_group(block['parent_id'])
        return self.get_section(group['parent_id'])

    def group_has_questions(self, group_id):
        for block in self.get_group(group_id)['blocks']:
            if block['type'] == 'Question':
                return True

        return False

    def get_first_block_id_for_group(self, group_id):
        group = self.get_group(group_id)
        if group:
            return group['blocks'][0]['id']

    def get_group_by_block_id(self, block_id):
        block = self.get_block(block_id)
        if block['type'] in LIST_COLLECTOR_CHILDREN:
            parent = self.get_block(block['parent_id'])
            return self.get_group(parent['parent_id'])
        return self.get_group(block['parent_id'])

    @classmethod
    def get_answer_ids_for_question(cls, question):
        answer_ids = set()

        for answer in question.get('answers', []):
            answer_ids.add(answer['id'])
            for option in answer.get('options', []):
                if 'detail_answer' in option:
                    answer_ids.add(option['detail_answer']['id'])

        return answer_ids

    def get_answer_ids_for_block(self, block_id):
        block = self.get_block(block_id)
        answer_ids = set()

        if block:
            questions = self.get_all_questions_for_block(block)

            for question in questions:
                answer_ids.update(self.get_answer_ids_for_question(question))

        return answer_ids

    def get_summary_and_confirmation_blocks(self):
        return [
            block['id'] for block in self.blocks
            if block['type'] in ('Summary', 'Confirmation')
        ]

    @staticmethod
    def get_all_questions_for_block(block):
        all_questions = []
        if block:
            if block.get('question'):
                all_questions.append(block['question'])
            elif block.get('question_variants'):
                for variant in block['question_variants']:
                    all_questions.append(variant['question'])

            return all_questions
        return []

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

    def get_list_collector_for_block_id(self, block_id):
        block = self.get_block(block_id)
        return self.get_block(block['parent_id'])

    def is_block_list_collector_child(self, block_id):
        block = self.get_block(block_id)
        if not block:
            return False

        return block['type'] in LIST_COLLECTOR_CHILDREN

    def _parse_schema(self):
        self._sections_by_id = self._get_sections_by_id()
        self._groups_by_id = get_nested_schema_objects(self._sections_by_id, 'groups')
        self._blocks_by_id = self._get_blocks_by_id()
        self._questions_by_id = self._get_questions_by_id()
        self._answers_by_id = self._get_answers_by_id()
        self.error_messages = self._get_error_messages()

    def _get_blocks_by_id(self):
        blocks = defaultdict(list)

        for group in self._groups_by_id.values():
            for block in group['blocks']:
                block['parent_id'] = group['id']
                blocks[block['id']] = block

                if block['type'] == 'ListCollector':
                    for nested_block_name in ['add_block', 'edit_block', 'remove_block']:
                        nested_block = block[nested_block_name]
                        nested_block['parent_id'] = block['id']
                        blocks[nested_block['id']] = nested_block

        return blocks

    def _get_questions_by_id(self):
        questions_by_id = defaultdict(list)

        for block in self._blocks_by_id.values():
            questions = self.get_all_questions_for_block(block)
            for question in questions:
                question['parent_id'] = block['id']
                questions_by_id[question['id']].append(question)

        return questions_by_id

    def _get_answers_by_id(self):
        answers_by_id = defaultdict(list)

        for question_set in self._questions_by_id.values():
            for question in question_set:
                for answer in question['answers']:
                    answer['parent_id'] = question['id']
                    answers_by_id[answer['id']].append(answer)
                    for option in answer.get('options', []):
                        if 'detail_answer' in option:
                            option['detail_answer']['parent_id'] = question['id']
                            answers_by_id[option['detail_answer']['id']].append(option['detail_answer'])

        return answers_by_id

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
