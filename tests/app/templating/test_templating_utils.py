import unittest
from mock import patch
from app.templating.utils import get_question_title


class TestTemplatingUtils(unittest.TestCase):

    def test_get_question_title_returns_empty_title(self):
        expected_value = ''
        test_schema = {'title': expected_value}

        actual_value = get_question_title(test_schema, None, None, None)

        self.assertEqual(expected_value, actual_value)

    def test_get_question_title_no_title_results_in_titles_resolution(self):
        expected_value = 'TitlesElement'
        test_schema = {}

        with patch('app.templating.utils.get_title_from_titles', return_value='TitlesElement'):
            actual_value = get_question_title(test_schema, None, None, None)
            self.assertEqual(expected_value, actual_value)

    def test_get_question_title_title_returned_if_present(self):
        expected_value = 'MyTitle'
        test_schema = {'title': expected_value}

        actual_value = get_question_title(test_schema, None, None, None)

        self.assertEqual(expected_value, actual_value)

    def test_default_titles_if_no_when_clauses(self):
        expected_value = 'MyTitle'
        test_schema = {'titles': [{'value': expected_value}]}

        actual_value = get_question_title(test_schema, None, None, None)
        self.assertEqual(expected_value, actual_value)

    def test_evaluates_when_rule_if_present(self):
        expected_value = 'MyTitle'
        test_schema = {
            'titles':
                [{
                    'value': expected_value,
                    'when': [{
                        'id': 'behalf-of-answer',
                        'condition': 'equals',
                        'value': 'chad'
                    }]
                }]
            }

        with patch('app.templating.utils.evaluate_when_rules', return_value=True):
            actual_value = get_question_title(test_schema, None, None, None)
            self.assertEqual(expected_value, actual_value)
