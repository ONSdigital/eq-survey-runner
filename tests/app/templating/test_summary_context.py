import unittest

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
                }

    def setUp(self):
        self.schema_json, self.schema = load_and_parse_schema('0', 'star_wars')

    def test_build_summary_rendering_context(self):
        answers = MagicMock()
        routing_path = ['f22b1ba4-d15f-48b8-a1f3-db62b6f34cc0']
        navigator = Mock()
        navigator.get_routing_path = Mock(return_value=routing_path)

        with patch('app.templating.summary_context.get_navigator', return_value=navigator):
            context = build_summary_rendering_context(self.schema_json, answers)

        self.assertEqual(len(context), 1)
