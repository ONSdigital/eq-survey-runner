import unittest
from unittest.mock import Mock

from app.validation.validators import OptionalForm
from wtforms.validators import StopValidation


class TestOptionalFormValidator(unittest.TestCase):
    def test_date_optional_empty(self):
        validator = OptionalForm()

        mock_form = Mock()

        mock_day = Mock()
        mock_month = Mock()
        mock_year = Mock()

        mock_day.raw_data = ['']
        mock_month.raw_data = []
        mock_year.raw_data = ['']

        mock_form.__iter__ = Mock(return_value=iter([mock_day, mock_month, mock_year]))

        mock_field = Mock()

        with self.assertRaises(StopValidation) as ite:
            validator(mock_form, mock_field)

        self.assertEqual('', str(ite.exception))

    def test_month_year_optional_month_empty(self):
        validator = OptionalForm()

        mock_form = Mock()

        mock_month = Mock()
        mock_year = Mock()

        mock_month.raw_data = []
        mock_year.raw_data = ['']

        mock_form.__iter__ = Mock(return_value=iter([mock_month, mock_year]))

        mock_field = Mock()

        with self.assertRaises(StopValidation) as ite:
            validator(mock_form, mock_field)

        self.assertEqual('', str(ite.exception))

    def test_date_optional_missing_day(self):

        validator = OptionalForm()

        mock_form = Mock()

        mock_day = Mock()
        mock_month = Mock()
        mock_year = Mock()

        mock_day.raw_data = ['']
        mock_month.raw_data = ['01']
        mock_year.raw_data = ['2015']

        mock_form.__iter__ = Mock(return_value=iter([mock_day, mock_month, mock_year]))

        mock_field = Mock()

        try:
            validator(mock_form, mock_field)
        except StopValidation:
            self.fail("Date that needs checking raised StopValidation")

    def test_month_year_optional_missing_year(self):

        validator = OptionalForm()

        mock_form = Mock()

        mock_month = Mock()
        mock_year = Mock()

        mock_month.raw_data = ['01']
        mock_year.raw_data = ['']

        mock_form.__iter__ = Mock(return_value=iter([mock_month, mock_year]))

        mock_field = Mock()

        try:
            validator(mock_form, mock_field)
        except StopValidation:
            self.fail("Date that needs checking raised StopValidation")
