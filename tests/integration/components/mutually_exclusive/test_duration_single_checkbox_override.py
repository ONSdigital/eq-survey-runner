from tests.integration.components.mutually_exclusive.schema_urls import MUTUALLY_EXCLUSIVE_DURATION
from tests.integration.integration_test_case import IntegrationTestCase


class TestDurationSingleCheckboxOverride(IntegrationTestCase):
    """
    Tests to ensure that the server-side validation for mutually exclusive duration
    with single checkbox override function as expected. These tests emulate the non-JS version.
    """

    def setUp(self):
        super().setUp()
        self.launchSurvey('test', 'mutually_exclusive')
        self.get(MUTUALLY_EXCLUSIVE_DURATION)

    def test_non_exclusive_answer(self):
        # When
        self.post({'duration-answer-months': '11',
                   'duration-answer-years': '1'})

        # Then
        self.assertInUrl('section-summary')
        self.assertInBody('1 year 11 months')

    def test_exclusive_answer(self):
        # When
        self.post({'duration-answer-months': '',
                   'duration-answer-years': '',
                   'duration-exclusive-answer': ['I prefer not to say']})

        # Then
        self.assertInUrl('section-summary')
        self.assertInBody('I prefer not to say')

    def test_optional_exclusive_question(self):
        # When
        self.post({'duration-answer-months': '',
                   'duration-answer-years': ''})

        # Then
        self.assertInUrl('section-summary')
        self.assertInBody('No answer provided')

    def test_invalid_exclusive_answers(self):
        # When
        self.post({'duration-answer-months': '11',
                   'duration-answer-years': '2',
                   'duration-exclusive-answer': ['I prefer not to say']})

        # Then
        self.assertInBody('Remove an answer to continue.')
