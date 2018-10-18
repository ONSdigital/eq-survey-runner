from tests.integration.components.mutually_exclusive.schema_urls import MUTUALLY_EXCLUSIVE_UNIT
from tests.integration.integration_test_case import IntegrationTestCase


class TestUnitSingleCheckboxOverride(IntegrationTestCase):
    """
    Tests to ensure that the server-side validation for mutually exclusive unit
    with single checkbox override function as expected. These tests emulate the non-JS version.
    """

    def setUp(self):
        super().setUp()
        self.launchSurvey('test', 'mutually_exclusive')
        self.get(MUTUALLY_EXCLUSIVE_UNIT)

    def test_non_exclusive_answer(self):
        # When
        self.post({'unit-answer': '123'})

        # Then
        self.assertInUrl('section-summary')
        self.assertInBody('123')

    def test_exclusive_answer(self):
        # When
        self.post({'unit-answer': '',
                   'unit-exclusive-answer': ['I prefer not to say']})

        # Then
        self.assertInUrl('section-summary')
        self.assertInBody('I prefer not to say')

    def test_optional_exclusive_question(self):
        # When
        self.post({'unit-answer': ''})

        # Then
        self.assertInUrl('section-summary')
        self.assertInBody('No answer provided')

    def test_invalid_exclusive_answers(self):
        # When
        self.post({'unit-answer': '123',
                   'unit-exclusive-answer': ['I prefer not to say']})

        # Then
        self.assertInBody('Remove an answer to continue.')
