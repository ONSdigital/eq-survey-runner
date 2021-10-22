from mock import MagicMock, patch
from tests.app.app_context_test_case import AppContextTestCase
from app.templating.summary.question import Question
from app.data_model.answer_store import AnswerStore, Answer
from app.utilities.schema import load_schema_from_params


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
            question = Question(question_schema, self.answer_store, self.metadata, self.schema, 0)

        # Then
        self.assertEqual(question.id, 'question_id-0')
        self.assertEqual(question.title, question_title)
        self.assertEqual(len(question.answers), 1)

    def test_create_question_with_no_answers(self):
        # Given
        question_title = 'question_title'
        question_schema = {'id': 'question_id', 'title': question_title, 'type': 'GENERAL', 'answers': []}

        # When
        with patch('app.templating.summary.question.get_question_title', return_value=question_title):
            question = Question(question_schema, self.answer_store, self.metadata, self.schema, 0)

        # Then
        self.assertEqual(question.id, 'question_id-0')
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
            question = Question(question_schema, self.answer_store, self.metadata, self.schema, 0)

        # Then
        evaluate_when_rules.assert_called_once_with(title_when, self.schema, self.metadata, self.answer_store, 0, group_instance_id=None)
        self.assertEqual(question.id, 'question_id-0')
        self.assertEqual(question.title, 'conditional_title')
        self.assertEqual(len(question.answers), 1)

    def test_create_question_with_answer_label_when_empty_title(self):
        # Given
        answer_schema = {'type': 'Number', 'id': 'age-answer', 'mandatory': True, 'label': 'Age'}
        question_schema = {'id': 'question_id', 'title': '', 'type': 'GENERAL', 'answers': [answer_schema]}

        # When
        with patch('app.templating.summary.question.get_question_title', return_value=False):
            question = Question(question_schema, self.answer_store, self.metadata, self.schema, 0)

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
            question = Question(question_schema, self.answer_store, self.metadata, self.schema, 0)

        # Then
        self.assertEqual(len(question.answers), 2)
        self.assertEqual(question.answers[0]['value'], 'Han')
        self.assertEqual(question.answers[1]['value'], 'Solo')

    def test_create_question_with_relationship_answers(self):
        with self.app_request_context():
            schema = load_schema_from_params('test', 'routing_on_answer_from_driving_repeating_group')

        answers = [
            {'group_instance': 0, 'group_instance_id': 'aaa', 'answer_id': 'primary-name', 'answer_instance': 0, 'value': 'Aaa'},
            {'group_instance': 0, 'group_instance_id': 'bbb', 'answer_id': 'repeating-name', 'answer_instance': 0, 'value': 'Bbb'},
            {'group_instance': 1, 'group_instance_id': 'ccc', 'answer_id': 'repeating-name', 'answer_instance': 0, 'value': 'Ccc'},
            {'group_instance': 0, 'group_instance_id': 'aaa', 'answer_id': 'who-is-related', 'answer_instance': 0, 'value': 'Husband or wife'},
            {'group_instance': 0, 'group_instance_id': 'aaa', 'answer_id': 'who-is-related', 'answer_instance': 1, 'value': 'Mother or father'},
            {'group_instance': 1, 'group_instance_id': 'bbb', 'answer_id': 'who-is-related', 'answer_instance': 0, 'value': 'Relation - other'},
        ]

        answer_store = AnswerStore(answers)

        question_schema = {
            'answers': [{
                'label': '%(current_person)s is the .... of %(other_person)s',
                'id': 'who-is-related',
                'options': [
                    {'label': 'Husband or wife', 'value': 'Husband or wife'},
                    {'label': 'Mother or father', 'value': 'Mother or father'},
                    {'label': 'Relation - other', 'value': 'Relation - other'},

                ],
                'type': 'Relationship',
                'parent_id': 'relationship-question'
            }],
            'id': 'relationship-question',
            'title': 'Describe how this person is related to the others',
            'description': 'If members are not related, select the ‘unrelated’ option, including foster parents and foster children.',
            'member_label': "answers['primary-name'] | default(answers['repeating-name'])",
            'type': 'Relationship',
            'parent_id': 'relationships'
        }

        question = Question(question_schema, answer_store, self.metadata, schema, 0)
        self.assertEqual(len(question.answers), 2)
        self.assertEqual(question.answers[0]['value'], 'Husband or wife')
        self.assertEqual(question.answers[1]['value'], 'Mother or father')

        question = Question(question_schema, answer_store, self.metadata, schema, 1)
        self.assertEqual(len(question.answers), 1)
        self.assertEqual(question.answers[0]['value'], 'Relation - other')


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
            question = Question(question_schema, self.answer_store, self.metadata, self.schema, 0)

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
        question = Question(question_schema, self.answer_store, self.metadata, self.schema, 0)

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
            question = Question(question_schema, self.answer_store, self.metadata, self.schema, 0)

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
                'label': 'Please describe other'
            }
        }]
        answer_schema = {'id': 'answer_1', 'label': 'Which side?', 'type': 'Checkbox', 'options': options}
        question_schema = {'id': 'question_id', 'title': 'question_title', 'type': 'GENERAL', 'answers': [answer_schema]}

        # When
        with patch('app.templating.summary.question.get_question_title', return_value=False):
            question = Question(question_schema, self.answer_store, self.metadata, self.schema, 0)

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
            question = Question(question_schema, self.answer_store, self.metadata, self.schema, 0)

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
            question = Question(question_schema, self.answer_store, self.metadata, self.schema, 0)

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
            question = Question(question_schema, self.answer_store, self.metadata, self.schema, 0)

        # Then
        self.assertEqual(question.answers[0]['value'], None)

    def test_radio_button_none_selected_should_be_none(self):
        # Given
        options = [{
            'label': 'Light Side',
            'value': 'Light Side',
        }]
        answer_schema = {'id': 'answer_1', 'label': 'Which side?', 'type': 'Radio', 'options': options, 'group_instance': 0}
        question_schema = {'id': 'question_id', 'title': 'question_title', 'type': 'GENERAL', 'answers': [answer_schema]}

        # When
        with patch('app.templating.summary.question.get_question_title', return_value=False):
            question = Question(question_schema, self.answer_store, self.metadata, self.schema, 0)

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
            question = Question(question_schema, self.answer_store, self.metadata, self.schema, 0)

        # Then
        self.assertEqual(question.answers[0]['value']['detail_answer_value'], 'Test')

    def test_build_answers_repeating_answers(self):
        # Given
        self.answer_store.add_or_update(Answer(
            answer_id='answer',
            value='Value',
        ))
        self.answer_store.add_or_update(Answer(
            answer_id='answer',
            value='Value 2',
            group_instance=1,
            group_instance_id='group-1',
        ))
        self.answer_store.add_or_update(Answer(
            answer_id='answer',
            value='Value 3',
            group_instance=2,
            group_instance_id='group-2',
        ))
        answer_schema = {'id': 'answer', 'title': '', 'type': '', 'label': ''}
        question_schema = {'id': 'question_id', 'title': 'question_title', 'type': 'RepeatingAnswer',
                           'answers': [answer_schema]}

        # When
        with patch('app.templating.summary.question.get_question_title', return_value=False):
            question = Question(question_schema, self.answer_store, self.metadata, self.schema, 0)
            # Then
            self.assertEqual(len(question.answers), 1)
            self.assertEqual(question.answers[0]['value'], 'Value')

            question = Question(question_schema, self.answer_store, self.metadata, self.schema, 1)
            # Then
            self.assertEqual(len(question.answers), 1)
            self.assertEqual(question.answers[0]['value'], 'Value 2')

            question = Question(question_schema, self.answer_store, self.metadata, self.schema, 2)
            # Then
            self.assertEqual(len(question.answers), 1)
            self.assertEqual(question.answers[0]['value'], 'Value 3')

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
            question = Question(question_schema, self.answer_store, self.metadata, self.schema, 0)

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
            question = Question(question_schema, self.answer_store, self.metadata, self.schema, 0)

        # Then
        self.assertEqual(question.answers[0]['value'], 'Dark Side label')
