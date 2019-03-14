from unittest.mock import Mock, patch

from app.data_model.answer_store import AnswerStore, Answer
from app.questionnaire.location import Location
from app.templating.summary_context import build_summary_rendering_context
from app.templating.view_context import build_view_context_for_final_summary, \
    build_view_context_for_section_summary, build_view_context_for_calculated_summary
from app.utilities.schema import load_schema_from_params
from tests.app.app_context_test_case import AppContextTestCase


class TestStandardSummaryContext(AppContextTestCase):
    def setUp(self):
        super().setUp()
        self.metadata = {
            'return_by': '2016-10-10',
            'ref_p_start_date': '2016-10-10',
            'ref_p_end_date': '2016-10-10',
            'ru_ref': 'def123',
            'ru_name': 'Mr Cloggs',
            'trad_as': 'Samsung',
            'tx_id': '12345678-1234-5678-1234-567812345678',
            'period_str': '201610',
            'employment_date': '2016-10-10',
            'collection_exercise_sid': '789',
            'form_type': '0000',
            'eq_id': '1',
        }

    def check_context(self, context):
        self.assertEqual(len(context), 1)
        self.assertTrue('summary' in context,
                        'Key value {} missing from context'.format('summary'))

        summary_context = context['summary']
        for key_value in ('groups', 'answers_are_editable', 'summary_type'):
            self.assertTrue(key_value in summary_context,
                            "Key value {} missing from context['summary']".format(key_value))

    def check_summary_rendering_context(self, summary_rendering_context):
        for group in summary_rendering_context:
            self.assertTrue('id' in group)
            self.assertTrue('blocks' in group)
            for block in group['blocks']:
                self.assertTrue('questions' in block)
                for question in block['questions']:
                    self.assertTrue('title' in question)
                    self.assertTrue('answers' in question)
                    for answer in question['answers']:
                        self.assertTrue('id' in answer)
                        self.assertTrue('value' in answer)
                        self.assertTrue('type' in answer)


class TestSummaryContext(TestStandardSummaryContext):

    def setUp(self):
        super().setUp()
        self.schema = load_schema_from_params('test', 'summary')
        self.answer_store = AnswerStore()
        self.schema_context = {
            'answers': {},
            'metadata': self.metadata
        }
        self.block_type = 'Summary'
        self.rendered_block = {
            'parent_id': 'summary-group',
            'id': 'summary',
            'type': 'Summary',
            'collapsible': True
        }

    def test_build_summary_rendering_context(self):
        sections = self.schema.sections
        summary_rendering_context = build_summary_rendering_context(self.schema, sections, self.answer_store,
                                                                    self.metadata, self.schema_context)
        self.check_summary_rendering_context(summary_rendering_context)

    def test_build_view_context_for_summary(self):
        context = build_view_context_for_final_summary(self.metadata, self.schema, self.answer_store,
                                                       self.schema_context, self.block_type,
                                                       self.rendered_block)

        self.check_context(context)
        self.check_summary_rendering_context(context['summary']['groups'])
        self.assertEqual(len(context['summary']), 5)
        self.assertTrue('is_view_submission_response_enabled' in context['summary'])
        self.assertTrue('collapsible' in context['summary'])


class TestSectionSummaryContext(TestStandardSummaryContext):

    def setUp(self):
        super().setUp()
        self.schema = load_schema_from_params('test', 'section_summary')
        self.answer_store = AnswerStore()
        self.schema_context = {
            'answers': {},
            'group_instance': 0,
            'metadata': self.metadata
        }
        self.block_type = 'SectionSummary'

    def test_build_summary_rendering_context(self):
        sections = [self.schema.get_section('property-details-section')]
        summary_rendering_context = build_summary_rendering_context(self.schema, sections, self.answer_store,
                                                                    self.metadata, self.schema_context)
        self.check_summary_rendering_context(summary_rendering_context)

    def test_build_view_context_for_section_summary(self):
        current_location = Location(block_id='property-details-summary')

        context = build_view_context_for_section_summary(self.metadata, self.schema, self.answer_store,
                                                         self.schema_context, self.block_type,
                                                         current_location)

        self.check_context(context)
        self.check_summary_rendering_context(context['summary']['groups'])
        self.assertEqual(len(context['summary']), 4)
        self.assertTrue('title' in context['summary'])


