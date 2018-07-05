from tests.integration.integration_test_case import IntegrationTestCase


class TestCheckboxMutuallyExclusive(IntegrationTestCase):
    """
    Tests to ensure that the server-side validation for mutually exclusive
    checkboxes function as expected. These tests emulate the non-JS version.
    """

    def setUp(self):
        super().setUp()
        self.launchSurvey('test', 'checkbox_mutually_exclusive')

    def test_non_exclusive_options(self):

        # When
        self.post({'mandatory-checkbox-answer': ['Pineapple', 'Tuna']})

        # Then
        self.assertInUrl('summary')
        self.assertInPage('Pineapple')
        self.assertInPage('Tuna')

    def test_exclusive_option(self):

        # When
        self.post({'mandatory-checkbox-answer': ['No extra']})

        # Then
        self.assertInUrl('summary')
        self.assertInPage('No extra toppings')

    def test_invalid_exclusive_options(self):

        # When
        self.post({'mandatory-checkbox-answer': ['Pineapple', 'Tuna', 'No extra']})

        # Then
        self.assertInPage('Uncheck "Pineapple" and "Tuna" or "No extra toppings" to continue')
