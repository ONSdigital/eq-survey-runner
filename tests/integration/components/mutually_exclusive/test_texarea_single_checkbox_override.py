from tests.integration.components.mutually_exclusive.schema_urls import MUTUALLY_EXCLUSIVE_TEXTAREA
from tests.integration.integration_test_case import IntegrationTestCase


class TestTextAreaSingleCheckboxOverride(IntegrationTestCase):
    """
    Tests to ensure that the server-side validation for mutually exclusive textarea
    with single checkbox override function as expected. These tests emulate the non-JS version.
    """

    def setUp(self):
        super().setUp()
        self.launchSurvey('test', 'mutually_exclusive')
        self.get(MUTUALLY_EXCLUSIVE_TEXTAREA)

    def test_non_exclusive_answer(self):
        # When
        self.post({'textarea-answer': 'John Doe'})

        # Then
        self.assertInUrl('section-summary')
        self.assertInBody('John Doe')

    def test_exclusive_answer(self):
        # When
        self.post({'textarea-answer': '',
                   'textarea-exclusive-answer': ['I prefer not to say']})

        # Then
        self.assertInUrl('section-summary')
        self.assertInBody('I prefer not to say')

    def test_optional_exclusive_question(self):
        # When
        self.post({'textarea-answer': ''})

        # Then
        self.assertInUrl('section-summary')
        self.assertInBody('No answer provided')

    def test_invalid_exclusive_answers(self):
        # When
        self.post({'textarea-answer': 'John Doe',
                   'textarea-exclusive-answer': ['I prefer not to say']})

        # Then
        self.assertInBody('Remove an answer to continue.')
