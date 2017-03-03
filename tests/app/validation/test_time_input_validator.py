import unittest
from unittest.mock import Mock
from wtforms.validators import ValidationError
from app.validation.validators import TimeInputCheck
from wtforms.validators import StopValidation


class TestTimeInputValidator(unittest.TestCase):

    def test_time_input_validator_invalid_hours_range(self):
        validator = TimeInputCheck()

        mock_form = Mock()
        mock_form.hours.raw_data = [1000]
        mock_form.hours.data = 1000
        mock_form.mins.data = None

        mock_field = Mock()

        with self.assertRaises(ValidationError) as ite:
            validator(mock_form, mock_field)

    def test_time_input_validator_invalid_mins_range(self):
        validator = TimeInputCheck()

        mock_form = Mock()
        mock_form.hours.data = None
        mock_form.mins.raw_data = [70]
        mock_form.mins.data = 70
        mock_field = Mock()

        with self.assertRaises(ValidationError) as ite:
            validator(mock_form, mock_field)

    def test_time_input_validator_invalid_hours_non_integer(self):
        validator = TimeInputCheck()

        mock_form = Mock()
        mock_form.hours.data = "test"
        mock_form.mins.data = None

        mock_field = Mock()

        with self.assertRaises(StopValidation) as ite:
            validator(mock_form, mock_field)

    def test_time_input_validator_invalid_mins_non_integer(self):
        validator = TimeInputCheck()

        mock_form = Mock()
        mock_form.hours.data = None
        mock_form.mins.data = "test"

        mock_field = Mock()

        with self.assertRaises(StopValidation) as ite:
            validator(mock_form, mock_field)



