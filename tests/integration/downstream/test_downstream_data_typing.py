# coding: utf-8
from mock import patch
from tests.integration.star_wars import star_wars_test_urls, STAR_WARS_TRIVIA_PART_1_DEFAULT_ANSWERS
from tests.integration.star_wars.star_wars_tests import StarWarsTestCase

from tests.app.submitter.test_encrypter import Decrypter

class TestDownstreamDataTyping(StarWarsTestCase):
    def setUp(self):
        self.patcher = patch('app.LogSubmitter')
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
        self.assertInPage('On 2 June 1983 how many were employed?')
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
        message = Decrypter().decrypt(self.instance.send_message.call_args[0][0])  # pylint: disable=no-member

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
