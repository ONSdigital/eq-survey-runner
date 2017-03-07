from tests.integration.integration_test_case import IntegrationTestCase
from tests.integration.create_token import create_token


class TestIntroduction(IntegrationTestCase):

    def test_mail_link_contains_ru_ref_in_subject(self):
        # Given
        response = self.start_new_survey()

        # When
        content = response.get_data(True)

        # Then
        self.assertRegex(content, '\"mailto\:.+\?subject\=.+123456789012A\"')

    def start_new_survey(self, survey_id='0203', eq_id='1'):
        token = create_token(survey_id, eq_id)
        resp = self.client.get('/session?token=' + token.decode(), follow_redirects=True)
        self.assertEquals(resp.status_code, 200)
        return resp

    def test_intro_description_displayed(self):
        # Given survey containing intro description
        response = self.start_new_survey('0112')

        # When on the introduction page
        content = response.get_data(True)

        # Then description should be displayed
        self.assertIn('qa-intro-description', content)

    def test_intro_description_not_displayed(self):
        # Given survey without introduction description
        response = self.start_new_survey('textfield', 'test')

        # When on the introduction page
        content = response.get_data(True)

        # Then description should not be displayed
        self.assertNotIn('qa-intro-description', content)

    def test_intro_basis_for_completion_displayed(self):
        # Given survey with basis for completion
        response = self.start_new_survey('0001', '2')

        # When on the introduction page
        content = response.get_data(True)

        # Then basis for completion should be displayed
        self.assertIn('basis-for-completion', content)

    def test_intro_basis_for_completion_not_displayed(self):

        # Given survey without basis for completion
        response = self.start_new_survey('0112')

        # When on the introduction page
        content = response.get_data(True)

        # Then basis for completion should not be displayed
        self.assertNotIn('basis-for-completion', content)
