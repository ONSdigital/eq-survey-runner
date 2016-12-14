from unittest import TestCase

import mock

from app.templating.summary.question import Question


class TestQuestion(TestCase):

    def test_create_question(self):
        # Given
        answers = mock.MagicMock()
        answer_schema = mock.MagicMock()
        question_schema = {'id': 'question_id', 'title': 'question_title', 'type': 'GENERAL', 'answers': [answer_schema]}

        # When
        question = Question(question_schema, answers)

        # Then
        self.assertEqual(question.id, 'question_id')
        self.assertEqual(question.title, 'question_title')
        self.assertEqual(len(question.answers), 1)

    def test_create_question_with_no_answers(self):
        # Given
        answers = {}
        answer_schema = mock.MagicMock()
        question_schema = {'id': 'question_id', 'title': 'question_title', 'type': 'GENERAL', 'answers': [answer_schema]}

        # When
        question = Question(question_schema, answers)

        # Then
        self.assertEqual(question.id, 'question_id')
        self.assertEqual(question.title, 'question_title')
        self.assertEqual(len(question.answers), 1)

    def test_create_question_with_multiple_answers(self):
        # Given
        answers = {'answer_1': 'Han',
                   'answer_2': 'Solo'}
        first_answer_schema = {'id': 'answer_1', 'label': 'First name', 'type': 'text'}
        second_answer_schema = {'id': 'answer_2', 'label': 'Surname', 'type': 'text'}
        question_schema = {'id': 'question_id', 'title': 'question_title', 'type': 'GENERAL', 'answers': [first_answer_schema, second_answer_schema]}

        # When
        question = Question(question_schema, answers)

        # Then
        self.assertEqual(len(question.answers), 2)
        self.assertEqual(question.answers[0].value, 'Han')
        self.assertEqual(question.answers[1].value, 'Solo')

    def test_merge_date_range_answers(self):
        # Given
        answers = {'answer_1': '13/02/2016',
                   'answer_2': '13/09/2016'}
        first_date_answer_schema = {'id': 'answer_1', 'label': 'From', 'type': 'date'}
        second_date_answer_schema = {'id': 'answer_2', 'label': 'To', 'type': 'date'}
        question_schema = {'id': 'question_id', 'title': 'question_title', 'type': 'DateRange', 'answers': [first_date_answer_schema, second_date_answer_schema]}

        # When
        question = Question(question_schema, answers)

        # Then
        self.assertEqual(len(question.answers), 1)
        self.assertEqual(question.answers[0].value['from'], '13/02/2016')
        self.assertEqual(question.answers[0].value['to'], '13/09/2016', '%d/%m/%Y')

    def test_merge_multiple_date_range_answers(self):
        # Given
        answers = {'answer_1': '13/02/2016',
                   'answer_2': '13/09/2016',
                   'answer_3': '13/03/2016',
                   'answer_4': '13/10/2016'}
        first_date_answer_schema = {'id': 'answer_1', 'label': 'From', 'type': 'date'}
        second_date_answer_schema = {'id': 'answer_2', 'label': 'To', 'type': 'date'}
        third_date_answer_schema = {'id': 'answer_3', 'label': 'First period', 'type': 'date'}
        fourth_date_answer_schema = {'id': 'answer_4', 'label': 'Second period', 'type': 'date'}
        question_schema = {'id': 'question_id', 'title': 'question_title', 'type': 'DateRange', 'answers':
                           [first_date_answer_schema, second_date_answer_schema, third_date_answer_schema, fourth_date_answer_schema]}

        # When
        question = Question(question_schema, answers)

        # Then
        self.assertEqual(len(question.answers), 2)
        self.assertEqual(question.answers[0].value['from'], '13/02/2016')
        self.assertEqual(question.answers[0].value['to'], '13/09/2016', '%d/%m/%Y')
        self.assertEqual(question.answers[1].value['from'], '13/03/2016', '%d/%m/%Y')
        self.assertEqual(question.answers[1].value['to'], '13/10/2016', '%d/%m/%Y')

    def test_checkbox_button_options(self):
        # Given
        answers = {'answer_1': ['Light Side', 'Dark Side']}
        options = [{
            'label': 'Light Side',
            'value': 'Light Side',
          },
          {
            'label': 'Dark Side',
            'value': 'Dark Side',
          }]
        answer_schema = {'id': 'answer_1', 'label': 'Which side?', 'type': 'Checkbox', 'options': options}
        question_schema = {'id': 'question_id', 'title': 'question_title', 'type': 'GENERAL', 'answers': [answer_schema]}

        # When
        question = Question(question_schema, answers)

        # Then
        self.assertEqual(len(question.answers[0].value), 2)
        self.assertEqual(question.answers[0].value[0], 'Light Side')
        self.assertEqual(question.answers[0].value[1], 'Dark Side')

    def test_checkbox_button_other_option_empty(self):
        # Given
        answers = {'answer_1': ['other', '']}
        options = [{
            'label': 'Light Side',
            'value': 'Light Side',
          },
          {
            'label': 'Other option label',
            'value': 'other',
            "other": {
              "label": "Please specify other"
            }
          }]
        answer_schema = {'id': 'answer_1', 'label': 'Which side?', 'type': 'Checkbox', 'options': options}
        question_schema = {'id': 'question_id', 'title': 'question_title', 'type': 'GENERAL', 'answers': [answer_schema]}

        # When
        question = Question(question_schema, answers)

        # Then
        self.assertEqual(len(question.answers[0].value), 1)
        self.assertEqual(question.answers[0].value[0], 'Other option label')

    def test_checkbox_button_other_option_text(self):
        # Given
        answers = {'answer_1': ['Light Side', 'other', 'Neither']}
        options = [{
            'label': 'Light Side',
            'value': 'Light Side',
          },
          {
            'label': 'Other',
            'value': 'other',
            "other": {
              "label": "Please specify other"
            }
          }]
        answer_schema = {'id': 'answer_1', 'label': 'Which side?', 'type': 'Checkbox', 'options': options}
        question_schema = {'id': 'question_id', 'title': 'question_title', 'type': 'GENERAL', 'answers': [answer_schema]}

        # When
        question = Question(question_schema, answers)

        # Then
        self.assertEqual(len(question.answers[0].value), 2)
        self.assertEqual(question.answers[0].value[0], 'Light Side')
        self.assertEqual(question.answers[0].value[1], 'Neither')

    def test_checkbox_button_none_selected_should_be_none(self):
        # Given
        answers = {'answer_1': []}
        options = [{
            'label': 'Light Side',
            'value': 'Light Side',
          }]
        answer_schema = {'id': 'answer_1', 'label': 'Which side?', 'type': 'Checkbox', 'options': options}
        question_schema = {'id': 'question_id', 'title': 'question_title', 'type': 'GENERAL', 'answers': [answer_schema]}

        # When
        question = Question(question_schema, answers)

        # Then
        self.assertEqual(question.answers[0].value, None)

    def test_radio_button_other_option_empty(self):
        # Given
        answers = {'answer_1': ''}
        options = [{
            'label': 'Light Side',
            'value': 'Light Side',
          },
          {
            'label': 'Other option label',
            'value': 'other',
            "other": {
              "label": "Please specify other"
            }
          }]
        answer_schema = {'id': 'answer_1', 'label': 'Which side?', 'type': 'Radio', 'options': options}
        question_schema = {'id': 'question_id', 'title': 'question_title', 'type': 'GENERAL', 'answers': [answer_schema]}

        # When
        question = Question(question_schema, answers)

        # Then
        self.assertEqual(question.answers[0].value, 'Other option label')

    def test_radio_button_other_option_text(self):
        # Given
        answers = {'answer_1': 'I want to be on the dark side'}
        options = [{
            'label': 'Light Side',
            'value': 'Light Side',
          },
          {
            'label': 'Other option label',
            'value': 'other',
            "other": {
              "label": "Please specify other"
            }
          }]
        answer_schema = {'id': 'answer_1', 'label': 'Which side?', 'type': 'Radio', 'options': options}
        question_schema = {'id': 'question_id', 'title': 'question_title', 'type': 'GENERAL', 'answers': [answer_schema]}

        # When
        question = Question(question_schema, answers)

        # Then
        self.assertEqual(question.answers[0].value, 'I want to be on the dark side')

    def test_radio_button_none_selected_should_be_none(self):
        # Given
        answers = {'answer_1': None}
        options = [{
            'label': 'Light Side',
            'value': 'Light Side',
          }]
        answer_schema = {'id': 'answer_1', 'label': 'Which side?', 'type': 'Radio', 'options': options}
        question_schema = {'id': 'question_id', 'title': 'question_title', 'type': 'GENERAL', 'answers': [answer_schema]}

        # When
        question = Question(question_schema, answers)

        # Then
        self.assertEqual(question.answers[0].value, None)

    def test_question_should_be_skipped(self):
        # Given
        answers = {'answer_1': 'skip me'}
        answer_schema = {'id': 'answer_1', 'title': '', 'type': '', 'label': ''}
        skip_condition = {'when': [{'id': 'answer_1', 'condition': 'equals', 'value': 'skip me'}]}
        question_schema = {'id': 'question_id', 'title': 'question_title', 'type': 'GENERAL', 'answers': [answer_schema],
                           'skip_condition': skip_condition}

        # When
        question = Question(question_schema, answers)

        # Then
        self.assertTrue(question.is_skipped(answers))

    def test_question_with_no_answers_should_not_be_skipped(self):
        # Given
        answers = {}
        answer_schema = {'id': 'answer_1', 'title': '', 'type': '', 'label': ''}
        skip_condition = {'when': [{'id': 'answer_1', 'condition': 'equals', 'value': 'skip me'}]}
        question_schema = {'id': 'question_id', 'title': 'question_title', 'type': 'GENERAL', 'answers': [answer_schema],
                           'skip_condition': skip_condition}

        # When
        question = Question(question_schema, answers)

        # Then
        self.assertFalse(question.is_skipped(answers))

    def test_build_answers_repeating_answers(self):
        # Given
        answers = {
            'answer': 'value',
            'answer_1': 'value1',
            'answer_2': 'value2',
        }
        answer_schema = {'id': 'answer', 'title': '', 'type': '', 'label': ''}
        question_schema = {'id': 'question_id', 'title': 'question_title', 'type': 'RepeatingAnswer',
                           'answers': [answer_schema]}

        # When
        question = Question(question_schema, answers)

        # Then
        self.assertEqual(len(question.answers), 3)
