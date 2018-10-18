from tests.integration.components.mutually_exclusive.schema_urls import MUTUALLY_EXCLUSIVE_NUMBER
from tests.integration.integration_test_case import IntegrationTestCase


class TestNumberSingleCheckboxOverride(IntegrationTestCase):
    """
    Tests to ensure that the server-side validation for mutually exclusive number
    with single checkbox override function as expected. These tests emulate the non-JS version.
    """

    def setUp(self):
        super().setUp()
        self.launchSurvey('test', 'mutually_exclusive')
        self.get(MUTUALLY_EXCLUSIVE_NUMBER)

    def test_non_exclusive_answer(self):
        # When
        self.post({'number-answer': '1234567'})

        # Then
        self.assertInUrl('section-summary')
        self.assertInBody('1,234,567')

    def test_exclusive_answer(self):
        # When
        self.post({'number-answer': '',
                   'number-exclusive-answer': ['I prefer not to say']})

        # Then
        self.assertInUrl('section-summary')
        self.assertInBody('I prefer not to say')

    def test_optional_exclusive_question(self):
        # When
        self.post({'number-answer': ''})

        # Then
        self.assertInUrl('section-summary')
        self.assertInBody('No answer provided')

    def test_invalid_exclusive_answers(self):
        # When
        self.post({'number-answer': '1234567',
                   'number-exclusive-answer': ['I prefer not to say']})

        # Then
        self.assertInBody('Remove an answer to continue.')
