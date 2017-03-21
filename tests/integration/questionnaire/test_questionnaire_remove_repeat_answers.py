from mock import patch, call

from tests.integration.integration_test_case import IntegrationTestCase


class TestQuestionnaireRemoveRepeatAnswers(IntegrationTestCase):

    def test_should_remove_household_composition_answer_when_no_answer(self):
        with patch('app.views.questionnaire.get_answer_store') as get_answer_store:
            # Given
            self.launchSurvey('census', 'household')

            # When
            self.post({'permanent-or-family-home-answer': 'No'})

            # Then
            get_answer_store().assert_has_calls([call.remove(block_id='household-composition', group_id='who-lives-here')])

    def test_should_not_remove_answers_when_yes_answer(self):
        with patch('app.views.questionnaire.get_answer_store') as get_answer_store:
            # Given
            self.launchSurvey('census', 'household')

            # When
            self.post({'permanent-or-family-home-answer': 'Yes'})

            # Then
            self.assertEqual(get_answer_store().remove.call_count, 0)

    def test_should_remove_all_repeating_groups(self):
        with patch('app.views.questionnaire.get_answer_store') as get_answer_store:
            # Given
            self.launchSurvey('census', 'household')

            # When
            self.post({'permanent-or-family-home-answer': 'No'})

            # Then
            get_answer_store().assert_has_calls([call.remove(group_id='who-lives-here-relationship'), call.remove(group_id='household-member')])
