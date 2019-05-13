import unittest
from unittest.mock import Mock
from wtforms.fields import Field
from app.forms.custom_fields import (
    MaxTextAreaField,
    CustomIntegerField,
    CustomDecimalField,
)


class TestMaxTextAreaField(unittest.TestCase):
    def setUp(self):
        self.mock_form = Mock()

    def test_text_area_a_wtforms_field(self):
        text_area = MaxTextAreaField('LabelText', _form=self.mock_form, _name='aName')
        self.assertIsInstance(text_area, Field)

    def test_text_area_supports_maxlength_property(self):
        text_area = MaxTextAreaField(
            'TestLabel', maxlength=20, _form=self.mock_form, _name='aName'
        )
        self.assertIsInstance(text_area, Field)
        self.assertEqual(text_area.maxlength, 20)

    def test_integer_field(self):
        integer_field = CustomIntegerField(_form=self.mock_form, _name='aName')
        self.assertIsInstance(integer_field, Field)

        try:
            integer_field.process_formdata(['NonInteger'])
        except IndexError:
            self.fail('Exceptions should not thrown by CustomIntegerField')

    def test_decimal_field(self):
        decimal_field = CustomDecimalField(_form=self.mock_form, _name='aName')
        self.assertIsInstance(decimal_field, Field)

        try:
            decimal_field.process_formdata(['NonDecimal'])
        except IndexError:
            self.fail('Exception should not be thrown by CustomDecimalField')
