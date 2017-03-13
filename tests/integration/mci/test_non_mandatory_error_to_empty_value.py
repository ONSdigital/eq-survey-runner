from tests.integration.integration_test_case import IntegrationTestCase
from tests.integration.mci import mci_test_urls


class TestNonMandatoryErrorToEmptyValue(IntegrationTestCase):

    def test_non_mandatory_error_to_empty_value(self):
        self.launchSurvey('1', '0203')

        # We proceed to the questionnaire
        self.post(action='start_questionnaire')

        # We fill in our answers, generating a error in a non-mandatory field
        form_data = {
            # Start Date
            'total-sales-food': '01',
            'period-from-month': '4',
            'period-from-year': '2016',
            # End Date
            'period-to-day': '01',
            'period-to-month': '4',
            'period-to-year': '2017',
            # Non Mandatory field but fails validation as should be Integer
            'total-retail-turnover': 'failing test'
        }

        # We submit the form
        self.post(form_data)

        # Get the page content
        self.assertInPage("Please only enter whole numbers into the field")

        # We remove the non-mandatory field value
        form_data = {
            # Start Date
            'period-from-day': '01',
            'period-from-month': '4',
            'period-from-year': '2016',
            # End Date
            'period-to-day': '30',
            'period-to-month': '4',
            'period-to-year': '2016',
            # Total Turnover
            'total-retail-turnover': '100000'
        }

        # We submit the form
        self.post(form_data)

        # There are no validation errors
        self.assertInUrl(mci_test_urls.MCI_0203_SUMMARY)
