from tests.integration.integration_test_case import IntegrationTestCase


class TestCheckboxSingleCheckboxOverride(IntegrationTestCase):
    """
    Tests to ensure that the server-side validation for mutually exclusive checkbox
    with single checkbox override function as expected. These tests emulate the non-JS version.
    """

    def setUp(self):
        super().setUp()
        self.launchSurvey('test', 'mutually_exclusive')

    def test_non_exclusive_answer(self):
        # When
        self.post({'checkbox-answer': ['British', 'Irish']})

        # Then
        self.assertInUrl('section-summary')
        self.assertInBody('British')
        self.assertInBody('Irish')

    def test_exclusive_answer(self):
        # When
        self.post({'checkbox-exclusive-answer': ['I prefer not to say']})

        # Then
        self.assertInUrl('section-summary')
        self.assertInBody('I prefer not to say')

    def test_mandatory_exclusive_question(self):
        # When
        self.post()

        # Then
        self.assertInBody('Enter an answer to continue.')

    def test_invalid_exclusive_answers(self):
        # When
        self.post({'checkbox-answer': ['British', 'Irish', 'Other'],
                   'checkbox-child-other-answer': 'Other field input',
                   'checkbox-exclusive-answer': ['I prefer not to say']})

        # Then
        self.assertInBody('Remove an answer to continue.')
