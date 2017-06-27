import unittest
from unittest.mock import Mock
from wtforms.fields import Field
from app.forms.custom_fields import MaxTextAreaField


class TestMaxTextAreaField(unittest.TestCase):

    def setUp(self):
        self.mock_form = Mock()

    def test_is_a_wtforms_field(self):
        text_area = MaxTextAreaField('LabelText', _form=self.mock_form, _name='aName')
        self.assertIsInstance(text_area, Field)

    def test_supports_maxlength_property(self):
        text_area = MaxTextAreaField('TestLabel', maxlength=20, _form=self.mock_form, _name='aName')
        self.assertEqual(text_area.maxlength, 20)
