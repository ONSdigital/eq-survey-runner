from app.forms.duration_form import get_duration_form
from app.validation.error_messages import error_messages
from tests.app.app_context_test_case import AppContextTestCase


class TestDurationForm(AppContextTestCase):
    def test_empty(self):
        form_class = get_duration_form(
            {'mandatory': False, 'units': ['years', 'months']}, error_messages
        )
        self.assertIsNone(form_class().data)

    def test_zero(self):
        form_class = get_duration_form(
            {'mandatory': False, 'units': ['years', 'months']}, error_messages
        )
        form = form_class()
        form.years.raw_data = ['0']
        form.years.data = 0
        form.months.raw_data = ['0']
        form.months.data = 0

        self.assertEqual(form.data['years'], 0)
        self.assertEqual(form.data['months'], 0)

    def test_year_month_validation(self):
        self._test_validation(False, '5', '4', True)
        self._test_validation(True, '5', '4', True)
        self._test_validation(False, '', '', True)
        self._test_validation(
            True, '', '', False, error='Enter a duration to continue.'
        )
        self._test_validation(False, '5', '', False, error='Enter a valid duration.')
        self._test_validation(True, '5', '', False, error='Enter a valid duration.')
        self._test_validation(False, '', '4', False, error='Enter a valid duration.')
        self._test_validation(True, '', '4', False, error='Enter a valid duration.')
        self._test_validation(
            False, '5', 'word', False, error='Enter a valid duration.'
        )
        self._test_validation(True, '5', 'word', False, error='Enter a valid duration.')
        self._test_validation(False, '5', '12', False, error='Enter a valid duration.')
        self._test_validation(True, '5', '12', False, error='Enter a valid duration.')
        self._test_validation(False, '5', '-1', False, error='Enter a valid duration.')
        self._test_validation(True, '5', '-1', False, error='Enter a valid duration.')
        self._test_validation(False, '-1', '4', False, error='Enter a valid duration.')
        self._test_validation(True, '-1', '4', False, error='Enter a valid duration.')

    def test_year_validation(self):
        self._test_validation(False, '5', None, True)
        self._test_validation(True, '5', None, True)
        self._test_validation(False, '', None, True)
        self._test_validation(
            True, '', None, False, error='Enter a duration to continue.'
        )
        self._test_validation(
            False, 'word', None, False, error='Enter a valid duration.'
        )
        self._test_validation(
            True, 'word', None, False, error='Enter a valid duration.'
        )
        self._test_validation(False, '-1', None, False, error='Enter a valid duration.')
        self._test_validation(True, '-1', None, False, error='Enter a valid duration.')

    def test_month_validation(self):
        self._test_validation(False, None, '5', True)
        self._test_validation(True, None, '5', True)
        self._test_validation(False, None, '', True)
        self._test_validation(
            True, None, '', False, error='Enter a duration to continue.'
        )
        self._test_validation(
            False, None, 'word', False, error='Enter a valid duration.'
        )
        self._test_validation(
            True, None, 'word', False, error='Enter a valid duration.'
        )
        self._test_validation(False, None, '-1', False, error='Enter a valid duration.')
        self._test_validation(True, None, '-1', False, error='Enter a valid duration.')
        self._test_validation(False, None, '12', True)
        self._test_validation(True, None, '12', True)

    def _test_validation(self, mandatory, years, months, valid, error=None):
        units = []
        if years is not None:
            units.append('years')
        if months is not None:
            units.append('months')

        form_class = get_duration_form(
            {'mandatory': mandatory, 'units': units}, error_messages
        )

        form = form_class()
        if years is not None:
            form.years.raw_data = [years]
            form.years.data = to_int(years)
        if months is not None:
            form.months.raw_data = [months]
            form.months.data = to_int(months)

        with self.app_request_context('/'):
            self.assertEqual(form.validate(), valid)

            if error:
                self.assertEqual(getattr(form, units[0]).errors[0], error)


def to_int(value):
    try:
        return int(value)
    except ValueError:
        return None
