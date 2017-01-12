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

    def start_new_survey(self):
        token = create_token('0203', '1')
        resp = self.client.get('/session?token=' + token.decode(), follow_redirects=True)
        self.assertEquals(resp.status_code, 200)
        return resp


