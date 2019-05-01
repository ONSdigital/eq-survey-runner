import simplejson as json
import snappy

from jwcrypto import jwe
from mock import patch
from tests.integration.integration_test_case import IntegrationTestCase

from app.storage.storage_encryption import StorageEncryption


class TestViewSubmission(IntegrationTestCase):

    def setUp(self):
        super().setUp()

        self.launchSurvey('test', 'view_submitted_response')

        form_data = {
            'radio-answer': 'Bacon',
        }
        self.post(form_data)

        form_data = {
            'test-currency': '12',
            'square-kilometres': '345',
            'test-decimal': '67.89',
        }
        self.post(form_data)

        # Submit answers
        self.post(action=None)

    def test_view_submission(self):

        # check we're on the thank you page and view submission link is available
        self.assertInUrl('thank-you')
        self.assertInBody('View and print a copy of your answers')

        # go to the view submission page
        self.get('submitted/view-submission')

        # check we're on the view submission page
        self.assertInUrl('view-submission')
        self.assertInBody('Submitted answers')

        # check answers are on page
        self.assertStatusOK()
        self.assertInBody('Bacon')
        self.assertInBody('12')
        self.assertInBody('345')
        self.assertInBody('67.89')

        # check edit links are not on page
        self.assertNotInBody('data-ga-action="Edit click"')

    def test_view_submission_sign_out(self):
        self.get('submitted/view-submission')

        self.post(action='sign_out')
        self.assertEqualUrl('/signed-out')

    def test_view_submission_post_no_action(self):
        self.get('submitted/view-submission')

        self.post(action=None)
        self.assertInUrl('view-submission')


class TestCantViewSubmission(IntegrationTestCase):

    def test_try_view_submission_when_not_available(self):
        self.launchSurvey('test', 'currency')

        # check we're on first page
        self.assertInBody('Currency Input Test')

        # We fill in our answers
        form_data = {
            # Food choice
            'answer': '12',
            'answer-usd': '345',
            'answer-eur': '67.89',
            'answer-jpy': '0',
        }

        # We submit the form
        self.post(form_data)

        # There are no validation errors
        self.assertInUrl('summary')

        # Submit answers
        self.post(action=None)

        # check we're on the thank you page and view submission link is not available
        self.assertInUrl('thank-you')
        self.assertNotInBody('View and print a copy of your answers')

        # try go to the view submission page anyway
        self.get('submitted/view-submission')

        # check we're redirected back to thank you page
        self.assertInUrl('thank-you')

    def test_try_view_submission_early(self):
        self.launchSurvey('test', 'view_submitted_response')

        # check we're on first page
        self.assertInBody('What is your favourite breakfast food')

        # try to get the view-submission page
        self.get('submitted/view-submission')

        # check we're redirected back to first page
        self.assertInBody('What is your favourite breakfast food')


