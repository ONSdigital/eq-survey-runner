from unittest import TestCase
from unittest.mock import MagicMock

from app.schema.widgets.multiple_choice_widget import MultipleChoiceWidget


class TestMultipleChoiceWidget(TestCase):

    def setUp(self):
        self.widget = MultipleChoiceWidget('multiple_choice_widget')

    def test_get_other_input_returns_none_for_empty_input(self):

        mock_dict = MagicMock()
        mock_dict.getlist = MagicMock(return_value=[])
        mock_dict.__len__ = MagicMock(return_value=0)

        assert self.widget.get_other_input({}) is None
        assert self.widget.get_other_input(mock_dict) is None

    def test_get_other_input_with_single_value(self):
        post_vars = {'answer': 'answer_value'}
        assert self.widget.get_other_input(post_vars) is None

    def test_get_other_input_when_other_value_supplied_returns_other_value(self):
        post_vars = {'multiple_choice_widget': ['Other', 'Other value']}
        assert self.widget.get_other_input(post_vars) == 'Other value'

    def test_get_other_input_when_other_selected_but_no_value_specified(self):
        post_vars = {'multiple_choice_widget': ['Other', '']}
        assert self.widget.get_other_input(post_vars) is None

    def test_get_other_input_with_multi_dict(self):
        post_vars = MagicMock()
        post_vars.getlist = MagicMock(return_value=['Other', 'Other value'])
        post_vars.__len__ = MagicMock(return_value=2)
        assert self.widget.get_other_input(post_vars) == 'Other value'
        post_vars.getlist.assert_called_once_with('multiple_choice_widget')

    def test_get_other_input_with_multi_dict_no_other_value(self):
        post_vars = MagicMock()
        post_vars.getlist = MagicMock(return_value=['Other', ''])
        post_vars.__len__ = MagicMock(return_value=2)
        assert self.widget.get_other_input(post_vars) is None
        post_vars.getlist.assert_called_once_with('multiple_choice_widget')

    def test_get_other_input_single_value_returns_none(self):
        post_vars = {'multiple_choice_widget': ['Some value']}
        assert self.widget.get_other_input(post_vars) is None
        assert self.widget.get_user_input(post_vars) == ['Some value']

    def test_get_other_value_when_blank_returns_other(self):
        post_vars = {'multiple_choice_widget': ['Other', '       ']}
        assert self.widget.get_other_input(post_vars) is None

    def test_get_other_value_when_single_value_called_other_returns_none(self):
        post_vars = {'multiple_choice_widget': ['Other']}
        assert self.widget.get_other_input(post_vars) is None
