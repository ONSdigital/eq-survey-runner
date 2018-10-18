import collections

from app.forms.household_relationship_form import build_relationship_choices
from app.templating.summary.answer import Answer
from app.templating.utils import get_question_title


class Question:

    def __init__(self, question_schema, answer_store, metadata, schema, group_instance):
        self.id = question_schema['id'] + '-' + str(group_instance)
        self.type = question_schema['type']
        self.schema = schema
        self.answer_schemas = iter(question_schema['answers'])

        self.title = (get_question_title(question_schema, answer_store, schema, metadata, group_instance=group_instance) or
                      question_schema['answers'][0]['label'])
        self.number = question_schema.get('number', None)
        self.answers = self._build_answers(answer_store, question_schema, group_instance)

    @staticmethod
    def _get_answers(answer_store, answer_id, group_instance):
        answers = answer_store.filter(answer_ids=[answer_id], group_instance=group_instance).values()

        return answers or [None]

    def _get_answer(self, answer_store, answer_id, group_instance):
        return self._get_answers(answer_store, answer_id, group_instance)[0]

    def _build_answers(self, answer_store, question_schema, group_instance):
        summary_answers = []

        for answer_schema in self.answer_schemas:
            if 'parent_answer_id' in answer_schema:
                continue
            else:
                answer_values = self._get_answers(answer_store, answer_schema['id'], group_instance)
                for answer_value in answer_values:

                    answer = self._build_answer(answer_store, question_schema, answer_schema,
                                                group_instance, answer_value)

                    child_answer_value = self._find_other_value_in_answers(answer_store, answer_schema, answer, group_instance)
                    summary_answer = Answer(answer_schema, answer, group_instance, child_answer_value).serialize()

                    if summary_answer['type'] == 'relationship':
                        summary_answer['label'] = self._relationship_answer_label(summary_answer['label'], question_schema['parent_id'],
                                                                                  answer_store, group_instance,
                                                                                  question_schema.get('member_label'),
                                                                                  answer_values.index(answer_value))

                    summary_answers.append(summary_answer)

        if question_schema['type'] == 'MutuallyExclusive':
            exclusive_option = summary_answers[-1]['value']
            if exclusive_option:
                return summary_answers[-1:]
            return summary_answers[:-1]

        return summary_answers

    def _relationship_answer_label(self, answer_label, block_id, answer_store, group_instance, member_label, index):
        group = self.schema.get_group(self.schema.get_block(block_id)['parent_id'])
        answer_ids = []

        repeat_rule = group['routing_rules'][0]['repeat']
        if 'answer_ids' in repeat_rule:
            for answer_id in repeat_rule['answer_ids']:
                answer_ids.append(answer_id)
        if 'answer_id' in repeat_rule:
            answer_ids.append(repeat_rule['answer_id'])

        choice = build_relationship_choices(answer_ids, answer_store, group_instance, member_label)[index]
        label = answer_label % dict(current_person=choice[0], other_person=choice[1])
        return label

    def _find_other_value_in_answers(self, answer_store, answer_schema, answer, group_instance):
        if answer is not None and 'options' in answer_schema:
            options = answer_schema['options']
            for option in options:
                if option['label'] in [a[0] for a in answer] or option['label'] == answer:
                    if 'child_answer_id' in option:
                        return self._get_answer(answer_store, option['child_answer_id'], group_instance)
        return None

    def _build_answer(self, answer_store, question_schema, answer_schema, group_instance, answer_value=None):
        if answer_value is None:
            return None

        if question_schema['type'] == 'DateRange':
            return self._build_date_range_answer(answer_store, answer_value, group_instance)

        answer_builder = {
            'Checkbox': self._build_checkbox_answers,
            'Radio': self._build_radio_answer,
            'Dropdown': self._build_dropdown_answer,
        }

        if answer_schema['type'] in answer_builder.keys():
            return answer_builder[answer_schema['type']](answer_value, answer_schema)

        return answer_value

    @staticmethod
    def _build_checkbox_answers(answer, answer_schema):
        multiple_answers = []
        CheckboxSummaryAnswer = collections.namedtuple('CheckboxSummaryAnswer', 'label should_display_other')
        for option in answer_schema['options']:
            if option['value'] in answer:
                if option['value'].lower() == 'other':
                    summary_option_display_value = option['label']
                    multiple_answers.append(CheckboxSummaryAnswer(label=summary_option_display_value,
                                                                  should_display_other=True))
                else:
                    multiple_answers.append(CheckboxSummaryAnswer(label=option['label'],
                                                                  should_display_other=False))
        return multiple_answers or None

    def _build_date_range_answer(self, answer_store, answer, group_instance):
        next_answer = next(self.answer_schemas)
        to_date = self._get_answer(answer_store, next_answer['id'], group_instance)
        return {
            'from': answer,
            'to': to_date,
        }

    @staticmethod
    def _build_radio_answer(answer, answer_schema):
        for option in answer_schema['options']:
            if option['value'].lower() == 'other' and answer != option['value']:
                return answer if answer else option['label']
            if answer == option['value']:
                return option['label']

    @staticmethod
    def _build_dropdown_answer(answer, answer_schema):
        for option in answer_schema['options']:
            if answer == option['value']:
                return option['label']

    def serialize(self):
        return {
            'id': self.id,
            'type': self.type,
            'title': self.title,
            'number': self.number,
            'answers': self.answers,
        }