class TestViewSubmissionTradingAs(IntegrationTestCase):

    def test_view_submission_shows_trading_as_if_present(self):
        self.launchSurvey('test', 'view_submitted_response')

        # check we're on first page
        self.assertInBody('What is your favourite breakfast food')

        # We fill in our answer
        form_data = {
            # Food choice
            'radio-answer': 'Bacon',
        }

        # We submit the form
        self.post(form_data)

        # check we're on second page
        self.assertInBody('Please enter test values (none mandatory)')

        # We fill in our answers
        form_data = {
            # Food choice
            'test-currency': '12',
            'square-kilometres': '345',
            'test-decimal': '67.89',
        }

        # We submit the form
        self.post(form_data)

        # Submit answers
        self.post(action=None)

        # go to the view submission page
        self.get('submitted/view-submission')

        # check we're on the view submission page, and trading as value is displayed
        self.assertInUrl('view-submission')
        self.assertInBody('(Integration Tests)')

    def test_view_submission_does_not_show_parenthesis_if_no_trading_as(self):
        no_trading_as_payload = {
            'user_id': 'integration-test',
            'period_str': 'April 2016',
            'period_id': '201604',
            'collection_exercise_sid': '789',
            'ru_ref': '123456789012A',
            'ru_name': 'Integration Testing',
            'ref_p_start_date': '2016-04-01',
            'ref_p_end_date': '2016-04-30',
            'return_by': '2016-05-06',
            'employment_date': '1983-06-02',
            'region_code': 'GB-ENG',
            'language_code': 'en',
            'roles': []
        }
        with patch('tests.integration.create_token.PAYLOAD', no_trading_as_payload):
            self.launchSurvey('test', 'view_submitted_response')

            # check we're on first page
            self.assertInBody('What is your favourite breakfast food')

            # We fill in our answer
            form_data = {
                # Food choice
                'radio-answer': 'Bacon',
            }

            # We submit the form
            self.post(form_data)

            # check we're on second page
            self.assertInBody('Please enter test values (none mandatory)')

            # We fill in our answers
            form_data = {
                # Food choice
                'test-currency': '12',
                'square-kilometres': '345',
                'test-decimal': '67.89',
            }

            # We submit the form
            self.post(form_data)

            # Submit answers
            self.post(action=None)

            # go to the view submission page
            self.get('submitted/view-submission')

            # check we're on the view submission page, and trading as value is displayed
            self.assertInUrl('view-submission')
            self.assertNotInBody('(Integration Tests)')
            self.assertNotInBody('()')

    def test_view_submission_does_not_show_parenthesis_trading_as_is_empty_string(self):
        no_trading_as_payload = {
            'user_id': 'integration-test',
            'period_str': 'April 2016',
            'period_id': '201604',
            'collection_exercise_sid': '789',
            'ru_ref': '123456789012A',
            'ru_name': 'Integration Testing',
            'ref_p_start_date': '2016-04-01',
            'ref_p_end_date': '2016-04-30',
            'return_by': '2016-05-06',
            'employment_date': '1983-06-02',
            'region_code': 'GB-ENG',
            'language_code': 'en',
            'roles': [],
            'trad_as': ''
        }
        with patch('tests.integration.create_token.PAYLOAD', no_trading_as_payload):
            self.launchSurvey('test', 'view_submitted_response')

            # check we're on first page
            self.assertInBody('What is your favourite breakfast food')

            # We fill in our answer
            form_data = {
                # Food choice
                'radio-answer': 'Bacon',
            }

            # We submit the form
            self.post(form_data)

            # check we're on second page
            self.assertInBody('Please enter test values (none mandatory)')

            # We fill in our answers
            form_data = {
                # Food choice
                'test-currency': '12',
                'square-kilometres': '345',
                'test-decimal': '67.89',
            }

            # We submit the form
            self.post(form_data)

            # Submit answers
            self.post(action=None)

            # go to the view submission page
            self.get('submitted/view-submission')

            # check we're on the view submission page, and trading as value is displayed
            self.assertInUrl('view-submission')
            self.assertNotInBody('(Integration Tests)')
            self.assertNotInBody('()')


class TestViewSubmissionCompression(IntegrationTestCase):

    def test_compressed_submitted_response_data(self):
        """Compressed storage will be introduced in the next release
        """
        # setup
        with patch(
                'app.views.questionnaire.StorageEncryption',
                wraps=_CompressedStorageEncryption):
            self.launchSurvey('test', 'view_submitted_response')

            form_data = {
                'radio-answer': 'Bacon',
            }
            self.post(form_data)

            form_data = {
                'test-currency': '12',
                'square-kilometres': '345',
                'test-decimal': '67.89',
            }
            self.post(form_data)

            self.post(action=None)

            # go to the view submission page
            self.get('submitted/view-submission')

            # check we're on the view submission page
            self.assertInUrl('view-submission')
            self.assertInBody('Submitted answers')
            self.assertStatusOK()


class _CompressedStorageEncryption(StorageEncryption):

    def encrypt_data(self, data):
        if isinstance(data, dict):
            data = json.dumps(data, for_json=True)

        protected_header = {
            'alg': 'dir',
            'enc': 'A256GCM',
            'kid': '1,1',
        }

        data = snappy.compress(data)

        jwe_token = jwe.JWE(
            plaintext=data,
            protected=protected_header,
            recipient=self.key,
        )

        return jwe_token.serialize(compact=True)

    def decrypt_data(self, encrypted_token):
        payload = super().decrypt_data(encrypted_token)
        return snappy.uncompress(payload)
