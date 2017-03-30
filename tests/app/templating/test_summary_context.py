from mock import MagicMock, Mock, patch

from app.questionnaire.location import Location
from app.templating.summary_context import build_summary_rendering_context
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
        self.schema_json = load_schema_from_params('0', 'star_wars', None)

    def test_build_summary_rendering_context(self):
        answer_store = MagicMock()
        routing_path = [Location(
            block_id='choose-your-side-block',
            group_id='star-wars',
            group_instance=0,
        )]
        navigator = Mock()
        navigator.get_routing_path = Mock(return_value=routing_path)

        with patch('app.templating.summary_context.PathFinder', return_value=navigator):
            context = build_summary_rendering_context(self.schema_json, answer_store, self.metadata)

        self.assertEqual(len(context), 1)
