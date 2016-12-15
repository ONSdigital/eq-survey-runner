from app.questionnaire.rules import evaluate_rule
from app.questionnaire_state.state_repeating_answer_question import iterate_over_instance_ids
from app.templating.summary.answer import Answer


class Question:

    def __init__(self, question_schema, answers):
        self.id = question_schema['id']
        self.type = question_schema['type']
        self.skip_condition = question_schema.get('skip_condition')
        answer_schema = question_schema['answers']
        self.title = question_schema['title'] or answer_schema[0]['label']
        self.answers = self._build_answers(question_schema, answer_schema, answers)

    def is_skipped(self, all_answers):
        if self.skip_condition is not None:
            for when_rule in self.skip_condition['when']:
                answer = all_answers.get(when_rule['id'])
                if not evaluate_rule(when_rule, answer):
                    return False
            return True

        return False

    @classmethod
    def _build_answers(cls, question_schema, answer_schema, answers):
        summary_answers = []
        answers_iterator = iter(answer_schema)
        for answer_schema in answers_iterator:
            if question_schema['type'] == 'RepeatingAnswer':
                for answer_id, answer_index in iterate_over_instance_ids(answers.keys()):
                    if answer_schema['id'] == answer_id:
                        key = answer_id if answer_index == 0 else '_'.join([answer_id, str(answer_index)])
                        answer = cls._build_answer(question_schema, answer_schema, answers, answers_iterator, key)
                        summary_answers.append(Answer(answer_schema, answer))

            else:
                answer = cls._build_answer(question_schema, answer_schema, answers, answers_iterator)
                summary_answers.append(Answer(answer_schema, answer))

        return summary_answers

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
        else:
            return answer

    @classmethod
    def _build_checkbox_answers(cls, answer, answer_schema):
        multiple_answers = []
        for option in answer_schema['options']:
            if option['value'] in answer:
                if option['value'] == 'other':
                    summary_option_display_value = cls._get_checkbox_other_display_value(answer, answer_schema, option)
                    multiple_answers.append(summary_option_display_value)
                else:
                    multiple_answers.append(option['label'])
        return multiple_answers

    @staticmethod
    def _get_checkbox_other_display_value(answer, answer_schema, option):
        options = {option['value'] for option in answer_schema['options']}
        other_option_input = [option for option in set(answer) - set(options) if option.strip()]
        return option['label'] if not other_option_input else other_option_input.pop()

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
            if option['value'] == 'other' and answer != option['value']:
                return answer if answer else option['label']
            elif answer == option['value']:
                return option['label']
