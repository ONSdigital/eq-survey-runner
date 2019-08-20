from tests.integration.integration_test_case import IntegrationTestCase


class TestQuestionnaireListCollector(IntegrationTestCase):
    def add_person(self, first_name, last_name):
        self.post({'anyone-else': 'Yes'})
        self.post({'first-name': first_name, 'last-name': last_name})

    def get_previous_link(self):
        selector = '#top-previous'
        selected = self.getHtmlSoup().select(selector)
        return selected[0].get('href')

    def test_add_list_question_displayed_before_list_collector_and_return_to_in_url(
        self
    ):
        # Given
        self.launchSurvey('test_answer_action_redirect_to_list_add_question')

        # When
        self.post({'anyone-else-live-here-answer': 'Yes'})

        # Then
        self.assertInUrl(
            '/questionnaire/people/add-person/?return_to=anyone-else-live-here-block'
        )

    def test_previous_link_when_list_empty_with_return_to_query_string(self):
        # Given
        self.launchSurvey('test_answer_action_redirect_to_list_add_question')
        self.post({'anyone-else-live-here-answer': 'Yes'})

        # When
        self.get(self.get_previous_link())

        # Then
        self.assertInUrl('/questionnaire/anyone-else-live-here-block/')

    def test_previous_link_when_list_not_empty(self):
        # Given
        self.launchSurvey('test_answer_action_redirect_to_list_add_question')
        self.post({'anyone-else-live-here-answer': 'Yes'})
        self.add_person('John', 'Doe')
        self.post({'anyone-else': 'Yes'})

        # When
        self.get(self.get_previous_link())

        # Then
        self.assertInUrl('/questionnaire/list-collector/')
