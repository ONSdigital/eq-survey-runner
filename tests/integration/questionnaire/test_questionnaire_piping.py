from tests.integration.integration_test_case import IntegrationTestCase


class TestQuestionnairePiping(IntegrationTestCase):

    def test_given_quotes_in_answer_when_piped_into_page_then_html_escaped_quotes_on_page(self):
        # Given
        self.launchSurvey('census', 'household')
        self.post({'address-line-1': '44 hill side'})
        self.post({'permanent-or-family-home-answer': 'Yes'})

        # When
        self.post({'household-0-first-name': 'Joe Bloggs "Junior"'})

        # Then
        self.get(self.last_url)
        self.assertStatusOK()
        self.assertInPage('Joe Bloggs &#34;Junior&#34;')

    def test_given_backslash_in_answer_when_piped_into_page_then_backslash_on_page(self):
        # Given
        self.launchSurvey('census', 'household')
        self.post({'address-line-1': '44 hill side'})
        self.post({'permanent-or-family-home-answer': 'Yes'})

        # When
        self.post({'household-0-first-name': 'Joe Bloggs\\John Doe'})

        # Then
        self.get(self.last_url)
        self.assertStatusOK()
        self.assertInPage('Joe Bloggs\\John Doe')
