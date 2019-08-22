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
        self.launchSurvey('test_answer_action_redirect_to_list_add_question_radio')

        # When
        self.post({'anyone-usually-live-at-answer': 'Yes'})

        # Then
        self.assertInUrl(
            '/questionnaire/people/add-person/?return_to=anyone-usually-live-at'
        )

    def test_previous_link_when_list_empty_with_return_to_query_string(self):
        # Given
        self.launchSurvey('test_answer_action_redirect_to_list_add_question_radio')
        self.post({'anyone-usually-live-at-answer': 'Yes'})

        # When
        self.get(self.get_previous_link())

        # Then
        self.assertInUrl('/questionnaire/anyone-usually-live-at/')

    def test_previous_link_when_list_not_empty(self):
        # Given
        self.launchSurvey('test_answer_action_redirect_to_list_add_question_radio')
        self.post({'anyone-usually-live-at-answer': 'Yes'})
        self.add_person('John', 'Doe')
        self.post({'anyone-else-live-at-answer': 'Yes'})

        # When
        self.get(self.get_previous_link())

        # Then
        self.assertInUrl('/questionnaire/anyone-else-live-at/')

    def test_previous_link_return_to_list_collector_when_invalid_return_to_block_id(
        self
    ):
        # Given
        self.launchSurvey('test_answer_action_redirect_to_list_add_question_radio')
        self.post({'anyone-usually-live-at-answer': 'Yes'})

        url_with_invalid_return_to = self.last_url + '-invalid'

        self.get(url_with_invalid_return_to)

        self.assertInUrl('?return_to=anyone-usually-live-at-invalid')

        # When
        self.get(self.get_previous_link())

        # Then
        self.assertInUrl('/questionnaire/anyone-else-live-at/')
