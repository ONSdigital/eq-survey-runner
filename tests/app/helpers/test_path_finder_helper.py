from unittest.mock import patch
from flask import g
from tests.app.app_context_test_case import AppContextTestCase

from app.helpers.path_finder_helper import path_finder


@patch('app.helpers.path_finder_helper.PathFinder')
@patch('app.helpers.path_finder_helper.get_metadata')
@patch('app.helpers.path_finder_helper.get_answer_store')
class TestPathFinderHelper(AppContextTestCase):
    def test_path_finder_instantiated_once(self, mock_path_finder, _, __):
        g.schema_json = {}

        # Werkzeug LocalProxy only instantiates an object on
        # attribute access. We use an example of a fake
        # method call to check the mock (which will be the PathFinder
        # class outside of this test) is only called once.
        path_finder.some_method_call()
        path_finder.some_method_call()
        self.assertEqual(1, len(mock_path_finder.mock_calls))
