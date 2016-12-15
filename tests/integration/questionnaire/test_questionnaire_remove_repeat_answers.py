from mock import patch, call

from tests.integration.create_token import create_token
from tests.integration.integration_test_case import IntegrationTestCase


class TestQuestionnaireRemoveRepeatAnswers(IntegrationTestCase):

    def test_should_remove_household_composition_answer_when_no_answer(self):
        with patch('app.main.views.questionnaire.get_answer_store') as get_answer_store:
            # Given
            self.token = create_token('household', 'census')
            self.client.get('/session?token=' + self.token.decode(), follow_redirects=True)
            answer = {'permanent-or-family-home-answer': 'No'}

            # When
            self.client.post('/questionnaire/census/household/789/who-lives-here/0/permanent-or-family-home', data=answer)

            # Then
            get_answer_store().assert_has_calls([call.remove(block_id='household-composition', group_id='who-lives-here')])

    def test_should_not_remove_answers_when_yes_answer(self):
        with patch('app.main.views.questionnaire.get_answer_store') as get_answer_store:
            # Given
            self.token = create_token('household', 'census')
            self.client.get('/session?token=' + self.token.decode(), follow_redirects=True)
            answer = {'permanent-or-family-home-answer': 'Yes'}

            # When
            self.client.post('/questionnaire/census/household/789/who-lives-here/0/permanent-or-family-home', data=answer)

            # Then
            assert get_answer_store().remove.call_count == 0

    def test_should_remove_all_repeating_groups(self):
        with patch('app.main.views.questionnaire.get_answer_store') as get_answer_store:
            # Given
            self.token = create_token('household', 'census')
            self.client.get('/session?token=' + self.token.decode(), follow_redirects=True)
            answer = {'permanent-or-family-home-answer': 'No'}

            # When
            self.client.post('/questionnaire/census/household/789/who-lives-here/0/permanent-or-family-home', data=answer)

            # Then
            get_answer_store().assert_has_calls([call.remove(group_id='who-lives-here-relationship'), call.remove(group_id='household-member')])
