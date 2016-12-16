from mock import patch, call

from tests.integration.create_token import create_token
from tests.integration.integration_test_case import IntegrationTestCase


class TestQuestionnaireRemoveAnswersAfterRoutingBack(IntegrationTestCase):

    def test_should_remove_answer_after_changing_household_composition(self):
        with patch('app.main.views.questionnaire.get_answer_store') as get_answer_store:
            # Given
            self.token = create_token('household', 'census')
            self.client.get('/session?token=' + self.token.decode(), follow_redirects=True)

            answer = {
                'permanent-or-family-home-answer': 'Yes',
            }
            self.client.post('/questionnaire/census/household/789/who-lives-here/0/permanent-or-family-home',
                             data=answer)

            answer = {
                'first-name': 'Person',
                'middle-names': '',
                'last-name': 'One',
                'action[save_continue]': '',
            }
            self.client.post('/questionnaire/census/household/789/who-lives-here/0/household-composition',
                             data=answer)

            # When
            answer = {
                'everyone-at-address-confirmation-answer': 'No, I need to add another person',
            }
            self.client.post('/questionnaire/census/household/789/who-lives-here/0/everyone-at-address-confirmation',
                             data=answer)

            answer = {
                'first-name': 'Person',
                'middle-names': '',
                'last-name': 'One',
                'action[add_answer]': '',
            }
            self.client.post('/questionnaire/census/household/789/who-lives-here/0/household-composition',
                             data=answer)

            answer = {
                'first-name': 'Person',
                'middle-names': '',
                'last-name': 'One',
                'first-name_1': 'Person',
                'middle-names_1': '',
                'last-name_1': 'Two',
                'action[save_continue]': '',
            }
            self.client.post('/questionnaire/census/household/789/who-lives-here/0/household-composition',
                             data=answer)

            # Then
            get_answer_store().assert_has_calls([call.remove(answer_id='everyone-at-address-confirmation')])
