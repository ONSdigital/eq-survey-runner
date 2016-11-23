import unittest

from app import create_app
from mock import MagicMock, Mock, patch

from app.templating.summary_context import build_summary_rendering_context
from app.utilities.schema import load_and_parse_schema


class TestSummaryContext(unittest.TestCase):

    metadata = {'return_by': '2016-10-10',
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
        self.app = create_app()
        self.app.config['SERVER_NAME'] = "test"
        self.app_context = self.app.app_context()
        self.app_context.push()

        self.schema_json, self.schema = load_and_parse_schema('0', 'star_wars')

    def test_build_summary_rendering_context(self):
        answer_store = MagicMock()
        routing_path = [{
            'block_id': 'f22b1ba4-d15f-48b8-a1f3-db62b6f34cc0',
            'group_id': '14ba4707-321d-441d-8d21-b8367366e766',
            'group_instance': 0,
        }]
        navigator = Mock()
        navigator.get_routing_path = Mock(return_value=routing_path)

        with patch('app.templating.summary_context.Navigator', return_value=navigator):
            context = build_summary_rendering_context(self.schema_json, answer_store, self.metadata)

        self.assertEqual(len(context), 1)
