import json
from jsonschema import SchemaError, ValidationError, validate
from mock import patch
from tests.integration.integration_test_case import IntegrationTestCase
from jwcrypto import jwt
from app.cryptography.token_helper import decrypt_jwe, extract_kid_from_header
from app.secrets import KEY_PURPOSE_SUBMISSION
from structlog import getLogger


logger = getLogger()

FEEDBACK_FORM_URL = '/feedback'
FEEDBACK_THANKYOU_URL = '/feedback/thank-you'

class Feedback(IntegrationTestCase):
    def setUp(self):
        self.patcher = patch('app.setup.LogSubmitter')
        mock_class = self.patcher.start()

        self.instance = mock_class.return_value
        self.instance.send_message.return_value = True

        super().setUp()
        self.launchSurvey('test', 'textfield')


    def tearDown(self):
        self.patcher.stop()


    def test_correct_feeback_link_in_page(self):
        soup = self.getHtmlSoup()
        links = soup.find_all('a')
        feedbackLinks = [link['href'] for link in links if FEEDBACK_FORM_URL in link['href']]
        self.assertGreaterEqual(len(feedbackLinks), 1)


    def test_get_feedback_page(self):
        self.get(FEEDBACK_FORM_URL)
        self.assertStatusOK()
        self.assertEqualUrl(FEEDBACK_FORM_URL)


    def test_feedback_empty_post_redirects_to_thankyou(self):
        self.post(url=FEEDBACK_FORM_URL, post_data='', action='send_feedback')
        self.assertStatusOK()
        self.assertEqualUrl(FEEDBACK_THANKYOU_URL)


    def test_post_with_empty_message_does_not_send_message(self):
        post_data = {
            'message': '',
            'name': 'Bill',
            'email': 'Bill@email.com'
        }

        self.post(url=FEEDBACK_FORM_URL, post_data=post_data, action='send_feedback')
        self.assertStatusOK()

        self.assertEqual(self.instance.send_message.call_count, 0)  # pylint: disable=no-member


    def test_post_sends_message(self):
        post_data = {
            'message': 'This survey is awesome',
            'name': 'Bill',
            'email': 'Bill@email.com'
        }

        referer = 'https://some.url'
        message = self.post_then_intercept_and_decrypt_message(
            post_data,
            headers={'Referer': referer}
        )

        self.assertStatusOK()

        expected_message = post_data
        expected_message['url'] = referer
        self.assertEqual(message['data'], expected_message)


    def test_post_csrf_failure_returns_bad_args(self):
        self.last_csrf_token = None
        post_data = {
            'message': 'This survey is awesome',
            'name': 'Bill',
            'email': 'Bill@email.com'
        }

        self.post(url='/feedback', post_data=post_data, action='send_feedback')
        self.assertStatusCode(400)


    def test_post_html_encodes_user_input(self):
        post_data = {
            'message': '&<>\'"',
            'name': '&<>\'"',
            'email': '&<>\'"'
        }

        data = self.post_then_intercept_and_decrypt_message(post_data)['data']
        expected = '&amp;&lt;&gt;&#39;&#34;'

        self.assertEqual(data['message'], expected)
        self.assertEqual(data['name'], expected)
        self.assertEqual(data['email'], expected)


    def test_post_sends_valid_message(self):
        post_data = {
            "message": "This survey is awesome",
            "name": "Bill",
            "email": "Bill@email.com",
        }

        message = self.post_then_intercept_and_decrypt_message(post_data)

        with open("data/schema/feedback_v1.json") as schema_file:
            schema = json.load(schema_file)

        errors = validate_json_with_schema(message, schema)

        if errors:
            for error in errors:
                logger.error(error)

            self.fail("{} Schema Validation Errors.\n{}".format(len(errors), errors))


    def test_post_with_broken_send_message_returns_503(self):
        post_data = {
            "message": "This survey is awesome",
            "name": "Bill",
            "email": "Bill@email.com"
        }

        self.instance.send_message.return_value = False  # pylint: disable=no-member

        self.post(url=FEEDBACK_FORM_URL, post_data=post_data, action='send_feedback')
        self.assertStatusCode(503)


    def post_then_intercept_and_decrypt_message(self, post_data, **kwargs):
        self.post(url=FEEDBACK_FORM_URL, post_data=post_data, action='send_feedback', **kwargs)

        signed_token = decrypt_jwe(self.instance.send_message.call_args[0][0], self._secret_store, KEY_PURPOSE_SUBMISSION) # pylint: disable=no-member
        return decode_jwt(signed_token, self._secret_store)


def validate_json_with_schema(data, schema):
    errors = []

    try:
        validate(data, schema)

    except ValidationError as e:
        errors.append("Schema Validation Error! message [{}] does not validate against schema. Error [{}]".format(data, e))

    except SchemaError as e:
        errors.append("JSON Parse Error! Could not parse [{}]. Error [{}]".format(data, e))

    return errors


def decode_jwt(jwt_token, secret_store):
    jwt_kid = extract_kid_from_header(jwt_token)

    public_key = secret_store.get_public_key_by_kid(KEY_PURPOSE_SUBMISSION, jwt_kid)

    signed_token = jwt.JWT(algs=['RS256'], check_claims={})

    signed_token.deserialize(jwt_token, key=public_key.as_jwk())

    return json.loads(signed_token.claims)
