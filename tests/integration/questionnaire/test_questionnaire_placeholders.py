from tests.integration.integration_test_case import IntegrationTestCase


class TestPlaceholders(IntegrationTestCase):
    def test_title_placeholders_rendered_in_summary(self):
        self.launchSurvey('test_placeholder_full')
        self.assertInBody('Please enter a name')
        self.post({'first-name': 'Kevin', 'last-name': 'Bacon'})

        self.assertInBody('What is Kevin Bacon’s date of birth?')

        self.post(
            {
                'date-of-birth-answer-day': 1,
                'date-of-birth-answer-month': 2,
                'date-of-birth-answer-year': 1999,
            }
        )

        self.post({'confirm-date-of-birth-answer-proxy': 'Yes'})

        self.assertInUrl('/summary/')
        self.assertInBody('What is Kevin Bacon’s date of birth?')
