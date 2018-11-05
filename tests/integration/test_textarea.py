import json
from tests.integration.integration_test_case import IntegrationTestCase

with open('tests/fixtures/blns.json') as blns:
    NAUGHTY_STRINGS = json.load(blns)


class TestTextArea(IntegrationTestCase):

    def test_empty_submission(self):
        self.launchSurvey('test', 'textarea')
        self.post(action='save_continue')

        self.assertInBody('No answer provided')

        self.post(action=None)
        self.assertInUrl('thank-you')

    def test_too_many_characters(self):
        self.launchSurvey('test', 'textarea')
        self.post({'answer': 'This is longer than twenty characters'})

        self.assertInBody('Your answer has to be less than 20 characters')

    def test_acceptable_submission(self):
        self.launchSurvey('test', 'textarea')
        self.post({'answer': 'Less than 20 chars'})

        self.assertInBody('Less than 20 chars')

        self.post(action=None)
        self.assertInUrl('thank-you')

    def test_big_list_of_naughty_strings(self):
        self.launchSurvey('test', 'big_list_naughty_strings')

        answers = {}
        for counter, value in enumerate(NAUGHTY_STRINGS):
            key = 'answer{}'.format(counter)
            answers[key] = value

        self.post(answers)
        self.assertInUrl('summary')
        self.assertEqual(200, self.last_response.status_code)
