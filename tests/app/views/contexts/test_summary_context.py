from unittest.mock import Mock, patch, MagicMock

from app.data_model.answer_store import AnswerStore, Answer
from app.data_model.list_store import ListStore
from app.data_model.progress_store import ProgressStore, CompletionStatus
from app.data_model.questionnaire_store import QuestionnaireStore
from app.questionnaire.location import Location
from app.views.handlers.calculated_summary import CalculatedSummary
from app.views.handlers.section_summary import SectionSummary
from app.views.handlers.summary import Summary
from app.utilities.schema import load_schema_from_name
from tests.app.app_context_test_case import AppContextTestCase
from app.questionnaire.questionnaire_schema import DEFAULT_LANGUAGE_CODE


class TestStandardSummaryContext(AppContextTestCase):
    def setUp(self):
        super().setUp()
        self.metadata = {
            'return_by': '2016-10-10',
            'ref_p_start_date': '2016-10-10',
            'ref_p_end_date': '2016-10-10',
            'ru_ref': 'def123',
            'response_id': 'abc123',
            'ru_name': 'Mr Cloggs',
            'trad_as': 'Samsung',
            'tx_id': '12345678-1234-5678-1234-567812345678',
            'period_str': '201610',
            'employment_date': '2016-10-10',
            'collection_exercise_sid': '789',
            'schema_name': '0000_1',
        }
        self.language = 'en'

    def check_context(self, context):
        self.assertEqual(len(context), 1)
        self.assertTrue(
            'summary' in context, 'Key value {} missing from context'.format('summary')
        )

        summary_context = context['summary']
        for key_value in ('groups', 'answers_are_editable', 'summary_type'):
            self.assertTrue(
                key_value in summary_context,
                "Key value {} missing from context['summary']".format(key_value),
            )

    def check_summary_rendering_context(self, summary_rendering_context):
        for group in summary_rendering_context:
            self.assertTrue('id' in group)
            self.assertTrue('blocks' in group)
            for block in group['blocks']:
                self.assertTrue('question' in block)
                self.assertTrue('title' in block['question'])
                self.assertTrue('answers' in block['question'])
                for answer in block['question']['answers']:
                    self.assertTrue('id' in answer)
                    self.assertTrue('value' in answer)
                    self.assertTrue('type' in answer)


class TestSummaryContext(TestStandardSummaryContext):
    def setUp(self):
        super().setUp()
        self.schema = load_schema_from_name('test_summary')
        self.answer_store = AnswerStore()
        self.list_store = ListStore()
        self.block_type = 'Summary'
        self.rendered_block = {
            'parent_id': 'summary-group',
            'id': 'summary',
            'type': 'Summary',
            'collapsible': True,
        }
        self.language = 'en'
        self.current_location = Location(
            section_id='default-section', block_id='summary'
        )

        storage = MagicMock()
        storage.get_user_data = MagicMock(return_value=('{}', 1))
        storage.add_or_update = MagicMock()

        self.questionnaire_store = QuestionnaireStore(storage)
        self.questionnaire_store.answer_store = AnswerStore(
            [
                {'answer_id': 'radio-answer', 'value': 'Eggs', 'list_item_id': None},
                {'answer_id': 'test-currency', 'value': 1, 'list_item_id': None},
                {'answer_id': 'square-kilometres', 'value': 1, 'list_item_id': None},
                {'answer_id': 'test-decimal', 'value': 1, 'list_item_id': None},
                {'answer_id': 'dessert', 'value': 'Cake', 'list_item_id': None},
            ]
        )
        self.questionnaire_store.progress_store = ProgressStore(
            [
                {
                    'section_id': 'default-section',
                    'list_item_id': None,
                    'status': CompletionStatus.COMPLETED,
                    'locations': [
                        {'section_id': 'default-section', 'block_id': 'radio'},
                        {
                            'section_id': 'default-section',
                            'block_id': 'test-number-block',
                        },
                        {'section_id': 'default-section', 'block_id': 'dessert-block'},
                    ],
                }
            ]
        )

    def test_build_summary_rendering_context(self):
        summary = Summary(
            self.schema, self.questionnaire_store, self.language, self.current_location
        )
        context = summary.get_context()

        self.check_summary_rendering_context(context['summary']['groups'])

    def test_build_view_context_for_summary(self):
        summary = Summary(
            self.schema, self.questionnaire_store, self.language, self.current_location
        )
        context = summary.get_context()

        self.check_context(context)
        self.check_summary_rendering_context(context['summary']['groups'])

        self.assertEqual(len(context['summary']), 5)
        self.assertTrue('is_view_submission_response_enabled' in context['summary'])
        self.assertTrue('collapsible' in context['summary'])


