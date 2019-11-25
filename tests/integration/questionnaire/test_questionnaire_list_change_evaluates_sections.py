from tests.integration.integration_test_case import IntegrationTestCase


class TestQuestionnaireListChangeEvaluatesSections(IntegrationTestCase):
    def add_person(self, first_name, last_name):
        self.post({'anyone-else': 'Yes'})
        self.post({'first-name': first_name, 'last-name': last_name})

    def get_link(self, rowIndex, text):
        selector = f'tbody:nth-child({rowIndex}) td:last-child a'
        selected = self.getHtmlSoup().select(selector)

        filtered = [html for html in selected if text in html.get_text()]

        return filtered[0].get('href')

    def get_previous_link(self):
        selector = '#top-previous'
        selected = self.getHtmlSoup().select(selector)
        return selected[0].get('href')

    def test_happy_path(self):
        self.launchSurvey('test_list_change_evaluates_sections')

        self.get('/questionnaire/sections/who-lives-here')
        self.assertEqualUrl('/questionnaire/list-collector/')

        self.post({'anyone-else': 'No'})
        self.assertEqualUrl('/questionnaire/')

        self.get('/questionnaire/sections/accommodation-section/')
        self.assertEqualUrl('/questionnaire/accommodation-type/')

        self.post(action='save_continue')
        self.post(action='save_continue')
        self.post(action='save_continue')
        self.post(action='save_continue')
        self.post()
        self.assertEqualUrl('/questionnaire/')

        self.get('/questionnaire/sections/who-lives-here')
        self.assertEqualUrl('/questionnaire/list-collector/')

        self.add_person('John', 'Doe')
        self.post({'anyone-else': 'No'})
        self.assertEqualUrl('/questionnaire/')

        self.assertInSelector(
            'Partially completed', 'tbody:nth-child(2) td:nth-child(2)'
        )

        self.get('questionnaire/sections/accommodation-section/')
        self.assertEqualUrl('/questionnaire/own-or-rent/')
