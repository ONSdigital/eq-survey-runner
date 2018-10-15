import unittest
from unittest.mock import Mock
from wtforms.validators import StopValidation

from app.validation.error_messages import error_messages
from app.validation.validators import YearCheck


class TestYearValidator(unittest.TestCase):
    def test_year_date_validator_none(self):
        validator = YearCheck()

        mock_form = Mock()
        mock_form.year.data = None

        mock_field = Mock()

        with self.assertRaises(StopValidation) as ite:
            validator(mock_form, mock_field)

        self.assertEqual(error_messages['INVALID_DATE'], str(ite.exception))

    def test_year_date_validator_empty_string(self):

        validator = YearCheck()

        mock_form = Mock()
        mock_form.year.data = ''

        mock_field = Mock()

        with self.assertRaises(StopValidation) as ite:
            validator(mock_form, mock_field)

        self.assertEqual(error_messages['INVALID_DATE'], str(ite.exception))

    def test_year_date_validator_invalid(self):
        validator = YearCheck()

        mock_form = Mock()
        mock_form.year.data = 'abcd'

        mock_field = Mock()

        with self.assertRaises(StopValidation) as ite:
            validator(mock_form, mock_field)

        self.assertEqual(error_messages['INVALID_DATE'], str(ite.exception))

    def test_year_date_validator_invalid_year(self):
        validator = YearCheck()

        mock_form = Mock()
        mock_form.year.data = '17'

        mock_field = Mock()

        with self.assertRaises(StopValidation) as ite:
            validator(mock_form, mock_field)

        self.assertEqual(error_messages['INVALID_DATE'], str(ite.exception))

    def test_year_date_validator_valid(self):
        validator = YearCheck()

        mock_form = Mock()
        mock_form.year.data = '2017'

        mock_field = Mock()

        try:
            validator(mock_form, mock_field)
        except StopValidation:
            self.fail('Valid date raised ValidationError')
