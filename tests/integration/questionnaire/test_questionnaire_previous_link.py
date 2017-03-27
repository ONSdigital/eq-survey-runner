from tests.integration.integration_test_case import IntegrationTestCase


class TestQuestionnairePreviousLink(IntegrationTestCase):

    def test_previous_link_doesnt_appear_on_introduction(self):
        # Given
        self.launchSurvey('test', 'final_confirmation')
        # When we open the introduction
        # Then previous link does not appear
        self.assertNotInPage('Previous')

    def test_previous_link_doesnt_appear_on_page_following_introduction(self):
        # Given
        self.launchSurvey('test', 'final_confirmation')

        # When we proceed through the questionnaire
        self.post(action='start_questionnaire')
        self.assertInPage('Previous')
        self.post({'breakfast-answer': 'Bacon'})
        self.assertNotInUrl('thank-you')
        self.assertNotInPage('Previous')

    def test_previous_link_doesnt_appear_on_thank_you(self):
        # Given
        self.launchSurvey('test', 'final_confirmation')

        # When ee proceed through the questionnaire
        self.post(action='start_questionnaire')
        self.post({'breakfast-answer': 'Eggs'})
        self.post(action=None)
        self.assertInUrl('thank-you')
        self.assertNotInUrl('Previous')

    def test_previous_link_on_relationship(self):

        # Given the census questionnaire.
        self.launchSurvey('census', 'household')

        # When we complete the who lives here section and the other questions needed to build the path.
        self.post({'permanent-or-family-home-answer': 'Yes'})

        post_data = {
            'household-0-first-name': 'Joe',
            'household-0-middle-names': '',
            'household-0-last-name': 'Bloggs',
            'household-1-first-name': 'Jane',
            'household-1-middle-names': '',
            'household-1-last-name': 'Bloggs',
            'household-2-first-name': 'Holly',
            'household-2-middle-names': '',
            'household-2-last-name': 'Bloggs',
        }

        self.post(post_data)

        self.post({'overnight-visitors-answer': '0'})

        # Then there should be a previous link on all repeating household blocks.
        self.assertInPage('Previous')

        self.get('questionnaire/census/household/789/who-lives-here-relationship/1/household-relationships')
        self.assertInPage('Previous')
