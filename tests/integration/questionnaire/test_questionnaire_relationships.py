from tests.integration.integration_test_case import IntegrationTestCase


class TestQuestionnaireRelationships(IntegrationTestCase):
    def add_person(self, first_name, last_name):
        self.post({'anyone-else': 'Yes'})
        self.post({'first-name': first_name, 'last-name': last_name})

    def get_previous_link(self):
        selector = '#top-previous'
        selected = self.getHtmlSoup().select(selector)
        return selected[0].get('href')

    def test_valid_relationship(self):
        self.launchSurvey('test_relationships')
        self.add_person('Marie', 'Doe')
        self.add_person('John', 'Doe')
        self.post({'anyone-else': 'No'})

        self.post({'relationship-answer': 'Husband or Wife'})
        self.assertInUrl('/questionnaire/confirmation')

    def test_go_to_relationships_not_on_path(self):
        self.launchSurvey('test_relationships')
        self.get('/questionnaire/relationships')
        self.assertInUrl('/questionnaire/list-collector')

    def test_go_to_relationship_when_relationships_not_on_path(self):
        self.launchSurvey('test_relationships')
        self.get('/questionnaire/relationships/fake-id/to/another-fake-id')
        self.assertInUrl('/questionnaire/list-collector')

    def test_go_to_invalid_relationship(self):
        self.launchSurvey('test_relationships')
        self.add_person('Marie', 'Doe')
        self.add_person('John', 'Doe')
        self.post({'anyone-else': 'No'})

        self.get('/questionnaire/relationships/fake-id/to/another-fake-id')
        self.assertInUrl('/questionnaire/relationships')

    def test_failed_validation(self):
        self.launchSurvey('test_relationships')
        self.add_person('Marie', 'Doe')
        self.add_person('John', 'Doe')
        self.post({'anyone-else': 'No'})
        self.post()
        self.assertInBody('This page has an error')

    def test_save_sign_out(self):
        self.launchSurvey(
            'test_relationships',
            account_service_url='https://localhost/my-account',
            account_service_log_out_url='https://localhost/logout',
        )
        self.add_person('Marie', 'Doe')
        self.add_person('John', 'Doe')
        self.post({'anyone-else': 'No'})
        self.post(action='save_sign_out')
        self.assertInUrl('/logout')

    def test_multiple_relationships(self):
        self.launchSurvey('test_relationships')
        self.add_person('Marie', 'Doe')
        self.add_person('John', 'Doe')
        self.add_person('Susan', 'Doe')
        self.post({'anyone-else': 'No'})

        self.post({'relationship-answer': 'Husband or Wife'})
        self.post({'relationship-answer': 'Husband or Wife'})
        self.post({'relationship-answer': 'Husband or Wife'})

        self.assertInUrl('/questionnaire/confirmation')
