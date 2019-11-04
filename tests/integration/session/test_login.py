import time

from httmock import urlmatch, HTTMock, response

from app.utilities.schema import get_schema_file_path
from tests.integration.create_token import PAYLOAD
from tests.integration.integration_test_case import IntegrationTestCase


class TestLoginWithGetRequest(IntegrationTestCase):
    def test_login_with_no_token_should_be_unauthorized(self):
        # Given
        token = ''

        # When
        self.get(url=f'/session?token={token}')

        # Then
        self.assertStatusUnauthorised()

    def test_login_with_invalid_token_should_be_forbidden(self):
        # Given
        token = '123'

        # When
        self.get(url=f'/session?token={token}')

        # Then
        self.assertStatusForbidden()

    def test_login_with_valid_token_should_redirect_to_survey(self):
        # Given
        token = self.token_generator.create_token('test_checkbox')

        # When
        self.get(url=f'/session?token={token}')

        # Then
        self.assertStatusOK()
        self.assertInUrl('/questionnaire')

    def test_login_with_token_twice_is_unauthorised_when_same_jti_provided(self):
        # Given
        token = self.token_generator.create_token('test_checkbox')
        self.get(url=f'/session?token={token}')

        # When
        self.get(url=f'/session?token={token}')

        # Then
        self.assertStatusUnauthorised()

    def test_login_without_jti_in_token_is_unauthorised(self):
        # Given
        token = self.token_generator.create_token_without_jti('test_checkbox')
        self.get(url=f'/session?token={token}')

        # Then
        self.assertStatusForbidden()

    def test_login_with_valid_token_no_schema_name(self):
        # Given
        token = self.token_generator.create_token('')

        # When
        self.get(url=f'/session?token={token}')

        # Then
        self.assertStatusForbidden()

    def test_http_head_request_to_login_returns_successfully_and_get_still_works(self):
        # Given
        token = self.token_generator.create_token('test_checkbox')

        # When
        self._client.head(
            '/session?token=' + token, as_tuple=True, follow_redirects=True
        )
        self.get(url=f'/session?token={token}')

        # Then
        self.assertStatusOK()
        self.assertInUrl('/questionnaire')

    def test_login_with_missing_mandatory_claims_should_be_forbidden(self):
        # Given
        payload_vars = PAYLOAD.copy()
        payload_vars['iat'] = time.time()
        payload_vars['exp'] = payload_vars['iat'] + float(3600)  # one hour from now

        token = self.token_generator.generate_token(payload_vars)

        # When
        self.get(url=f'/session?token={token}')

        # Then
        self.assertStatusForbidden()

    def test_login_with_invalid_questionnaire_claims_should_be_forbidden(self):
        # flag_1 should be a boolean
        token = self.token_generator.create_token('test_metadata_routing', flag_1=123)

        self.get(url=f'/session?token={token}')

        self.assertStatusForbidden()

    def test_login_token_with_survey_url_should_redirect_to_survey(self):

        survey_url = 'http://eq-survey-register.url/my-test-schema'

        # Given
        token = self.token_generator.create_token_with_survey_url(
            'test_textarea', survey_url
        )

        # When
        with HTTMock(self.survey_url_mock):
            self.get(url=f'/session?token={token}')

        self.assertStatusOK()
        self.assertInUrl('/questionnaire')

    def test_login_token_with_incorrect_survey_url_results_in_404(self):

        survey_url = 'http://eq-survey-register.url/my-test-schema-not-found'

        # Given
        token = self.token_generator.create_token_with_survey_url(
            'test_textarea', survey_url
        )

        # When
        with HTTMock(self.survey_url_mock_404):
            self.get(url=f'/session?token={token}')

        # Then
        self.assertStatusNotFound()

    def test_login_without_case_id_in_token_is_authorised(self):
        # Given
        token = self.token_generator.create_token_without_case_id('test_textfield')
        self.get(url=f'/session?token={token}')

        # Then
        self.assertStatusOK()

    def test_login_without_questionnaire_id_in_token_is_unauthorised(self):
        # Given
        token = self.token_generator.create_token_without_questionnaire_id(
            'textfield_test'
        )
        self.get(url=f'/session?token={token}')

        # Then
        self.assertStatusForbidden()

    @staticmethod
    @urlmatch(netloc=r'eq-survey-register', path=r'\/my-test-schema')
    def survey_url_mock(_url, _request):
        schema_path = get_schema_file_path('test_textarea', language_code='en')

        with open(schema_path, encoding='utf8') as json_data:
            return json_data.read()

    @staticmethod
    @urlmatch(netloc=r'eq-survey-register', path=r'\/my-test-schema-not-found')
    def survey_url_mock_404(_url, _request):
        return response(404)


