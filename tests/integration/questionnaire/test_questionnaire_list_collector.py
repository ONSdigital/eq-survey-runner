from tests.integration.integration_test_case import IntegrationTestCase


class TestQuestionnaireListCollector(IntegrationTestCase):
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

    def test_invalid_list_collector(self):
        self.launchSurvey('test_list_collector')

        self.get('/questionnaire/invalid/some-list-id/edit-person')

        self.assertInUrl('/questionnaire/list-collector')

    def test_invalid_list_item_id_on_add_block(self):
        self.launchSurvey('test_list_collector')

        self.get('/questionnaire/people/123/add-person')

        self.assertInUrl('/questionnaire/list-collector')

    def test_invalid_block(self):
        self.launchSurvey('test_list_collector')

        self.get('/questionnaire/bad-block')

        self.assertInUrl('list-collector')

    def test_invalid_list_item_id(self):
        self.launchSurvey('test_list_collector')

        self.get('/questionnaire/people/123/edit-person')

        self.assertInUrl('list-collector')

    def test_happy_path(self):
        self.launchSurvey('test_list_collector')

        self.assertInBody('Does anyone else live here?')

        self.post({'anyone-else': 'Yes'})

        self.add_person('Marie Claire', 'Doe')

        self.assertInSelector('Marie Claire Doe', 'tbody:nth-child(1) td:first-child')

        self.add_person('John', 'Doe')

        self.assertInSelector('John Doe', 'tbody:nth-child(2) td:first-child')

        self.add_person('A', 'Mistake')

        self.assertInSelector('A Mistake', 'tbody:nth-child(3) td:first-child')

        self.add_person('Johnny', 'Doe')

        self.assertInSelector('Johnny Doe', 'tbody:nth-child(4) td:first-child')

        # Make another mistake

        mistake_change_link = self.get_link('3', 'Change')

        self.get(mistake_change_link)

        self.post({'first-name': 'Another', 'last-name': 'Mistake'})

        self.assertInSelector('Another Mistake', 'tbody:nth-child(3) td:first-child')

        # Get rid of the mistake

        mistake_remove_link = self.get_link('3', 'Remove')

        self.get(mistake_remove_link)

        self.assertInBody('Are you sure you want to remove this person?')

        # Cancel

        self.post({'remove-confirmation': 'No'})

        self.assertEqualUrl('/questionnaire/list-collector/')

        # Remove again

        self.get(mistake_remove_link)

        self.post({'remove-confirmation': 'Yes'})

        # Make sure Johnny has moved up the list
        self.assertInSelector('Johnny Doe', 'tbody:nth-child(3) td:first-child')

        # Test the previous links
        john_change_link = self.get_link('2', 'Change')
        john_remove_link = self.get_link('2', 'Remove')

        self.get(john_change_link)

        self.get(self.get_previous_link())

        self.assertEqualUrl('/questionnaire/list-collector/')

        self.get(john_remove_link)

        self.assertInUrl('remove')

        self.get(self.get_previous_link())

        self.assertEqualUrl('/questionnaire/list-collector/')

    def test_list_collector_submission(self):
        self.launchSurvey('test_list_collector')

        self.post(action='start_questionnaire')

        self.assertInBody('Does anyone else live here?')

        self.post({'anyone-else': 'Yes'})

        self.add_person('Marie Claire', 'Doe')

        self.assertInSelector('Marie Claire Doe', 'tbody:nth-child(1) td:first-child')

        self.add_person('John', 'Doe')

        self.assertInSelector('John Doe', 'tbody:nth-child(2) td:first-child')

        self.post({'anyone-else': 'No'})

        self.post(action='save_continue')

        self.post({'another-anyone-else': 'No'})

        self.assertInBody('Check your answers before continuing')

        self.post()

        self.post()

        self.assertInUrl('thank-you')

    def test_optional_list_collector_submission(self):
        self.launchSurvey('test_list_collector')

        self.post(action='start_questionnaire')

        self.assertInBody('Does anyone else live here?')

        self.post({'anyone-else': 'No'})

        self.post(action='save_continue')

        self.post({'another-anyone-else': 'No'})

        self.assertInBody('Check your answers before continuing')

        self.post()

        self.post()

        self.assertInUrl('thank-you')