class TestSectionSummaryContext(TestStandardSummaryContext):
    def setUp(self):
        super().setUp()
        self.block_type = 'SectionSummary'
        self.language = 'en'
        self.current_location = Location(
            section_id='property-details-section', block_id='property-details-summary'
        )

        storage = MagicMock()
        storage.get_user_data = MagicMock(return_value=('{}', 1))
        storage.add_or_update = MagicMock()

        self.questionnaire_store = QuestionnaireStore(storage)
        self.questionnaire_store.answer_store = AnswerStore()
        self.questionnaire_store.progress_store = ProgressStore(
            [
                {
                    'section_id': 'property-details-section',
                    'list_item_id': None,
                    'status': CompletionStatus.COMPLETED,
                    'locations': [
                        {
                            'section_id': 'property-details-section',
                            'block_id': 'insurance-type',
                        },
                        {
                            'section_id': 'property-details-section',
                            'block_id': 'insurance-address',
                        },
                        {
                            'section_id': 'property-details-section',
                            'block_id': 'address-duration',
                        },
                    ],
                }
            ]
        )
        self.schema = load_schema_from_name('test_section_summary')

    def test_build_summary_rendering_context(self):
        summary = SectionSummary(
            self.schema, self.questionnaire_store, self.language, self.current_location, return_to=None
        )
        context = summary.get_context()
        self.check_summary_rendering_context(context['summary']['groups'])
        self.assertTrue('title' in context['summary'])


class TestCalculatedSummaryContext(TestStandardSummaryContext):
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
            self.schema, self.questionnaire_store, self.language, current_location, return_to=None
        )

        context = summary.get_context()

        self.check_context(context)
        self.check_summary_rendering_context(context['summary']['groups'])
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
            self.schema, self.questionnaire_store, self.language, current_location, return_to=None
        )

        context = summary.get_context()

        self.check_context(context)
        self.check_summary_rendering_context(context['summary']['groups'])
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
            self.schema, self.questionnaire_store, self.language, current_location, return_to=None
        )

        context = summary.get_context()

        self.check_context(context)
        self.check_summary_rendering_context(context['summary']['groups'])
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
            self.schema, self.questionnaire_store, self.language, current_location, return_to=None
        )

        context = summary.get_context()

        self.check_context(context)
        self.check_summary_rendering_context(context['summary']['groups'])
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
            self.schema, self.questionnaire_store, self.language, current_location, return_to=None
        )

        context = summary.get_context()

        self.check_context(context)
        self.check_summary_rendering_context(context['summary']['groups'])
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


def test_context_for_section_list_summary(people_answer_store, app):
    schema = load_schema_from_name('test_list_collector_section_summary')
    current_location = Location(
        block_id='people-list-section-summary', section_id='section'
    )

    storage = MagicMock()
    storage.get_user_data = MagicMock(return_value=('{}', 1))
    storage.add_or_update = MagicMock()

    questionnaire_store = QuestionnaireStore(storage)
    questionnaire_store.answer_store = people_answer_store
    questionnaire_store.list_store = ListStore(
        [
            {'items': ['PlwgoG', 'UHPLbX'], 'name': 'people'},
            {'items': ['gTrlio'], 'name': 'visitors'},
        ]
    )

    summary = SectionSummary(
        schema, questionnaire_store, 'en', current_location, return_to=None
    )

    context = summary.get_context()

    expected = [
        {
            'add_link': '/questionnaire/people/add-person/',
            'add_link_text': 'Add someone to this household',
            'empty_list_text': 'There are no householders',
            'list_items': [
                {
                    'edit_link': '/questionnaire/people/PlwgoG/edit-person/',
                    'item_title': 'Toni Morrison',
                    'primary_person': False,
                    'remove_link': '/questionnaire/people/PlwgoG/remove-person/',
                },
                {
                    'edit_link': '/questionnaire/people/UHPLbX/edit-person/',
                    'item_title': 'Barry Pheloung',
                    'primary_person': False,
                    'remove_link': '/questionnaire/people/UHPLbX/remove-person/',
                },
            ],
            'title': 'Household members on 13 October 2019',
            'list_name': 'people',
        },
        {
            'add_link': '/questionnaire/visitors/add-visitor/',
            'add_link_text': 'Add another visitor to this household',
            'empty_list_text': 'There are no visitors',
            'list_items': [
                {
                    'edit_link': '/questionnaire/visitors/gTrlio/edit-visitor-person/',
                    'item_title': '',
                    'primary_person': False,
                    'remove_link': '/questionnaire/visitors/gTrlio/remove-visitor/',
                }
            ],
            'title': 'Visitors staying overnight on 13 October 2019',
            'list_name': 'visitors',
        },
    ]

    assert context['summary']['list_summaries'] == expected
