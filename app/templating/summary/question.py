import collections

from app.templating.summary.answer import Answer
from app.templating.utils import get_question_title


class Question:

    def __init__(self, question_schema, answer_store, metadata, schema):
        self.id = question_schema['id']
        self.type = question_schema['type']
        self.schema = schema
        self.answer_schemas = iter(question_schema['answers'])

        self.title = (get_question_title(question_schema, answer_store, schema, metadata)
                      or question_schema['answers'][0]['label'])
        self.number = question_schema.get('number', None)
        self.answers = self._build_answers(answer_store, question_schema)

    @staticmethod
    def _get_answers(answer_store, answer_id):
        answers = answer_store.filter(answer_ids=[answer_id]).values()

        return answers or [None]

    def _get_answer(self, answer_store, answer_id):
        return self._get_answers(answer_store, answer_id)[0]

    def _build_answers(self, answer_store, question_schema):
        summary_answers = []

        for answer_schema in self.answer_schemas:
            answer_values = self._get_answers(answer_store, answer_schema['id'])
            for answer_value in answer_values:

                answer = self._build_answer(answer_store, question_schema, answer_schema, answer_value)

                summary_answer = Answer(answer_schema, answer).serialize()

                summary_answers.append(summary_answer)

        if question_schema['type'] == 'MutuallyExclusive':
            exclusive_option = summary_answers[-1]['value']
            if exclusive_option:
                return summary_answers[-1:]
            return summary_answers[:-1]

        return summary_answers

    def _build_answer(self, answer_store, question_schema, answer_schema, answer_value=None):
        if answer_value is None:
            return None

        if question_schema['type'] == 'DateRange':
            return self._build_date_range_answer(answer_store, answer_value)

        if answer_schema['type'] == 'Dropdown':
            return self._build_dropdown_answer(answer_value, answer_schema)

        answer_builder = {
            'Checkbox': self._build_checkbox_answers,
            'Radio': self._build_radio_answer,
        }

        if answer_schema['type'] in answer_builder.keys():
            return answer_builder[answer_schema['type']](answer_value, answer_schema, answer_store)

        return answer_value

    def _build_checkbox_answers(self, answer, answer_schema, answer_store):
        multiple_answers = []
        CheckboxSummaryAnswer = collections.namedtuple('CheckboxSummaryAnswer', 'label detail_answer_value')
        for option in answer_schema['options']:
            if option['value'] in answer:
                detail_answer_value = self._get_detail_answer_value(option, answer_store)

                multiple_answers.append(CheckboxSummaryAnswer(label=option['label'],
                                                              detail_answer_value=detail_answer_value))

        return multiple_answers or None

    def _build_date_range_answer(self, answer_store, answer):
        next_answer = next(self.answer_schemas)
        to_date = self._get_answer(answer_store, next_answer['id'])
        return {
            'from': answer,
            'to': to_date,
        }

    def _build_radio_answer(self, answer, answer_schema, answer_store):
        for option in answer_schema['options']:
            if answer == option['value']:
                detail_answer_value = self._get_detail_answer_value(option, answer_store)
                return {
                    'label': option['label'],
                    'detail_answer_value': detail_answer_value,
                }

    def _get_detail_answer_value(self, option, answer_store):
        if 'detail_answer' in option:
            return self._get_answer(answer_store, option['detail_answer']['id'])

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
