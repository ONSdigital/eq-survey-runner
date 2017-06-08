from tests.integration.integration_test_case import IntegrationTestCase


class TestLogin(IntegrationTestCase):

    def test_login_with_no_token_should_be_unauthorized(self):
        # Given
        token = ""

        # When
        self.get('/session?token=' + token)

        # Then
        self.assertStatusUnauthorised()

    def test_login_with_invalid_token_should_be_forbidden(self):
        # Given
        token = "123"

        # When
        self.get('/session?token=' + token)

        # Then
        self.assertStatusForbidden()

    def test_login_with_valid_token_should_redirect_to_survey(self):
        # Given
        token = self.token_generator.create_token('0205', '1')

        # When
        self.get('/session?token=' + token.decode())

        # Then
        self.assertStatusOK()
        self.assertInUrl('/questionnaire/1/0205')

    def test_login_with_token_twice_is_unauthorised_when_same_jti_provided(self):
        # Given
        token = self.token_generator.create_token('0205', '1')
        self.get('/session?token=' + token.decode())

        # When
        self.get('/session?token=' + token.decode())

        # Then
        self.assertStatusUnauthorised()

    def test_login_with_token_twice_is_authorised_when_no_jti(self):
        # Given
        token = self.token_generator.create_token('0205', '1', jti=None)
        self.get('/session?token=' + token.decode())

        # When
        self.get('/session?token=' + token.decode())

        # Then
        self.assertStatusOK()
        self.assertInUrl('/questionnaire/1/0205')

    def test_login_with_valid_token_no_eq_id_and_form_type(self):
        # Given
        token = self.token_generator.create_token('', '')

        # When
        self.get('/session?token=' + token.decode())

        # Then
        self.assertStatusNotFound()


    def test_http_head_request_to_login_returns_successfully_and_get_still_works(self):
        # Given
        token = self.token_generator.create_token('0205', '1')

        # When
        self._client.head('/session?token=' + token.decode(), as_tuple=True, follow_redirects=True)
        self.get('/session?token=' + token.decode())

        # Then
        self.assertStatusOK()
        self.assertInUrl('/questionnaire/1/0205')
