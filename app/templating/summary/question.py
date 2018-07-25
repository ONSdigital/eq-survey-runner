import collections

from app.templating.summary.answer import Answer
from app.templating.utils import get_question_title


class Question:

    def __init__(self, question_schema, answer_store, metadata):
        self.id = question_schema['id']
        self.type = question_schema['type']

        answer_schemas = iter(question_schema['answers'])

        # Using group instance as 0 for now as summary rendering context only has knowledge of current locations group instance (i.e. 0)
        self.title = get_question_title(question_schema, answer_store, metadata, group_instance=0) or question_schema['answers'][0]['label']
        self.number = question_schema.get('number', None)
        self.answers = self._build_answers(answer_store, question_schema, answer_schemas)

    @staticmethod
    def _get_answers(answer_store, answer_id):
        return answer_store.filter(answer_ids=[answer_id]).escaped().values()

    def _get_answer(self, answer_store, answer_id):
        try:
            return self._get_answers(answer_store, answer_id)[0]
        except IndexError:
            return None

    def _build_answers(self, answer_store, question_schema, answer_schemas):
        summary_answers = []
        for answer_schema in answer_schemas:
            if 'parent_answer_id' in answer_schema:
                continue
            if question_schema['type'] == 'RepeatingAnswer':
                for answer_value in self._get_answers(answer_store, answer_schema['id']):
                    answer = self._build_answer(answer_store, question_schema, answer_schema, answer_schemas,
                                                answer_value)
                    summary_answers.append(Answer(answer_schema, answer))
            else:
                answer_value = self._get_answer(answer_store, answer_schema['id'])
                answer = self._build_answer(answer_store, question_schema, answer_schema, answer_schemas, answer_value)
                child_answer_value = self._find_other_value_in_answers(answer_store, answer_schema, answer)
                summary_answers.append(Answer(answer_schema, answer, child_answer_value).serialize())
        return summary_answers

    def _find_other_value_in_answers(self, answer_store, answer_schema, answer):
        if answer is not None and 'options' in answer_schema:
            options = answer_schema['options']
            for option in options:
                if option['label'] in [a[0] for a in answer] or option['label'] == answer:
                    if 'child_answer_id' in option:
                        return self._get_answer(answer_store, option['child_answer_id'])
        return None

    def _build_answer(self, answer_store, question_schema, answer_schema, answer_schemas, answer_value=None):
        if answer_value is None:
            return None
        if question_schema['type'] == 'DateRange':
            return self._build_date_range_answer(answer_store, answer_value, answer_schemas)
        if answer_schema['type'] in ['Checkbox', 'MutuallyExclusiveCheckbox']:
            checkbox_answers = self._build_checkbox_answers(answer_value, answer_schema)
            return checkbox_answers or None
        if answer_schema['type'] == 'Radio':
            return self._build_radio_answer(answer_value, answer_schema)
        if answer_schema['type'] == 'Dropdown':
            return self._build_dropdown_answer(answer_value, answer_schema)
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
        return multiple_answers

    def _build_date_range_answer(self, answer_store, answer, answer_schemas):
        next_answer = next(answer_schemas)
        to_date = self._get_answer(answer_store, next_answer['id'])
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
