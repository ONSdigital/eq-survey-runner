import mock
from mock import patch
from app.templating.summary.question import Question
from app.data_model.answer_store import AnswerStore
from tests.app.app_context_test_case import AppContextTestCase


class TestQuestion(AppContextTestCase):

    def test_create_question(self):
        # Given
        answer_schema = mock.MagicMock()
        answer_store = AnswerStore()
        question_schema = {'id': 'question_id', 'title': 'question_title', 'type': 'GENERAL', 'answers': [answer_schema]}

        # When
        question = Question(question_schema, answer_store, {})

        # Then
        self.assertEqual(question.id, 'question_id')
        self.assertEqual(question.title, 'question_title')
        self.assertEqual(len(question.answers), 1)

    def test_create_question_with_no_answers(self):
        # Given
        answer_schema = mock.MagicMock()
        answer_store = AnswerStore()
        question_schema = {'id': 'question_id', 'title': 'question_title', 'type': 'GENERAL', 'answers': [answer_schema]}

        # When
        question = Question(question_schema, answer_store, {})

        # Then
        self.assertEqual(question.id, 'question_id')
        self.assertEqual(question.title, 'question_title')
        self.assertEqual(len(question.answers), 1)

    def test_create_question_with_default_title(self):
        # Given
        answer_schema = mock.MagicMock()
        answer_store = AnswerStore()
        question_schema = {'id': 'question_id', 'titles': [{'value': 'question_title'}], 'type': 'GENERAL', 'answers': [answer_schema]}

        # When
        question = Question(question_schema, answer_store, {})

        # Then
        self.assertEqual(question.id, 'question_id')
        self.assertEqual(question.title, 'question_title')
        self.assertEqual(len(question.answers), 1)

    def test_create_question_with_conditional_title(self):
        # Given
        answer_store = AnswerStore([{
            'answer_id': 'answer_1',
            'block_id': '',
            'value': 'Han',
            'answer_instance': 0,
            'group_instance': 0
        }])
        answer_schema = mock.MagicMock()
        question_schema = {'id': 'question_id', 'titles': [{'value': 'conditional_title', 'when': [{'id': 'answer_1',
                                                                                                    'condition': 'equals',
                                                                                                    'value': 'Han'}]},
                                                           {'value': 'question_title'}], 'type': 'GENERAL', 'answers': [answer_schema]}

        # When
        with patch('app.questionnaire.rules._answer_is_in_repeating_group', return_value=False):
            question = Question(question_schema, answer_store, {})

        # Then
        self.assertEqual(question.id, 'question_id')
        self.assertEqual(question.title, 'conditional_title')
        self.assertEqual(len(question.answers), 1)

    def test_create_question_with_answer_label_when_empty_title(self):
        # Given
        answer_schema = {'type': 'Number', 'id': 'age-answer', 'mandatory': True, 'label': 'Age'}
        answer_store = AnswerStore()
        question_schema = {'id': 'question_id', 'title': '', 'type': 'GENERAL', 'answers': [answer_schema]}

        # When
        question = Question(question_schema, answer_store, {})

        # Then
        self.assertEqual(question.title, 'Age')
        self.assertEqual(len(question.answers), 1)

    def test_create_question_with_multiple_answers(self):
        # Given
        answer_store = AnswerStore([{
            'answer_id': 'answer_1',
            'block_id': '',
            'value': 'Han',
            'answer_instance': 0,
        }, {
            'answer_id': 'answer_2',
            'block_id': '',
            'value': 'Solo',
            'answer_instance': 0,
        }])
        first_answer_schema = {'id': 'answer_1', 'label': 'First name', 'type': 'text'}
        second_answer_schema = {'id': 'answer_2', 'label': 'Surname', 'type': 'text'}
        question_schema = {'id': 'question_id', 'title': 'question_title', 'type': 'GENERAL',
                           'answers': [first_answer_schema, second_answer_schema]}

        # When
        question = Question(question_schema, answer_store, {})

        # Then
        self.assertEqual(len(question.answers), 2)
        self.assertEqual(question.answers[0]['value'], 'Han')
        self.assertEqual(question.answers[1]['value'], 'Solo')

    def test_merge_date_range_answers(self):
        # Given
        answer_store = AnswerStore([{
            'answer_id': 'answer_1',
            'block_id': '',
            'value': '13/02/2016',
            'answer_instance': 0,
        }, {
            'answer_id': 'answer_2',
            'block_id': '',
            'value': '13/09/2016',
            'answer_instance': 0,
        }])
        first_date_answer_schema = {'id': 'answer_1', 'label': 'From', 'type': 'date'}
        second_date_answer_schema = {'id': 'answer_2', 'label': 'To', 'type': 'date'}
        question_schema = {'id': 'question_id', 'title': 'question_title', 'type': 'DateRange',
                           'answers': [first_date_answer_schema, second_date_answer_schema]}

        # When
        question = Question(question_schema, answer_store, {})

        # Then
        self.assertEqual(len(question.answers), 1)
        self.assertEqual(question.answers[0]['value']['from'], '13/02/2016')
        self.assertEqual(question.answers[0]['value']['to'], '13/09/2016', '%d/%m/%Y')

    def test_merge_multiple_date_range_answers(self):
        # Given
        answer_store = AnswerStore([{
            'answer_id': 'answer_1',
            'block_id': '',
            'value': '13/02/2016',
            'answer_instance': 0,
        }, {
            'answer_id': 'answer_2',
            'block_id': '',
            'value': '13/09/2016',
            'answer_instance': 0,
        }, {
            'answer_id': 'answer_3',
            'block_id': '',
            'value': '13/03/2016',
            'answer_instance': 0,
        }, {
            'answer_id': 'answer_4',
            'block_id': '',
            'value': '13/10/2016',
            'answer_instance': 0,
        }])
        first_date_answer_schema = {'id': 'answer_1', 'label': 'From', 'type': 'date'}
        second_date_answer_schema = {'id': 'answer_2', 'label': 'To', 'type': 'date'}
        third_date_answer_schema = {'id': 'answer_3', 'label': 'First period', 'type': 'date'}
        fourth_date_answer_schema = {'id': 'answer_4', 'label': 'Second period', 'type': 'date'}
        question_schema = {'id': 'question_id', 'title': 'question_title', 'type': 'DateRange', 'answers':
                           [first_date_answer_schema, second_date_answer_schema, third_date_answer_schema, fourth_date_answer_schema]}

        # When
        question = Question(question_schema, answer_store, {})

        # Then
        self.assertEqual(len(question.answers), 2)
        self.assertEqual(question.answers[0]['value']['from'], '13/02/2016')
        self.assertEqual(question.answers[0]['value']['to'], '13/09/2016', '%d/%m/%Y')
        self.assertEqual(question.answers[1]['value']['from'], '13/03/2016', '%d/%m/%Y')
        self.assertEqual(question.answers[1]['value']['to'], '13/10/2016', '%d/%m/%Y')

    def test_checkbox_button_options(self):
        # Given
        answer_store = AnswerStore([{
            'answer_id': 'answer_1',
            'block_id': '',
            'value': ['Light Side', 'Dark Side'],
            'answer_instance': 0,
        }])

        options = [{
            'label': 'Light Side',
            'value': 'Light Side',
        }, {
            'label': 'Dark Side',
            'value': 'Dark Side',
        }]
        answer_schema = {'id': 'answer_1', 'label': 'Which side?', 'type': 'Checkbox', 'options': options}
        question_schema = {'id': 'question_id', 'title': 'question_title', 'type': 'GENERAL', 'answers': [answer_schema]}

        # When
        question = Question(question_schema, answer_store, {})

        # Then
        self.assertEqual(len(question.answers[0]['value']), 2)
        self.assertEqual(question.answers[0]['value'][0].label, 'Light Side')
        self.assertEqual(question.answers[0]['value'][1].label, 'Dark Side')

    def test_checkbox_button_other_option_empty(self):
        # Given
        answer_store = AnswerStore([{
            'answer_id': 'answer_1',
            'block_id': '',
            'value': ['other', ''],
            'answer_instance': 0,
        }])
        options = [{
            'label': 'Light Side',
            'value': 'Light Side',
        }, {
            'label': 'Other option label',
            'value': 'other',
            'other': {
                'label': 'Please specify other'
            }
        }]
        answer_schema = {'id': 'answer_1', 'label': 'Which side?', 'type': 'Checkbox', 'options': options}
        question_schema = {'id': 'question_id', 'title': 'question_title', 'type': 'GENERAL', 'answers': [answer_schema]}

        # When
        question = Question(question_schema, answer_store, {})

        # Then
        self.assertEqual(len(question.answers[0]['value']), 1)
        self.assertEqual(question.answers[0]['value'][0].label, 'Other option label')
        self.assertEqual(question.answers[0]['value'][0].should_display_other, True)

    def test_checkbox_answer_with_other_value_returns_the_value(self):
        # Given
        answer_store = AnswerStore([{
            'answer_id': 'answer_1',
            'block_id': '',
            'value': ['Light Side', 'Other'],
            'answer_instance': 0,
        }, {
            'answer_id': 'child_answer',
            'block_id': '',
            'value': 'Test',
            'answer_instance': 0,
        }])
        options = [{
            'label': 'Light Side',
            'value': 'Light Side',
        }, {
            'label': 'Other',
            'value': 'Other',
            'child_answer_id': 'child_answer'
        }]
        answer_schema = [{
            'id': 'answer_1',
            'label': 'Which side?',
            'type': 'Checkbox',
            'options': options
        }, {
            'parent_answer_id': 'answer_1',
            'id': 'child_answer',
            'type': 'TextField'
        }]
        question_schema = {'id': 'question_id', 'title': 'question_title', 'type': 'GENERAL',
                           'answers': answer_schema}

        # When
        question = Question(question_schema, answer_store, {})

        # Then
        self.assertEqual(len(question.answers[0]['value']), 2)
        self.assertEqual(question.answers[0]['child_answer_value'], 'Test')

    def test_checkbox_button_other_option_text(self):
        # Given
        answer_store = AnswerStore([{
            'answer_id': 'answer_1',
            'block_id': '',
            'value': ['Light Side', 'other'],
            'answer_instance': 0,
        }, {
            'answer_id': 'child_answer',
            'block_id': '',
            'value': 'Neither',
            'answer_instance': 0,
        }])
        options = [{
            'label': 'Light Side',
            'value': 'Light Side',
        }, {
            'label': 'other',
            'value': 'other',
            'child_answer_id': 'child_answer'
        }]
        answer_schema = {'id': 'answer_1', 'label': 'Which side?', 'type': 'Checkbox', 'options': options}
        question_schema = {'id': 'question_id', 'title': 'question_title', 'type': 'GENERAL', 'answers': [answer_schema]}

        # When
        question = Question(question_schema, answer_store, {})

        # Then
        self.assertEqual(len(question.answers[0]['value']), 2)
        self.assertEqual(question.answers[0]['value'][0].label, 'Light Side')
        self.assertEqual(question.answers[0]['child_answer_value'], 'Neither')

    def test_checkbox_button_none_selected_should_be_none(self):
        # Given
        answer_store = AnswerStore([{
            'answer_id': 'answer_1',
            'block_id': '',
            'value': [],
            'answer_instance': 0,
        }])
        options = [{
            'label': 'Light Side',
            'value': 'Light Side',
        }]
        answer_schema = {'id': 'answer_1', 'label': 'Which side?', 'type': 'Checkbox', 'options': options}
        question_schema = {'id': 'question_id', 'title': 'question_title', 'type': 'GENERAL', 'answers': [answer_schema]}

        # When
        question = Question(question_schema, answer_store, {})

        # Then
        self.assertEqual(question.answers[0]['value'], None)

    def test_radio_button_other_option_empty(self):
        # Given
        answer_store = AnswerStore([{
            'answer_id': 'answer_1',
            'block_id': '',
            'value': '',
            'answer_instance': 0,
        }])
        options = [{
            'label': 'Light Side',
            'value': 'Light Side',
        }, {
            'label': 'Other option label',
            'value': 'other',
            'other': {
                'label': 'Please specify other'
            }
        }]
        answer_schema = {'id': 'answer_1', 'label': 'Which side?', 'type': 'Radio', 'options': options}
        question_schema = {'id': 'question_id', 'title': 'question_title', 'type': 'GENERAL', 'answers': [answer_schema]}

        # When
        question = Question(question_schema, answer_store, {})

        # Then
        self.assertEqual(question.answers[0]['value'], 'Other option label')

    def test_radio_button_other_option_text(self):
        # Given
        answer_store = AnswerStore([{
            'answer_id': 'answer_1',
            'block_id': '',
            'value': 'I want to be on the dark side',
            'answer_instance': 0,
        }])
        options = [{
            'label': 'Light Side',
            'value': 'Light Side',
        }, {
            'label': 'Other option label',
            'value': 'other',
            'other': {
                'label': 'Please specify other'
            }
        }]
        answer_schema = {'id': 'answer_1', 'label': 'Which side?', 'type': 'Radio', 'options': options}
        question_schema = {'id': 'question_id', 'title': 'question_title', 'type': 'GENERAL', 'answers': [answer_schema]}

        # When
        question = Question(question_schema, answer_store, {})

        # Then
        self.assertEqual(question.answers[0]['value'], 'I want to be on the dark side')

    def test_radio_button_none_selected_should_be_none(self):
        # Given
        answer_store = AnswerStore([{
            'answer_id': 'answer_1',
            'block_id': '',
            'value': None,
            'answer_instance': 0,
        }])
        options = [{
            'label': 'Light Side',
            'value': 'Light Side',
        }]
        answer_schema = {'id': 'answer_1', 'label': 'Which side?', 'type': 'Radio', 'options': options}
        question_schema = {'id': 'question_id', 'title': 'question_title', 'type': 'GENERAL', 'answers': [answer_schema]}

        # When
        question = Question(question_schema, answer_store, {})

        # Then
        self.assertEqual(question.answers[0]['value'], None)

    def test_radio_answer_with_other_value_returns_the_value(self):
        # Given
        answer_store = AnswerStore([{
            'answer_id': 'answer_1',
            'block_id': '',
            'value': 'Other',
            'answer_instance': 0,
        }, {
            'answer_id': 'child_answer',
            'block_id': '',
            'value': 'Test',
            'answer_instance': 0,
        }])
        options = [{
            'label': 'Other',
            'value': 'Other',
            'child_answer_id': 'child_answer'
        }]
        answer_schema = [{
            'id': 'answer_1',
            'label': 'Which side?',
            'type': 'Radio',
            'options': options
        }, {
            'parent_answer_id': 'answer_1',
            'id': 'child_answer',
            'type': 'TextField'
        }]
        question_schema = {'id': 'question_id', 'title': 'question_title', 'type': 'GENERAL',
                           'answers': answer_schema}

        # When
        question = Question(question_schema, answer_store, {})

        # Then
        self.assertEqual(question.answers[0]['child_answer_value'], 'Test')

    def test_build_answers_repeating_answers(self):
        # Given
        answer_store = AnswerStore([{
            'answer_id': 'answer',
            'block_id': '',
            'value': 'value',
            'answer_instance': 0,
        }, {
            'answer_id': 'answer',
            'block_id': '',
            'value': 'value1',
            'answer_instance': 0,
        }, {
            'answer_id': 'answer',
            'block_id': '',
            'value': 'value2',
            'answer_instance': 0,
        }])
        answer_schema = {'id': 'answer', 'title': '', 'type': '', 'label': ''}
        question_schema = {'id': 'question_id', 'title': 'question_title', 'type': 'RepeatingAnswer',
                           'answers': [answer_schema]}

        # When
        question = Question(question_schema, answer_store, {})

        # Then
        self.assertEqual(len(question.answers), 3)
