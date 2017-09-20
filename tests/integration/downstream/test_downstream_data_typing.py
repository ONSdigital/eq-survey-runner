# coding: utf-8
import json

from jwcrypto import jwt
from mock import patch
from sdc.crypto.decrypter import decrypt
from sdc.crypto.helper import extract_kid_from_header

from app.secrets import KEY_PURPOSE_SUBMISSION
from tests.integration.star_wars import star_wars_test_urls, STAR_WARS_TRIVIA_PART_1_DEFAULT_ANSWERS
from tests.integration.star_wars.star_wars_tests import StarWarsTestCase


class TestDownstreamDataTyping(StarWarsTestCase):
    def setUp(self):
        self.patcher = patch('app.setup.LogSubmitter')
        mock_class = self.patcher.start()

        self.instance = mock_class.return_value
        self.instance.send_message.return_value = False

        super().setUp()
        self.launchSurvey('0', 'star_wars')

    def tearDown(self):
        self.patcher.stop()

    def test_star_wars_kitchen_sink(self):
        self.start_questionnaire_and_navigate_routing()

        # Form submission with no errors
        self.post(STAR_WARS_TRIVIA_PART_1_DEFAULT_ANSWERS)
        self.assertInPage("On <span class='date'>2 June 1983</span> how many were employed?")
        self.assertInPage('Why doesn\'t Chewbacca receive a medal at the end of A New Hope?')
        self.assertInPage('chewbacca-medal-answer')

        self.post({
            'chewbacca-medal-answer': 'Wookiees don’t place value in material rewards and refused the medal initially',
            'confirm-chewbacca-age-answer': 'Yes',
        })

        self.assertInPage('Finally, which  is your favourite film?')

        self.post({
            'jar-jar-binks-planet-answer': 'Naboo',
            'favourite-film-answer': '5',
        })

        self.assertRegexUrl(star_wars_test_urls.STAR_WARS_SUMMARY_REGEX)

        self.post(action=None)

        # Get the message that would be sent downstream
        signed_token = decrypt(self.instance.send_message.call_args[0][0], self._secret_store, KEY_PURPOSE_SUBMISSION) # pylint: disable=no-member
        message = decode_jwt(signed_token, self._secret_store)

        self.assertIn('data', message.keys())

        data = message['data']

        expected = {
            '20': 'Light Side',
            '23': 'Yes',
            '22': 'Millennium Falcon',
            '1': '234',
            '2': '40',
            '3': '1370',
            '4': 'Elephant',
            '5': 'Luke, I am your father',
            '6': ['Luke Skywalker', 'Yoda', 'Qui-Gon Jinn'],
            '81': '28/05/1983',
            '82': '29/05/1983',
            '10': 'Wookiees don’t place value in material rewards and refused the medal initially',
            '43': 'Yes'
        }

        for key, value in expected.items():
            self.assertIn(key, data.keys())
            self.assertEqual(expected[key], value)
            if isinstance(expected[key], list):
                for item in expected[key]:
                    self.assertIn(item, value)


def decode_jwt(jwt_token, secret_store):
    jwt_kid = extract_kid_from_header(jwt_token)

    public_key = secret_store.get_public_key_by_kid(KEY_PURPOSE_SUBMISSION, jwt_kid)

    signed_token = jwt.JWT(algs=['RS256'], check_claims={})

    signed_token.deserialize(jwt_token, key=public_key.as_jwk())

    return json.loads(signed_token.claims)
