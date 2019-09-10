import re

from tests.integration.integration_test_case import IntegrationTestCase


class TestQuestionnaireListCollector(IntegrationTestCase):
    def get_previous_link(self):
        selector = '#top-previous'
        selected = self.getHtmlSoup().select(selector)
        return selected[0].get('href')

    def test_invalid_list_on_primary_personcollector(self):
        self.launchSurvey('test_list_collector_primary_person')

        self.get('/questionnaire/invalid/123423/add-or-edit-person/')

        self.assertInUrl('/questionnaire/primary-person-list-collector')

    def test_adding_then_removing_primary_person(self):
        self.launchSurvey('test_list_collector_primary_person')

        self.post({'you-live-here': 'Yes'})

        self.assertInBody('What is your name')

        self.post({'first-name': 'Marie', 'last-name': 'Day'})

        self.assertInBody('Does anyone else live here?')

        self.assertInBody('Marie Day')

        self.post({'anyone-else': 'Yes'})

        self.assertInBody('What is the name of the person')

        self.post({'first-name': 'James', 'last-name': 'May'})

        self.assertInBody('James May')

        self.get('/questionnaire/primary-person-list-collector')

        self.post({'you-live-here': 'No'})

        self.assertInUrl('anyone-usually-live-at')

        self.post({'anyone-usually-live-at-answer': 'Yes'})

        self.assertInBody('James May')

    def test_cannot_remove_primary_person_from_list_collector(self):
        self.launchSurvey('test_list_collector_primary_person')

        self.post({'you-live-here': 'Yes'})

        primary_person_list_item_id = re.search(
            r'people\/([a-zA-Z]*)\/add-or-edit-primary-person', self.last_url
        ).group(1)

        self.post({'first-name': 'Marie', 'last-name': 'Day'})

        self.post({'anyone-else': 'Yes'})

        self.post({'first-name': 'James', 'last-name': 'May'})

        self.get(f'questionnaire/people/{primary_person_list_item_id}/remove-person/')

        self.assertInUrl('list-collector')

        self.assertInBody('James May')
        self.assertInBody('Marie Day')
