from app.validation.error_messages import error_messages
from tests.integration.integration_test_case import IntegrationTestCase


class TestSaveSignOut(IntegrationTestCase):

    def test_save_sign_out_with_mandatory_question_not_answered(self):
        # We can save and go to the sign-out page without having to fill in mandatory answer

        # Given
        self.launchSurvey('test', 'radio_mandatory', account_service_url='https://localhost/my-account', account_service_log_out_url='https://localhost/logout')

        # When
        self.post(action='save_sign_out')

        # Then we are presented with the sign out page
        self.assertInUrl('/logout')

    def test_save_sign_out_with_non_mandatory_validation_error(self):
        # We can't save if a validation error is caused, this doesn't include missing a mandatory question

        # Given
        self.launchSurvey('test', 'error_messages')

        # When
        self.post(post_data={'test-number': 'error'}, action='save_sign_out')

        # Then we are presented with an error message
        self.assertRegexPage(error_messages['INVALID_NUMBER'])

    def test_save_sign_out_complete_a_block_then_revisit_it(self):
        # If a user completes a block, but then goes back and uses save and come back on that block, that block
        # should no longer be considered complete and on re-authenticate it should return to it

        self.launchSurvey('test', 'textfield')

        block_one_url = self.last_url

        post_data = {
            'name-answer': 'Joe Bloggs'
        }

        self.post(post_data)

        # We go back to the first page and save and complete later
        self.get(block_one_url)
        self.post(action='save_sign_out')

        # We re-authenticate and check we are on the first page
        self.launchSurvey('test', 'textfield')
        self.assertEqual(block_one_url, self.last_url)

    def test_sign_out_on_introduction_page(self):

        # Given
        self.launchSurvey('test', 'introduction', account_service_url='https://localhost/my-account', account_service_log_out_url='https://localhost/logout')

        # When
        self.post(action='sign_out')

        # Then we are presented with the sign out page
        self.assertInUrl('/logout')

    def test_thank_you_without_logout_url(self):
        """
        If the signed-out url is hit but there is no account_service_log_out_url, then a sign out page is rendered.
        """
        self.launchSurvey('test', 'textarea')
        self.post({'answer': 'This is an answer'})
        token = self.last_csrf_token

        self.post(action=None)
        self.assertInUrl('thank-you')

        self.last_csrf_token = token
        self.post(action='sign_out')
        self.assertInUrl('/signed-out')
        self.assertInBody('Your survey answers have been saved. You are now signed out')

    def test_thank_you_page_post_without_action(self):
        """
        If the thank you page is posted to without an action,
        it takes you back to the thank you page.
        """

        self.launchSurvey('test', 'textarea')
        self.post({'answer': 'This is an answer'})
        token = self.last_csrf_token

        self.post(action=None)
        self.assertInUrl('thank-you')

        self.last_csrf_token = token
        self.post(action=None)
        self.assertInUrl('/thank-you')
