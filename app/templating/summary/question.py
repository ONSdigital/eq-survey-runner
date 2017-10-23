import collections

from app.data_model.answer_store import iterate_over_instance_ids
from app.templating.summary.answer import Answer
from app.questionnaire.rules import evaluate_skip_conditions


class Question:

    def __init__(self, question_schema, answers_map, answer_store, metadata):
        self.id = question_schema['id']
        self.type = question_schema['type']
        self.skip_conditions = question_schema.get('skip_conditions')
        answer_schema = question_schema['answers']
        self.title = question_schema['title'] or answer_schema[0]['label']
        self.number = question_schema.get('number', None)
        self.answers = self._build_answers(question_schema, answer_schema, answers_map)
        self.is_skipped = evaluate_skip_conditions(self.skip_conditions, metadata, answer_store)

    @classmethod
    def _build_answers(cls, question_schema, answer_schema, answers):
        summary_answers = []
        answers_iterator = iter(answer_schema)
        for answer_schema in answers_iterator:  # pylint: disable=redefined-argument-from-local
            if 'parent_answer_id' in answer_schema:
                continue
            if question_schema['type'] == 'RepeatingAnswer':
                for answer_id, answer_index in iterate_over_instance_ids(answers.keys()):
                    if answer_schema['id'] == answer_id:
                        key = answer_id if answer_index == 0 else '_'.join([answer_id, str(answer_index)])
                        answer = cls._build_answer(question_schema, answer_schema, answers, answers_iterator, key)
                        summary_answers.append(Answer(answer_schema, answer))
            else:
                answer = cls._build_answer(question_schema, answer_schema, answers, answers_iterator)
                child_answer_value = cls._find_other_value_in_answers(answer_schema, answer, answers)
                summary_answers.append(Answer(answer_schema, answer, child_answer_value))

        return summary_answers

    @classmethod
    def _find_other_value_in_answers(cls, answer_schema, answer, answers):
        if answer is not None and 'options' in answer_schema:
            options = answer_schema['options']
            for option in options:
                if option['label'] in [a[0] for a in answer] or option['label'] == answer:
                    for child_answer in answers:
                        if 'child_answer_id' in option and child_answer == option['child_answer_id']:
                            return answers[child_answer]
        return None

    @classmethod
    def _build_answer(cls, question_schema, answer_schema, answers, answers_iterator, answer_id=None):
        answer = answers.get(answer_schema['id'] if answer_id is None else answer_id)

        if answer is None:
            return None
        elif question_schema['type'] == 'DateRange':
            return cls._build_data_range_answer(answer, answers, answers_iterator)
        elif answer_schema['type'] == 'Checkbox':
            checkbox_answers = cls._build_checkbox_answers(answer, answer_schema)
            return checkbox_answers or None
        elif answer_schema['type'] == 'Radio':
            return cls._build_radio_answer(answer, answer_schema)
        return answer

    @classmethod
    def _build_checkbox_answers(cls, answer, answer_schema):
        multiple_answers = []
        CheckboxSummaryAnswer = collections.namedtuple('CheckboxSummaryAnswer', 'label should_display_other')
        for option in answer_schema['options']:
            if option['label'] in answer:
                if option['value'].lower() == 'other':
                    summary_option_display_value = option['label']
                    multiple_answers.append(CheckboxSummaryAnswer(label=summary_option_display_value,
                                                                  should_display_other=True))
                else:
                    multiple_answers.append(CheckboxSummaryAnswer(label=option['label'], should_display_other=False))
        return multiple_answers

    @staticmethod
    def _build_data_range_answer(answer, answers, answers_iterator):
        next_answer = next(answers_iterator)
        to_date = answers[next_answer['id']]
        return {
            'from': answer,
            'to': to_date,
        }

    @staticmethod
    def _build_radio_answer(answer, answer_schema):
        for option in answer_schema['options']:
            if option['value'].lower() == 'other' and answer != option['value']:
                return answer if answer else option['label']
            elif answer == option['value']:
                return option['label']
