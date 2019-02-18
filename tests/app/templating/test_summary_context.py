import uuid
from unittest.mock import Mock, patch

from app.data_model.answer_store import AnswerStore, Answer
from app.questionnaire.location import Location
from app.templating.summary_context import build_summary_rendering_context
from app.templating.view_context import build_view_context_for_final_summary, \
    build_view_context_for_section_summary, build_view_context_for_calculated_summary, \
    build_view_context
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
            'group_instance': 0,
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
        current_location = Location(
            block_id='property-details-summary',
            group_id='property-details',
            group_instance=0,
        )

        context = build_view_context_for_section_summary(self.metadata, self.schema, self.answer_store,
                                                         self.schema_context, self.block_type,
                                                         current_location.group_id)

        self.check_context(context)
        self.check_summary_rendering_context(context['summary']['groups'])
        self.assertEqual(len(context['summary']), 4)
        self.assertTrue('title' in context['summary'])


class TestCalculatedSummaryContext(TestStandardSummaryContext):

    def setUp(self):
        super().setUp()
        self.schema = load_schema_from_params('test', 'calculated_summary')
        answers = [
            {'value': 1, 'answer_id': 'first-number-answer', 'group_instance': 0, 'group_instance_id': None, 'answer_instance': 0},
            {'value': 2, 'answer_id': 'second-number-answer', 'group_instance': 0, 'group_instance_id': None, 'answer_instance': 0},
            {'value': 3, 'answer_id': 'second-number-answer-unit-total', 'group_instance': 0, 'group_instance_id': None, 'answer_instance': 0},
            {'value': 4, 'answer_id': 'second-number-answer-also-in-total', 'group_instance': 0, 'group_instance_id': None, 'answer_instance': 0},
            {'value': 5, 'answer_id': 'third-number-answer', 'group_instance': 0, 'group_instance_id': None, 'answer_instance': 0},
            {'value': 6, 'answer_id': 'third-number-answer-unit-total', 'group_instance': 0, 'group_instance_id': None, 'answer_instance': 0},
            {'value': 'No', 'answer_id': 'skip-fourth-block-answer', 'group_instance': 0, 'group_instance_id': None, 'answer_instance': 0},
            {'value': 7, 'answer_id': 'fourth-number-answer', 'group_instance': 0, 'group_instance_id': None, 'answer_instance': 0},
            {'value': 8, 'answer_id': 'fourth-number-answer-also-in-total', 'group_instance': 0, 'group_instance_id': None, 'answer_instance': 0},
            {'value': 9, 'answer_id': 'fifth-percent-answer', 'group_instance': 0, 'group_instance_id': None, 'answer_instance': 0},
            {'value': 10, 'answer_id': 'fifth-number-answer', 'group_instance': 0, 'group_instance_id': None, 'answer_instance': 0},
            {'value': 11, 'answer_id': 'sixth-percent-answer', 'group_instance': 0, 'group_instance_id': None, 'answer_instance': 0},
            {'value': 12, 'answer_id': 'sixth-number-answer', 'group_instance': 0, 'group_instance_id': None, 'answer_instance': 0},
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
        current_location = Location(
            block_id='currency-total-playback',
            group_id='group',
            group_instance=0,
        )

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
        current_location = Location(
            block_id='currency-total-playback',
            group_id='group',
            group_instance=0,
        )

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
        current_location = Location(
            block_id='unit-total-playback',
            group_id='group',
            group_instance=0,
        )

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
        current_location = Location(
            block_id='percentage-total-playback',
            group_id='group',
            group_instance=0,
        )

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
        current_location = Location(
            block_id='number-total-playback',
            group_id='group',
            group_instance=0,
        )

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


class TestRepeatingSummaryContext(TestStandardSummaryContext):

    def setUp(self):
        super().setUp()
        self.schema = load_schema_from_params('test', 'repeat_until_summaries')

        answers = [
            {'group_instance': 0, 'answer_instance': 0, 'answer_id': 'primary-name',
             'group_instance_id': 'aaa-group-instance-id', 'value': 'Aaa'},
            {'group_instance': 0, 'answer_instance': 0, 'answer_id': 'repeating-anyone-else',
             'group_instance_id': None, 'value': 'Yes'},
            {'group_instance': 0, 'answer_instance': 0, 'answer_id': 'repeating-name',
             'group_instance_id': 'bbb-group-instance-id', 'value': 'Bbb'},
            {'group_instance': 1, 'answer_instance': 0, 'answer_id': 'repeating-anyone-else',
             'group_instance_id': None, 'value': 'Yes'},
            {'group_instance': 1, 'answer_instance': 0, 'answer_id': 'repeating-name',
             'group_instance_id': 'ccc-group-instance-id', 'value': 'Ccc'},
            {'group_instance': 2, 'answer_instance': 0, 'answer_id': 'repeating-anyone-else',
             'group_instance_id': None, 'value': 'No'},
            {'group_instance': 0, 'answer_instance': 0, 'answer_id': 'first-number-answer',
             'group_instance_id': 'aaa-group-instance-id', 'value': 1},
            {'group_instance': 0, 'answer_instance': 0, 'answer_id': 'second-number-answer',
             'group_instance_id': 'aaa-group-instance-id', 'value': 11},
            {'group_instance': 1, 'answer_instance': 0, 'answer_id': 'first-number-answer',
             'group_instance_id': 'bbb-group-instance-id', 'value': 2},
            {'group_instance': 1, 'answer_instance': 0, 'answer_id': 'second-number-answer',
             'group_instance_id': 'bbb-group-instance-id', 'value': 22},
            {'group_instance': 2, 'answer_instance': 0, 'answer_id': 'first-number-answer',
             'group_instance_id': 'ccc-group-instance-id', 'value': 3},
            {'group_instance': 2, 'answer_instance': 0, 'answer_id': 'second-number-answer',
             'group_instance_id': 'ccc-group-instance-id', 'value': 33}
        ]
        self.answer_store = AnswerStore(answers)

        self.schema_context = {
            'answers': {
                'repeating-name': ['Bbb', 'Ccc'],
                'repeating-anyone-else': ['Yes', 'Yes', 'No'],
                'first-number-answer': [1, 2, 3],
                'second-number-answer': [11, 22, 33],
                'primary-name': 'Aaa'
            },
            'group_instance': 0,
            'group_instance_id': None,
            'group_instances': {
                'aaa-group-instance-id': {'first-number-answer': 1, 'second-number-answer': 11, 'primary-name': 'Aaa'},
                'bbb-group-instance-id': {'repeating-name': 'Bbb', 'first-number-answer': 2, 'second-number-answer': 22},
                'ccc-group-instance-id': {'repeating-name': 'Ccc', 'first-number-answer': 3, 'second-number-answer': 33},
                None: {'repeating-anyone-else': 'No'},
            },
            'metadata': self.metadata
        }

    def test_build_view_context_for_section_summary_for_repeating_group(self):
        block_type = 'SectionSummary'
        group_id = 'household-summary-group'

        context = build_view_context_for_section_summary(self.metadata, self.schema, self.answer_store, self.schema_context,
                                                         block_type, group_id)

        self.check_context(context)

        context_summary = context['summary']

        self.assertEqual(len(context_summary['groups']), 4)
        self.assertTrue('title' in context_summary)

        self.assertEqual(context_summary['groups'][0]['title'], 'Your Details')
        self.assertEqual(context_summary['groups'][1]['title'], 'Other Household Members')
        self.assertIsNone(context_summary['groups'][2]['title'])
        self.assertIsNone(context_summary['groups'][3]['title'])

        self.assertEqual(context_summary['groups'][0]['blocks'][0]['questions'][0]['answers'][0]['value'], 'Aaa')
        self.assertEqual(context_summary['groups'][1]['blocks'][0]['questions'][0]['answers'][0]['value'], 'Bbb')
        self.assertEqual(context_summary['groups'][2]['blocks'][0]['questions'][0]['answers'][0]['value'], 'Ccc')
        self.assertEqual(context_summary['groups'][3]['blocks'], [])

    @patch('app.jinja_filters.flask_babel.get_locale', Mock(return_value='en_GB'))
    def test_build_view_context_for_calculated_summary_for_repeating_group(self):
        block_type = 'CalculatedSummary'
        schema_context = self.schema_context
        schema_context['group_instance_id'] = 'bbb-group-instance-id'
        current_location = Location('member-group', 1, 'currency-total-playback')

        context = build_view_context_for_calculated_summary(self.metadata, self.schema, self.answer_store, schema_context, block_type,
                                                            current_location)

        self.check_context(context)

        context_summary = context['summary']

        self.assertEqual(len(context_summary['groups']), 1)
        self.assertEqual(context_summary['title'], 'We calculate the total of currency values entered for Bbb to be £24.00. Is this correct?')
        self.assertEqual(context_summary['groups'][0]['blocks'][0]['questions'][0]['answers'][0]['value'], 2)
        self.assertEqual(context_summary['groups'][0]['blocks'][1]['questions'][0]['answers'][0]['value'], 22)

    def test_build_view_context_for_final_summary_for_repeating_group(self):
        block_type = 'Summary'
        block = self.schema.get_block('summary')

        context = build_view_context_for_final_summary(self.metadata, self.schema, self.answer_store, self.schema_context,
                                                       block_type, block)

        self.check_context(context)

        context_summary = context['summary']

        self.assertEqual(len(context_summary['groups']), 7)

        self.assertEqual(context_summary['groups'][0]['title'], 'Your Details')
        self.assertEqual(context_summary['groups'][1]['title'], 'Other Household Members')
        self.assertIsNone(context_summary['groups'][2]['title'])
        self.assertIsNone(context_summary['groups'][3]['title'])
        self.assertEqual(context_summary['groups'][4]['title'], 'Aaa')
        self.assertEqual(context_summary['groups'][5]['title'], 'Bbb')
        self.assertEqual(context_summary['groups'][6]['title'], 'Ccc')

        self.assertEqual(context_summary['groups'][0]['blocks'][0]['questions'][0]['answers'][0]['value'], 'Aaa')
        self.assertEqual(context_summary['groups'][1]['blocks'][0]['questions'][0]['answers'][0]['value'], 'Bbb')
        self.assertEqual(context_summary['groups'][2]['blocks'][0]['questions'][0]['answers'][0]['value'], 'Ccc')

        self.assertEqual(context_summary['groups'][4]['blocks'][0]['questions'][0]['title'].endswith('Aaa'), True)
        self.assertEqual(context_summary['groups'][5]['blocks'][0]['questions'][0]['title'].endswith('Bbb'), True)
        self.assertEqual(context_summary['groups'][6]['blocks'][0]['questions'][0]['title'].endswith('Ccc'), True)

        self.assertEqual(context_summary['groups'][4]['blocks'][0]['questions'][0]['answers'][0]['value'], 1)
        self.assertEqual(context_summary['groups'][4]['blocks'][1]['questions'][0]['answers'][0]['value'], 11)
        self.assertEqual(context_summary['groups'][5]['blocks'][0]['questions'][0]['answers'][0]['value'], 2)
        self.assertEqual(context_summary['groups'][5]['blocks'][1]['questions'][0]['answers'][0]['value'], 22)
        self.assertEqual(context_summary['groups'][6]['blocks'][0]['questions'][0]['answers'][0]['value'], 3)
        self.assertEqual(context_summary['groups'][6]['blocks'][1]['questions'][0]['answers'][0]['value'], 33)


class TestAnswerSummaryContext(TestStandardSummaryContext):

    def setUp(self):
        super().setUp()
        self.schema = load_schema_from_params('test', 'answer_summary')
        self.answer_store = AnswerStore()
        self.block_type = 'AnswerSummary'

    def test_build_view_context_for_answer_summary(self):
        primary_uuid = uuid.uuid4()
        repeating_0_uuid = uuid.uuid4()
        repeating_1_uuid = uuid.uuid4()
        self.answer_store.add_or_update(Answer('primary-first-name', 'Bob', primary_uuid, 0, 0))
        self.answer_store.add_or_update(Answer('primary-last-name', 'Smith', primary_uuid, 0, 0))
        self.answer_store.add_or_update(Answer('primary-anyone-else', 'Yes', primary_uuid, 0, 0))
        self.answer_store.add_or_update(Answer('repeating-first-name', 'Mary', repeating_0_uuid, 0, 0))
        self.answer_store.add_or_update(Answer('repeating-last-name', 'Smith', repeating_0_uuid, 0, 0))
        self.answer_store.add_or_update(Answer('repeating-anyone-else', 'Yes', repeating_0_uuid, 0, 0))
        self.answer_store.add_or_update(Answer('repeating-first-name', 'Sally', repeating_1_uuid, 1, 0))
        self.answer_store.add_or_update(Answer('repeating-last-name', 'Smith', repeating_1_uuid, 1, 0))

        current_location = Location(
            block_id='household-summary',
            group_id='household-summary-group',
            group_instance=0,
        )

        with self.app_request_context('/'):
            context = build_view_context(self.block_type, self.metadata, self.schema, self.answer_store,
                                         None, None, current_location, None)

        self.check_context(context)
        self.assertEqual(len(context['summary']), 6)
        self.assertTrue('title' in context['summary'])
        self.assertTrue('icon' in context['summary'])
        self.assertEqual('person', context['summary']['icon'])
        self.assertEqual(1, len(context['summary']['groups']))

        summary_answers = context['summary']['groups'][0]['answers']
        labels = [summary_answer['label'] for summary_answer in summary_answers]
        self.assertIn('Bob Smith', labels)
        self.assertIn('Mary Smith', labels)
        self.assertIn('Sally Smith', labels)