class TestLoginWIthPostRequest(IntegrationTestCase):
    def test_login_with_no_token_should_be_unauthorized(self):
        # Given
        token = ''

        # When
        self.post(url=f'/session?token={token}')

        # Then
        self.assertStatusUnauthorised()

    def test_login_with_invalid_token_should_be_forbidden(self):
        # Given
        token = '123'

        # When
        self.post(url=f'/session?token={token}')

        # Then
        self.assertStatusForbidden()

    def test_login_with_valid_token_should_redirect_to_survey(self):
        # Given
        token = self.token_generator.create_token('test_checkbox')

        # When
        self.post(url=f'/session?token={token}')

        # Then
        self.assertStatusOK()
        self.assertInUrl('/questionnaire')

    def test_login_with_token_twice_is_unauthorised_when_same_jti_provided(self):
        # Given
        token = self.token_generator.create_token('test_checkbox')
        self.post(url=f'/session?token={token}')

        # When
        self.post(url=f'/session?token={token}')

        # Then
        self.assertStatusUnauthorised()

    def test_login_without_jti_in_token_is_unauthorised(self):
        # Given
        token = self.token_generator.create_token_without_jti('test_checkbox')
        self.post(url=f'/session?token={token}')

        # Then
        self.assertStatusForbidden()

    def test_login_with_valid_token_no_schema_name(self):
        # Given
        token = self.token_generator.create_token('')

        # When
        self.post(url=f'/session?token={token}')

        # Then
        self.assertStatusForbidden()

    def test_http_head_request_to_login_returns_successfully_and_post_still_works(self):
        # Given
        token = self.token_generator.create_token('test_checkbox')

        # When
        self._client.head(
            '/session?token=' + token, as_tuple=True, follow_redirects=True
        )
        self.post(url=f'/session?token={token}')

        # Then
        self.assertStatusOK()
        self.assertInUrl('/questionnaire')

    def test_login_with_missing_mandatory_claims_should_be_forbidden(self):
        # Given
        payload_vars = PAYLOAD.copy()
        payload_vars['iat'] = time.time()
        payload_vars['exp'] = payload_vars['iat'] + float(3600)  # one hour from now

        token = self.token_generator.generate_token(payload_vars)

        # When
        self.post(url=f'/session?token={token}')

        # Then
        self.assertStatusForbidden()

    def test_login_with_invalid_questionnaire_claims_should_be_forbidden(self):
        # flag_1 should be a boolean
        token = self.token_generator.create_token('test_metadata_routing', flag_1=123)

        self.post(url=f'/session?token={token}')

        self.assertStatusForbidden()

    def test_login_token_with_survey_url_should_redirect_to_survey(self):

        survey_url = 'http://eq-survey-register.url/my-test-schema'

        # Given
        token = self.token_generator.create_token_with_survey_url(
            'test_textarea', survey_url
        )

        # When
        with HTTMock(self.survey_url_mock):
            self.post(url=f'/session?token={token}')

        self.assertStatusOK()
        self.assertInUrl('/questionnaire')

    def test_login_token_with_incorrect_survey_url_results_in_404(self):

        survey_url = 'http://eq-survey-register.url/my-test-schema-not-found'

        # Given
        token = self.token_generator.create_token_with_survey_url(
            'test_textarea', survey_url
        )

        # When
        with HTTMock(self.survey_url_mock_404):
            self.post(url=f'/session?token={token}')

        # Then
        self.assertStatusNotFound()

    def test_login_without_case_id_in_token_is_authorised(self):
        # Given
        token = self.token_generator.create_token_without_case_id('test_textfield')
        self.post(url=f'/session?token={token}')

        # Then
        self.assertStatusOK()

    def test_login_without_questionnaire_id_in_token_is_unauthorised(self):
        # Given
        token = self.token_generator.create_token_without_questionnaire_id(
            'textfield_test'
        )
        self.post(url=f'/session?token={token}')

        # Then
        self.assertStatusForbidden()

    @staticmethod
    @urlmatch(netloc=r'eq-survey-register', path=r'\/my-test-schema')
    def survey_url_mock(_url, _request):
        schema_path = get_schema_file_path('test_textarea', language_code='en')

        with open(schema_path, encoding='utf8') as json_data:
            return json_data.read()

    @staticmethod
    @urlmatch(netloc=r'eq-survey-register', path=r'\/my-test-schema-not-found')
    def survey_url_mock_404(_url, _request):
        return response(404)
