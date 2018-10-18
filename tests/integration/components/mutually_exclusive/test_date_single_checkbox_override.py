from tests.integration.components.mutually_exclusive.schema_urls import MUTUALLY_EXCLUSIVE_DAY_MONTH_YEAR_DATE
from tests.integration.integration_test_case import IntegrationTestCase


class TestDateSingleCheckboxOverride(IntegrationTestCase):
    """
    Tests to ensure that the server-side validation for mutually exclusive date
    with single checkbox override function as expected. These tests emulate the non-JS version.
    """

    def setUp(self):
        super().setUp()
        self.launchSurvey('test', 'mutually_exclusive')
        self.get(MUTUALLY_EXCLUSIVE_DAY_MONTH_YEAR_DATE)

    def test_non_exclusive_answer(self):
        # When
        self.post({'date-answer-day': '10',
                   'date-answer-month': '9',
                   'date-answer-year': '2018'})

        # Then
        self.assertInUrl('section-summary')
        self.assertInBody('10 September 2018')

    def test_exclusive_answer(self):
        # When
        self.post({'date-answer-day': '',
                   'date-answer-month': '',
                   'date-answer-year': '',
                   'date-exclusive-answer': ['I prefer not to say']})

        # Then
        self.assertInUrl('section-summary')
        self.assertInBody('I prefer not to say')

    def test_optional_exclusive_question(self):
        # When
        self.post()

        # Then
        self.assertInUrl('section-summary')
        self.assertInBody('No answer provided')

    def test_invalid_exclusive_answers(self):
        # When
        self.post({'date-answer-day': '10',
                   'date-answer-month': '9',
                   'date-answer-year': '2018',
                   'date-exclusive-answer': ['I prefer not to say']})

        # Then
        self.assertInBody('Remove an answer to continue.')
