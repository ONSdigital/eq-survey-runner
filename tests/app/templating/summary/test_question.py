from mock import MagicMock, patch
from tests.app.app_context_test_case import AppContextTestCase
from app.templating.summary.question import Question
from app.data_model.answer_store import AnswerStore, Answer


class TestQuestion(AppContextTestCase):   # pylint: disable=too-many-public-methods

    def setUp(self):
        super().setUp()
        self.answer_schema = MagicMock()
        self.answer_store = AnswerStore()
        self.schema = MagicMock()
        self.metadata = {}

    def test_create_question(self):
        # Given
        question_title = 'question_title'
        question_schema = {'id': 'question_id', 'title': question_title, 'type': 'GENERAL', 'answers': [self.answer_schema]}

        # When
        with patch('app.templating.summary.question.get_question_title', return_value=question_title):
            question = Question(question_schema, self.answer_store, self.metadata, self.schema)

        # Then
        self.assertEqual(question.id, 'question_id')
        self.assertEqual(question.title, question_title)
        self.assertEqual(len(question.answers), 1)

    def test_create_question_with_no_answers(self):
        # Given
        question_title = 'question_title'
        question_schema = {'id': 'question_id', 'title': question_title, 'type': 'GENERAL', 'answers': []}

        # When
        with patch('app.templating.summary.question.get_question_title', return_value=question_title):
            question = Question(question_schema, self.answer_store, self.metadata, self.schema)

        # Then
        self.assertEqual(question.id, 'question_id')
        self.assertEqual(question.title, question_title)
        self.assertEqual(len(question.answers), 0)

    def test_create_question_with_conditional_title(self):
        # Given
        self.answer_store.add_or_update(Answer(
            answer_id='answer_1',
            value='Han',
        ))

        title_when = [{
            'id': 'answer_1',
            'condition': 'equals',
            'value': 'Han'
            }]
        question_schema = {'id': 'question_id', 'titles': [{'value': 'conditional_title', 'when': title_when},
                                                           {'value': 'question_title'}], 'type': 'GENERAL', 'answers': [self.answer_schema]}

        # When
        with patch('app.templating.utils.evaluate_when_rules', side_effect=[True, False]) as evaluate_when_rules:
            question = Question(question_schema, self.answer_store, self.metadata, self.schema)

        # Then
        evaluate_when_rules.assert_called_once_with(title_when, self.schema, self.metadata, self.answer_store)
        self.assertEqual(question.id, 'question_id')
        self.assertEqual(question.title, 'conditional_title')
        self.assertEqual(len(question.answers), 1)

    def test_create_question_with_answer_label_when_empty_title(self):
        # Given
        answer_schema = {'type': 'Number', 'id': 'age-answer', 'mandatory': True, 'label': 'Age'}
        question_schema = {'id': 'question_id', 'title': '', 'type': 'GENERAL', 'answers': [answer_schema]}

        # When
        with patch('app.templating.summary.question.get_question_title', return_value=False):
            question = Question(question_schema, self.answer_store, self.metadata, self.schema)

        # Then
        self.assertEqual(question.title, 'Age')
        self.assertEqual(len(question.answers), 1)

    def test_create_question_with_multiple_answers(self):
        # Given
        self.answer_store.add_or_update(Answer(
            answer_id='answer_1',
            value='Han',
        ))
        self.answer_store.add_or_update(Answer(
            answer_id='answer_2',
            value='Solo',
        ))
        first_answer_schema = {
            'id': 'answer_1',
            'label': 'First name',
            'type': 'text'
        }
        second_answer_schema = {
            'id': 'answer_2',
            'label': 'Surname',
            'type': 'text'
        }
        question_schema = {'id': 'question_id', 'title': 'question_title', 'type': 'GENERAL',
                           'answers': [first_answer_schema, second_answer_schema]}

        # When
        with patch('app.templating.summary.question.get_question_title', return_value=False):
            question = Question(question_schema, self.answer_store, self.metadata, self.schema)

        # Then
        self.assertEqual(len(question.answers), 2)
        self.assertEqual(question.answers[0]['value'], 'Han')
        self.assertEqual(question.answers[1]['value'], 'Solo')

    def test_merge_date_range_answers(self):
        # Given
        self.answer_store.add_or_update(Answer(
            answer_id='answer_1',
            value='13/02/2016',
        ))
        self.answer_store.add_or_update(Answer(
            answer_id='answer_2',
            value='13/09/2016',
        ))
        first_date_answer_schema = {'id': 'answer_1', 'label': 'From', 'type': 'date'}
        second_date_answer_schema = {'id': 'answer_2', 'label': 'To', 'type': 'date'}
        question_schema = {'id': 'question_id', 'title': 'question_title', 'type': 'DateRange',
                           'answers': [first_date_answer_schema, second_date_answer_schema]}

        # When
        with patch('app.templating.summary.question.get_question_title', return_value=False):
            question = Question(question_schema, self.answer_store, self.metadata, self.schema)

        # Then
        self.assertEqual(len(question.answers), 1)
        self.assertEqual(question.answers[0]['value']['from'], '13/02/2016')
        self.assertEqual(question.answers[0]['value']['to'], '13/09/2016', '%d/%m/%Y')

    def test_merge_multiple_date_range_answers(self):
        # Given
        self.answer_store.add_or_update(Answer(
            answer_id='answer_1',
            value='13/02/2016',
        ))
        self.answer_store.add_or_update(Answer(
            answer_id='answer_2',
            value='13/09/2016',
        ))
        self.answer_store.add_or_update(Answer(
            answer_id='answer_3',
            value='13/03/2016',
        ))
        self.answer_store.add_or_update(Answer(
            answer_id='answer_4',
            value='13/10/2016',
        ))

        first_date_answer_schema = {'id': 'answer_1', 'label': 'From', 'type': 'date'}
        second_date_answer_schema = {'id': 'answer_2', 'label': 'To', 'type': 'date'}
        third_date_answer_schema = {'id': 'answer_3', 'label': 'First period', 'type': 'date'}
        fourth_date_answer_schema = {'id': 'answer_4', 'label': 'Second period', 'type': 'date'}
        question_schema = {'id': 'question_id', 'title': 'question_title', 'type': 'DateRange', 'answers':
                           [first_date_answer_schema, second_date_answer_schema, third_date_answer_schema, fourth_date_answer_schema]}

        # When
        question = Question(question_schema, self.answer_store, self.metadata, self.schema)

        # Then
        self.assertEqual(len(question.answers), 2)
        self.assertEqual(question.answers[0]['value']['from'], '13/02/2016')
        self.assertEqual(question.answers[0]['value']['to'], '13/09/2016', '%d/%m/%Y')
        self.assertEqual(question.answers[1]['value']['from'], '13/03/2016', '%d/%m/%Y')
        self.assertEqual(question.answers[1]['value']['to'], '13/10/2016', '%d/%m/%Y')

    def test_checkbox_button_options(self):
        # Given
        self.answer_store.add_or_update(Answer(
            answer_id='answer_1',
            value=['Light Side', 'Dark Side'],
        ))

        options = [{
            'label': 'Light Side label',
            'value': 'Light Side',
        }, {
            'label': 'Dark Side label',
            'value': 'Dark Side',
        }]
        answer_schema = {'id': 'answer_1', 'label': 'Which side?', 'type': 'Checkbox', 'options': options}
        question_schema = {'id': 'question_id', 'title': 'question_title', 'type': 'GENERAL', 'answers': [answer_schema]}

        # When
        with patch('app.templating.summary.question.get_question_title', return_value=False):
            question = Question(question_schema, self.answer_store, self.metadata, self.schema)

        # Then
        self.assertEqual(len(question.answers[0]['value']), 2)
        self.assertEqual(question.answers[0]['value'][0].label, 'Light Side label')
        self.assertEqual(question.answers[0]['value'][1].label, 'Dark Side label')

    def test_checkbox_button_detail_answer_empty(self):
        # Given
        self.answer_store.add_or_update(Answer(
            answer_id='answer_1',
            value=['other', ''],
        ))

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
        with patch('app.templating.summary.question.get_question_title', return_value=False):
            question = Question(question_schema, self.answer_store, self.metadata, self.schema)

        # Then
        self.assertEqual(len(question.answers[0]['value']), 1)
        self.assertEqual(question.answers[0]['value'][0].label, 'Other option label')
        self.assertEqual(question.answers[0]['value'][0].detail_answer_value, None)

    def test_checkbox_answer_with_detail_answer_returns_the_value(self):
        # Given
        self.answer_store.add_or_update(Answer(
            answer_id='answer_1',
            value=['Light Side', 'Other'],
        ))
        self.answer_store.add_or_update(Answer(
            answer_id='child_answer',
            value='Test',
        ))

        options = [{
            'label': 'Light Side',
            'value': 'Light Side',
        }, {
            'label': 'Other',
            'value': 'Other',
            'detail_answer': {
                'id': 'child_answer',
                'type': 'TextField'
            }
        }]
        answer_schema = [{
            'id': 'answer_1',
            'label': 'Which side?',
            'type': 'Checkbox',
            'options': options
        }]
        question_schema = {'id': 'question_id', 'title': 'question_title', 'type': 'GENERAL',
                           'answers': answer_schema}

        # When
        with patch('app.templating.summary.question.get_question_title', return_value=False):
            question = Question(question_schema, self.answer_store, self.metadata, self.schema)

        # Then
        self.assertEqual(len(question.answers[0]['value']), 2)
        self.assertEqual(question.answers[0]['value'][1].detail_answer_value, 'Test')

    def test_checkbox_button_other_option_text(self):
        # Given
        self.answer_store.add_or_update(Answer(
            answer_id='answer_1',
            value=['Light Side', 'other'],
        ))
        self.answer_store.add_or_update(Answer(
            answer_id='child_answer',
            value='Neither',
        ))
        options = [{
            'label': 'Light Side',
            'value': 'Light Side',
        }, {
            'label': 'other',
            'value': 'other',
            'detail_answer': {'id': 'child_answer'}
        }]
        answer_schema = {'id': 'answer_1', 'label': 'Which side?', 'type': 'Checkbox', 'options': options}
        question_schema = {'id': 'question_id', 'title': 'question_title', 'type': 'GENERAL', 'answers': [answer_schema]}

        # When
        with patch('app.templating.summary.question.get_question_title', return_value=False):
            question = Question(question_schema, self.answer_store, self.metadata, self.schema)

        # Then
        self.assertEqual(len(question.answers[0]['value']), 2)
        self.assertEqual(question.answers[0]['value'][0].label, 'Light Side')
        self.assertEqual(question.answers[0]['value'][1].detail_answer_value, 'Neither')

    def test_checkbox_button_none_selected_should_be_none(self):
        # Given
        self.answer_store.add_or_update(Answer(
            answer_id='answer_1',
            value=[],
        ))
        options = [{
            'label': 'Light Side',
            'value': 'Light Side',
        }]
        answer_schema = {'id': 'answer_1', 'label': 'Which side?', 'type': 'Checkbox', 'options': options}
        question_schema = {'id': 'question_id', 'title': 'question_title', 'type': 'GENERAL', 'answers': [answer_schema]}

        # When
        with patch('app.templating.summary.question.get_question_title', return_value=False):
            question = Question(question_schema, self.answer_store, self.metadata, self.schema)

        # Then
        self.assertEqual(question.answers[0]['value'], None)

    def test_radio_button_none_selected_should_be_none(self):
        # Given
        options = [{
            'label': 'Light Side',
            'value': 'Light Side',
        }]
        answer_schema = {'id': 'answer_1', 'label': 'Which side?', 'type': 'Radio', 'options': options}
        question_schema = {'id': 'question_id', 'title': 'question_title', 'type': 'GENERAL', 'answers': [answer_schema]}

        # When
        with patch('app.templating.summary.question.get_question_title', return_value=False):
            question = Question(question_schema, self.answer_store, self.metadata, self.schema)

        # Then
        self.assertEqual(question.answers[0]['value'], None)

    def test_radio_answer_with_detail_answer_returns_the_value(self):
        # Given
        self.answer_store.add_or_update(Answer(
            answer_id='answer_1',
            value='Other',
        ))
        self.answer_store.add_or_update(Answer(
            answer_id='child_answer',
            value='Test',
        ))
        options = [{
            'label': 'Other',
            'value': 'Other',
            'detail_answer': {
                'id': 'child_answer',
                'type': 'TextField'
            }
        }]
        answer_schema = [{
            'id': 'answer_1',
            'label': 'Which side?',
            'type': 'Radio',
            'options': options
        }]
        question_schema = {'id': 'question_id', 'title': 'question_title', 'type': 'GENERAL',
                           'answers': answer_schema}

        # When
        with patch('app.templating.summary.question.get_question_title', return_value=False):
            question = Question(question_schema, self.answer_store, self.metadata, self.schema)

        # Then
        self.assertEqual(question.answers[0]['value']['detail_answer_value'], 'Test')

    def test_dropdown_none_selected_should_be_none(self):
        # Given
        options = [{
            'label': 'Light Side',
            'value': 'Light Side',
        }]
        answer_schema = {'id': 'answer_1', 'label': 'Which side?', 'type': 'Dropdown', 'options': options}
        question_schema = {'id': 'question_id', 'title': 'question_title', 'type': 'GENERAL', 'answers': [answer_schema]}

        # When
        with patch('app.templating.summary.question.get_question_title', return_value=False):
            question = Question(question_schema, self.answer_store, self.metadata, self.schema)

        # Then
        self.assertEqual(question.answers[0]['value'], None)

    def test_dropdown_selected_option_label(self):
        # Given
        options = [{
            'label': 'Light Side label',
            'value': 'Light Side',
        }, {
            'label': 'Dark Side label',
            'value': 'Dark Side',
        }]
        answer_schema = {'id': 'answer_1', 'label': 'Which side?', 'type': 'Dropdown', 'options': options}
        question_schema = {'id': 'question_id', 'title': 'question_title', 'type': 'GENERAL', 'answers': [answer_schema]}

        self.answer_store.add_or_update(Answer(
            answer_id='answer_1',
            value='Dark Side',
        ))

        # When
        with patch('app.templating.summary.question.get_question_title', return_value=False):
            question = Question(question_schema, self.answer_store, self.metadata, self.schema)

        # Then
        self.assertEqual(question.answers[0]['value'], 'Dark Side label')
