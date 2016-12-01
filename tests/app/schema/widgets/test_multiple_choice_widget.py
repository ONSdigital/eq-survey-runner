from unittest import TestCase

from werkzeug.datastructures import MultiDict

from app.schema.widgets.multiple_choice_widget import MultipleChoiceWidget


class MockMultipleChoiceWidget(MultipleChoiceWidget):
    def __init__(self):
        super().__init__('multiple_choice_widget')
        self.type = 'mock_multiple_choice_widget'

    @staticmethod
    def _build_options(schema_item, answer_state):
        pass


class TestMultipleChoiceWidget(TestCase):

    def setUp(self):

        self.widget = MockMultipleChoiceWidget()
        self.options = [{"label": "test","value": "test"}]

    def test_get_other_input_returns_none_for_empty_input(self):
        assert self.widget.get_other_input({}, self.options) is None
        assert self.widget.get_other_input(MultiDict(), self.options) is None

    def test_get_other_input_with_single_value(self):
        post_vars = {'answer': 'answer_value'}
        assert self.widget.get_other_input(post_vars, self.options) is None

    def test_get_other_input_when_other_value_supplied_returns_other_value(self):
        post_vars = {'multiple_choice_widget': ['other', 'Other value']}
        assert self.widget.get_other_input(post_vars, self.options) == 'Other value'

    def test_get_other_input_when_other_selected_but_no_value_specified(self):
        post_vars = {'multiple_choice_widget': ['Other', '']}
        assert self.widget.get_other_input(post_vars, self.options) is None

    def test_get_other_input_with_multi_dict(self):
        post_vars = MultiDict()
        post_vars.add('multiple_choice_widget', 'other')
        post_vars.add('multiple_choice_widget', 'Other value')
        assert self.widget.get_other_input(post_vars, self.options) == 'Other value'

    def test_get_other_input_with_multi_dict_no_other_value(self):
        post_vars = MultiDict()
        post_vars.add('multiple_choice_widget', 'Other')
        post_vars.add('multiple_choice_widget', '')
        assert self.widget.get_other_input(post_vars, self.options) is None

    def test_get_other_input_single_value_returns_none(self):
        post_vars = {'multiple_choice_widget': ['Some value']}
        assert self.widget.get_other_input(post_vars, self.options) is None
        assert self.widget.get_user_input(post_vars) == ['Some value']

    def test_get_other_value_when_blank_returns_other(self):
        post_vars = MultiDict()
        post_vars.add('multiple_choice_widget', 'Other')
        post_vars.add('multiple_choice_widget', '       ')
        assert self.widget.get_other_input(post_vars, self.options) is None

    def test_get_other_value_when_single_value_called_other_returns_none(self):
        post_vars = {'multiple_choice_widget': ['Other']}
        assert self.widget.get_other_input(post_vars, self.options) is None

    def test_get_other_input_with_multi_dict_other_not_selected(self):
        post_vars = MultiDict()
        post_vars.add('multiple_choice_widget', 'Another Option')
        post_vars.add('multiple_choice_widget', 'Other value')
        assert self.widget.get_other_input(post_vars, self.options) is None
