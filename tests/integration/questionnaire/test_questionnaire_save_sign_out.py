from tests.integration.integration_test_case import IntegrationTestCase


class TestSaveSignOut(IntegrationTestCase):

    def test_save_sign_out_with_mandatory_question_not_answered(self):
        # We can save and go to the sign-out page without having to fill in mandatory answer

        # Given
        self.launchSurvey('1', '0205')

        # When
        self.post(action='start_questionnaire')
        self.post(post_data={'total-retail-turnover': '1000'}, action='save_sign_out')

        # Then we are presented with the sign out page
        self.assertStatusOK()
        self.assertInUrl("signed-out")

    def test_save_sign_out_with_non_mandatory_validation_error(self):
        # We can't save if a validation error is caused, this doesn't include missing a mandatory question

        # Given
        self.launchSurvey('1', '0205')

        # When
        self.post(action='start_questionnaire')
        self.post(post_data={'total-retail-turnover': 'error'}, action='save_sign_out')

        # Then we are presented with an error message
        self.assertRegexPage('Please only enter whole numbers into the field.')

    def test_save_sign_out_complete_a_block_then_revisit_it(self):
        # If a user completes a block, but then goes back and uses save and come back on that block, that block
        # should no longer be considered complete and on re-authenticate it should return to it

        self.launchSurvey('1', '0102')

        self.post(action='start_questionnaire')
        block_one_url = self.last_url

        post_data = {
            'period-from-day': '01',
            'period-from-month': '4',
            'period-from-year': '2016',
            'period-to-day': '30',
            'period-to-month': '4',
            'period-to-year': '2016'
        }

        self.post(post_data)

        # We go back to the first page and save and complete later
        self.get(block_one_url)
        self.post(action='save_sign_out')

        # We re-authenticate and check we are on the first page
        self.launchSurvey('1', '0102')
        self.assertEqual(block_one_url, self.last_url)
