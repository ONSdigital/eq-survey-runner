from app.validation.error_messages import error_messages


class QuestionnaireSchema(object):

    def __init__(self, questionnaire_json):
        self.json = questionnaire_json
        self._groups_by_id = self._get_groups_by_id()
        self._blocks_by_id = self._get_blocks_by_id()
        self._answers_by_id = self._get_answers_by_id()
        self.error_messages = self._get_error_messages()
        self.aliases = self._get_aliases()

    def _get_groups_by_id(self):
        groups = {}
        for group in self.json.get('groups', []):
            groups[group.get('id')] = group

        return groups

    def _get_blocks_by_id(self):
        blocks = {}
        for group in self.json.get('groups', []):
            for block in group['blocks']:
                blocks[block.get('id')] = block

        return blocks

    def _get_answers_by_id(self):
        answers = {}
        for block in self.get_blocks():
            for question in self.get_questions_for_block(block):
                for answer in question['answers']:
                    answers[answer['id']] = answer

        return answers

    def _get_error_messages(self):
        messages = error_messages.copy()
        if 'messages' in self.json:
            for key, message in self.json['messages'].items():
                messages[key] = message

        return messages

    def _get_aliases(self):
        aliases = {}
        for block in self.get_blocks():
            for question in self.get_questions_for_block(block):
                for answer in question['answers']:
                    if 'alias' in answer:
                        if answer['alias'] in aliases:
                            raise Exception('Duplicate alias found: ' + answer['alias'])
                        aliases[answer['alias']] = {
                            'answer_id': answer['id'],
                            'repeats': answer['type'] == 'Checkbox' or question['type'] == 'RepeatingAnswer',
                        }

        return aliases

    def get_sections(self):
        navigation = self.json.get('navigation')

        if navigation:
            return navigation.get('sections')

        return None

    def get_groups(self):
        for group in self.json.get('groups', []):
            yield group

    def get_group(self, group_id):
        return self._groups_by_id.get(group_id)

    def get_groups_that_repeat_with_answer_id(self, answer_id):
        for group in self.get_groups():
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

    def get_blocks(self):
        for group in self.get_groups():
            for block in group['blocks']:
                yield block

    def get_block(self, block_id):
        return self._blocks_by_id.get(block_id)

    def get_answer_schema_for_answer_id(self, answer_id):
        return self._answers_by_id.get(answer_id)

    def get_answers_by_id_for_block(self, block_id):
        answers = {}
        block = self.get_block(block_id)
        if block:
            for question in block.get('questions', []):
                for answer in question.get('answers', []):
                    answers[answer['id']] = answer

        return answers

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
        blocks = []

        for block in self.get_blocks():
            if block['type'] in ('Summary', 'Confirmation'):
                blocks.append(block['id'])

        return blocks

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
