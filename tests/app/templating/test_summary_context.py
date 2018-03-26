from flask import g
from mock import MagicMock, Mock, patch

from app.data_model.answer_store import AnswerStore
from app.questionnaire.location import Location
from app.templating.summary_context import build_summary_rendering_context
from app.templating.view_context import build_view_context_for_summary
from app.utilities.schema import load_schema_from_params

from tests.app.app_context_test_case import AppContextTestCase


class TestSummaryContext(AppContextTestCase):

    metadata = {
        'return_by': '2016-10-10',
        'ref_p_start_date': '2016-10-10',
        'ref_p_end_date': '2016-10-10',
        'ru_ref': 'abc123',
        'ru_name': 'Mr Bloggs',
        'trad_as': 'Apple',
        'tx_id': '12345678-1234-5678-1234-567812345678',
        'period_str': '201610',
        'employment_date': '2016-10-10',
        'collection_exercise_sid': '789',
        'form_type': '0102',
        'eq_id': '1',
    }

    def setUp(self):
        super().setUp()
        self.schema = load_schema_from_params('0', 'star_wars')

    def test_build_summary_rendering_context(self):
        answer_store = MagicMock()
        routing_path = [Location(
            block_id='choose-your-side-block',
            group_id='star-wars',
            group_instance=0,
        )]
        navigator = Mock()
        navigator.get_full_routing_path = Mock(return_value=routing_path)

        with patch('app.templating.summary_context.PathFinder', return_value=navigator):
            context = build_summary_rendering_context(self.schema, self.schema.json['sections'], answer_store, self.metadata)

        self.assertEqual(len(context), 1)

    def test_summary_context_html_encodes_answers(self):
        answer_store = AnswerStore([{
            'answer_id': 'choose-your-side-answer',
            'block_id': '',
            'value': """<>"'&""",
            'answer_instance': 0,
        }])

        routing_path = [Location(
            block_id='choose-your-side-block',
            group_id='star-wars',
            group_instance=0,
        )]
        navigator = Mock()
        navigator.get_full_routing_path = Mock(return_value=routing_path)

        with patch('app.templating.summary_context.PathFinder', return_value=navigator):
            context = build_summary_rendering_context(self.schema, self.schema.json['sections'], answer_store, self.metadata)

        answer = context[0]['blocks'][0]['questions'][0]['answers'][0]
        self.assertEqual(answer['value'], '&lt;&gt;&#34;&#39;&amp;')


class TestSectionSummaryContext(AppContextTestCase):
    metadata = {
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
        'form_type': '0102',
        'eq_id': '1',
    }

    def setUp(self):
        super().setUp()
        self.schema = load_schema_from_params('test', 'section_summary')
        self.answer_store = AnswerStore()

    def test_build_summary_rendering_context(self):
        answer_store = MagicMock()
        current_location = Location(
            block_id='property-details-summary',
            group_id='property-details',
            group_instance=0,
        )
        routing_path = [Location(
            block_id='property-details-summary',
            group_id='property-details',
            group_instance=0,
        )]
        navigator = Mock()
        navigator.get_full_routing_path = Mock(return_value=routing_path)

        with patch('app.templating.summary_context.PathFinder', return_value=navigator):
            context = build_summary_rendering_context(self.schema, answer_store, self.metadata, current_location)

        self.assertEqual(len(context), 0)

    def test_build_view_context_for_summary(self):
        block_type = 'SectionSummary'
        csrf_token = None
        variables = None

        g.schema = load_schema_from_params('test', 'section_summary')

        section = g.schema.json
        current_location = Location(
            block_id='property-details-summary',
            group_id='property-details',
            group_instance=0,
        )

        context = build_view_context_for_summary(self.metadata, self.answer_store, section, block_type, variables,
                                                 csrf_token, current_location)

        self.assertEqual(len(context), 3)
