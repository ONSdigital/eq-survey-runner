from unittest.mock import MagicMock, Mock, patch

from app.data_model.answer import Answer
from app.data_model.answer_store import AnswerStore
from app.data_model.list_store import ListStore
from app.data_model.progress_store import ProgressStore, CompletionStatus
from app.data_model.questionnaire_store import QuestionnaireStore
from app.questionnaire.location import Location
from app.utilities.schema import load_schema_from_name
from app.views.handlers.calculated_summary import CalculatedSummary
from tests.app.views.handlers.test_summary_handler import TestStandardSummaryHandler


class TestCalculatedSummaryHandler(TestStandardSummaryHandler):
    def setUp(self):
        super().setUp()
        self.schema = load_schema_from_name('test_calculated_summary')

        storage = MagicMock()
        storage.get_user_data = MagicMock(return_value=('{}', 1))
        storage.add_or_update = MagicMock()

        self.language = 'en'
        self.questionnaire_store = QuestionnaireStore(storage)
        self.questionnaire_store.answer_store = AnswerStore(
            [
                {'value': 1, 'answer_id': 'first-number-answer'},
                {'value': 2, 'answer_id': 'second-number-answer'},
                {'value': 3, 'answer_id': 'second-number-answer-unit-total'},
                {'value': 4, 'answer_id': 'second-number-answer-also-in-total'},
                {'value': 5, 'answer_id': 'third-number-answer'},
                {'value': 6, 'answer_id': 'third-and-a-half-number-answer-unit-total'},
                {'value': 'No', 'answer_id': 'skip-fourth-block-answer'},
                {'value': 7, 'answer_id': 'fourth-number-answer'},
                {
                    'value': 8,
                    'answer_id': 'fourth-and-a-half-number-answer-also-in-total',
                },
                {'value': 9, 'answer_id': 'fifth-percent-answer'},
                {'value': 10, 'answer_id': 'fifth-number-answer'},
                {'value': 11, 'answer_id': 'sixth-percent-answer'},
                {'value': 12, 'answer_id': 'sixth-number-answer'},
            ]
        )
        self.questionnaire_store.progress_store = ProgressStore(
            [
                {
                    'section_id': 'default-section',
                    'list_item_id': None,
                    'status': CompletionStatus.COMPLETED,
                    'locations': [
                        {
                            'section_id': 'default-section',
                            'block_id': 'first-number-block',
                        },
                        {
                            'section_id': 'default-section',
                            'block_id': 'second-number-block',
                        },
                        {
                            'section_id': 'default-section',
                            'block_id': 'third-number-block',
                        },
                        {
                            'section_id': 'default-section',
                            'block_id': 'third-and-a-half-number-block',
                        },
                        {
                            'section_id': 'default-section',
                            'block_id': 'skip-fourth-block',
                        },
                        {
                            'section_id': 'default-section',
                            'block_id': 'fourth-number-block',
                        },
                        {
                            'section_id': 'default-section',
                            'block_id': 'fourth-and-a-half-number-block',
                        },
                        {
                            'section_id': 'default-section',
                            'block_id': 'fifth-number-block',
                        },
                        {
                            'section_id': 'default-section',
                            'block_id': 'sixth-number-block',
                        },
                        {
                            'section_id': 'default-section',
                            'block_id': 'currency-total-playback-skipped-fourth',
                        },
                        {
                            'section_id': 'default-section',
                            'block_id': 'currency-total-playback-with-fourth',
                        },
                        {
                            'section_id': 'default-section',
                            'block_id': 'unit-total-playback',
                        },
                        {
                            'section_id': 'default-section',
                            'block_id': 'percentage-total-playback',
                        },
                    ],
                }
            ]
        )
        self.list_store = ListStore()
        self.block_type = 'CalculatedSummary'

    @patch('app.jinja_filters.flask_babel.get_locale', Mock(return_value='en_GB'))
    def test_build_view_context_for_currency_calculated_summary_no_skip(self):
        current_location = Location(
            section_id='default-section', block_id='currency-total-playback-with-fourth'
        )

        summary = CalculatedSummary(
            self.schema, self.questionnaire_store, self.language, current_location, None
        )

        context = summary.get_context()

        self.check_context(context)
        self.check_groups(context['summary']['groups'])
        self.assertEqual(len(context['summary']), 5)
        context_summary = context['summary']
        self.assertTrue('title' in context_summary)
        self.assertEqual(
            context_summary['title'],
            'We calculate the total of currency values entered to be £27.00. Is this correct? (With Fourth)',
        )

        self.assertTrue('calculated_question' in context_summary)
        self.assertEqual(len(context_summary['groups'][0]['blocks']), 5)
        self.assertEqual(
            context_summary['calculated_question']['title'],
            'Grand total of previous values',
        )
        self.assertEqual(
            context_summary['calculated_question']['answers'][0]['value'], '£27.00'
        )

    @patch('app.jinja_filters.flask_babel.get_locale', Mock(return_value='en_GB'))
    def test_build_view_context_for_currency_calculated_summary_with_skip(self):
        current_location = Location(
            section_id='default-section',
            block_id='currency-total-playback-skipped-fourth',
        )

        skip_answer = Answer('skip-fourth-block-answer', 'Yes')

        self.questionnaire_store.answer_store.add_or_update(skip_answer)

        summary = CalculatedSummary(
            self.schema, self.questionnaire_store, self.language, current_location, None
        )

        context = summary.get_context()

        self.check_context(context)
        self.check_groups(context['summary']['groups'])
        self.assertEqual(len(context['summary']), 5)
        context_summary = context['summary']
        self.assertTrue('title' in context_summary)
        self.assertEqual(len(context_summary['groups'][0]['blocks']), 3)
        self.assertEqual(
            context_summary['title'],
            'We calculate the total of currency values entered to be £12.00. Is this correct? (Skipped Fourth)',
        )

        self.assertTrue('calculated_question' in context_summary)
        self.assertEqual(
            context_summary['calculated_question']['title'],
            'Grand total of previous values',
        )
        self.assertEqual(
            context_summary['calculated_question']['answers'][0]['value'], '£12.00'
        )

    @patch('app.jinja_filters.flask_babel.get_locale', Mock(return_value='en_GB'))
    def test_build_view_context_for_unit_calculated_summary(self):
        current_location = Location(
            section_id='default-section', block_id='unit-total-playback'
        )

        summary = CalculatedSummary(
            self.schema, self.questionnaire_store, self.language, current_location, None
        )

        context = summary.get_context()

        self.check_context(context)
        self.check_groups(context['summary']['groups'])
        self.assertEqual(len(context['summary']), 5)
        context_summary = context['summary']
        self.assertTrue('title' in context_summary)
        self.assertEqual(
            context_summary['title'],
            'We calculate the total of unit values entered to be 9 cm. Is this correct?',
        )

        self.assertTrue('calculated_question' in context_summary)
        self.assertEqual(
            context_summary['calculated_question']['title'],
            'Grand total of previous values',
        )
        self.assertEqual(
            context_summary['calculated_question']['answers'][0]['value'], '9 cm'
        )

    def test_build_view_context_for_percentage_calculated_summary(self):
        current_location = Location(
            section_id='default-section', block_id='percentage-total-playback'
        )

        summary = CalculatedSummary(
            self.schema, self.questionnaire_store, self.language, current_location, None
        )

        context = summary.get_context()

        self.check_context(context)
        self.check_groups(context['summary']['groups'])
        self.assertEqual(len(context['summary']), 5)
        context_summary = context['summary']
        self.assertTrue('title' in context_summary)
        self.assertEqual(
            context_summary['title'],
            'We calculate the total of percentage values entered to be 20%. Is this correct?',
        )

        self.assertTrue('calculated_question' in context_summary)
        self.assertEqual(
            context_summary['calculated_question']['title'],
            'Grand total of previous values',
        )
        self.assertEqual(
            context_summary['calculated_question']['answers'][0]['value'], '20%'
        )

    @patch('app.jinja_filters.flask_babel.get_locale', Mock(return_value='en_GB'))
    def test_build_view_context_for_number_calculated_summary(self):
        current_location = Location(
            section_id='default-section', block_id='number-total-playback'
        )

        summary = CalculatedSummary(
            self.schema, self.questionnaire_store, self.language, current_location, None
        )

        context = summary.get_context()

        self.check_context(context)
        self.check_groups(context['summary']['groups'])
        self.assertEqual(len(context['summary']), 5)
        context_summary = context['summary']
        self.assertTrue('title' in context_summary)
        self.assertEqual(
            context_summary['title'],
            'We calculate the total of number values entered to be 22. Is this correct?',
        )

        self.assertTrue('calculated_question' in context_summary)
        self.assertEqual(
            context_summary['calculated_question']['title'],
            'Grand total of previous values',
        )
        self.assertEqual(
            context_summary['calculated_question']['answers'][0]['value'], '22'
        )
