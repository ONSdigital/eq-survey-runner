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

    def test_title_placeholders_rendered_in_summary_using_correct_language(self):
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
        self.assertInBody('1 February 1999')

        self.get(self.last_url + '?language_code=cy')

        self.assertInUrl('/summary/?language_code=cy')
        self.assertInBody('What is Kevin Bacon date of birth?')
        self.assertInBody('1 Chwefror 1999')