class TestCalculatedSummaryContext(TestStandardSummaryContext):

    def setUp(self):
        super().setUp()
        self.schema = load_schema_from_params('test', 'calculated_summary')
        answers = [
            {'value': 1, 'answer_id': 'first-number-answer'},
            {'value': 2, 'answer_id': 'second-number-answer'},
            {'value': 3, 'answer_id': 'second-number-answer-unit-total'},
            {'value': 4, 'answer_id': 'second-number-answer-also-in-total'},
            {'value': 5, 'answer_id': 'third-number-answer'},
            {'value': 6, 'answer_id': 'third-number-answer-unit-total'},
            {'value': 'No', 'answer_id': 'skip-fourth-block-answer'},
            {'value': 7, 'answer_id': 'fourth-number-answer'},
            {'value': 8, 'answer_id': 'fourth-number-answer-also-in-total'},
            {'value': 9, 'answer_id': 'fifth-percent-answer'},
            {'value': 10, 'answer_id': 'fifth-number-answer'},
            {'value': 11, 'answer_id': 'sixth-percent-answer'},
            {'value': 12, 'answer_id': 'sixth-number-answer'},
        ]
        self.answer_store = AnswerStore(answers)
        self.schema_context = {
            'answers': answers,
            'group_instance': 0,
            'metadata': self.metadata
        }
        self.block_type = 'CalculatedSummary'

    @patch('app.jinja_filters.flask_babel.get_locale', Mock(return_value='en_GB'))
    def test_build_view_context_for_currency_calculated_summary_no_skip(self):
        current_location = Location(block_id='currency-total-playback')

        context = build_view_context_for_calculated_summary(self.metadata, self.schema, self.answer_store,
                                                            self.schema_context, self.block_type,
                                                            current_location)

        self.check_context(context)
        self.check_summary_rendering_context(context['summary']['groups'])
        self.assertEqual(len(context['summary']), 5)
        context_summary = context['summary']
        self.assertTrue('title' in context_summary)
        self.assertEqual(context_summary['title'],
                         'We calculate the total of currency values entered to be £27.00. Is this correct? (With Fourth)')

        self.assertTrue('calculated_question' in context_summary)
        self.assertEqual(len(context_summary['groups'][0]['blocks']), 4)
        self.assertEqual(context_summary['calculated_question']['title'], 'Grand total of previous values')
        self.assertEqual(context_summary['calculated_question']['answers'][0]['value'], '£27.00')

    @patch('app.jinja_filters.flask_babel.get_locale', Mock(return_value='en_GB'))
    def test_build_view_context_for_currency_calculated_summary_with_skip(self):
        current_location = Location(block_id='currency-total-playback')

        skip_answer = Answer('skip-fourth-block-answer', 'Yes')
        self.answer_store.add_or_update(skip_answer)
        context = build_view_context_for_calculated_summary(self.metadata, self.schema, self.answer_store,
                                                            self.schema_context, self.block_type,
                                                            current_location)

        self.check_context(context)
        self.check_summary_rendering_context(context['summary']['groups'])
        self.assertEqual(len(context['summary']), 5)
        context_summary = context['summary']
        self.assertTrue('title' in context_summary)
        self.assertEqual(len(context_summary['groups'][0]['blocks']), 3)
        self.assertEqual(context_summary['title'],
                         'We calculate the total of currency values entered to be £12.00. Is this correct? (Skipped Fourth)')

        self.assertTrue('calculated_question' in context_summary)
        self.assertEqual(context_summary['calculated_question']['title'], 'Grand total of previous values')
        self.assertEqual(context_summary['calculated_question']['answers'][0]['value'], '£12.00')

    @patch('app.jinja_filters.flask_babel.get_locale', Mock(return_value='en_GB'))
    def test_build_view_context_for_unit_calculated_summary(self):
        current_location = Location(block_id='unit-total-playback')

        context = build_view_context_for_calculated_summary(self.metadata, self.schema, self.answer_store,
                                                            self.schema_context, self.block_type,
                                                            current_location)

        self.check_context(context)
        self.check_summary_rendering_context(context['summary']['groups'])
        self.assertEqual(len(context['summary']), 5)
        context_summary = context['summary']
        self.assertTrue('title' in context_summary)
        self.assertEqual(context_summary['title'],
                         'We calculate the total of unit values entered to be 9 cm. Is this correct?')

        self.assertTrue('calculated_question' in context_summary)
        self.assertEqual(context_summary['calculated_question']['title'], 'Grand total of previous values')
        self.assertEqual(context_summary['calculated_question']['answers'][0]['value'], '9 cm')

    def test_build_view_context_for_percentage_calculated_summary(self):
        current_location = Location(block_id='percentage-total-playback')

        context = build_view_context_for_calculated_summary(self.metadata, self.schema, self.answer_store,
                                                            self.schema_context, self.block_type,
                                                            current_location)

        self.check_context(context)
        self.check_summary_rendering_context(context['summary']['groups'])
        self.assertEqual(len(context['summary']), 5)
        context_summary = context['summary']
        self.assertTrue('title' in context_summary)
        self.assertEqual(context_summary['title'],
                         'We calculate the total of percentage values entered to be 20%. Is this correct?')

        self.assertTrue('calculated_question' in context_summary)
        self.assertEqual(context_summary['calculated_question']['title'], 'Grand total of previous values')
        self.assertEqual(context_summary['calculated_question']['answers'][0]['value'], '20%')

    @patch('app.jinja_filters.flask_babel.get_locale', Mock(return_value='en_GB'))
    def test_build_view_context_for_number_calculated_summary(self):
        current_location = Location(block_id='number-total-playback')

        context = build_view_context_for_calculated_summary(self.metadata, self.schema, self.answer_store,
                                                            self.schema_context, self.block_type,
                                                            current_location)

        self.check_context(context)
        self.check_summary_rendering_context(context['summary']['groups'])
        self.assertEqual(len(context['summary']), 5)
        context_summary = context['summary']
        self.assertTrue('title' in context_summary)
        self.assertEqual(context_summary['title'],
                         'We calculate the total of number values entered to be 22. Is this correct?')

        self.assertTrue('calculated_question' in context_summary)
        self.assertEqual(context_summary['calculated_question']['title'], 'Grand total of previous values')
        self.assertEqual(context_summary['calculated_question']['answers'][0]['value'], '22')
