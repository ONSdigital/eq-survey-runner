from werkzeug.datastructures import MultiDict

from tests.integration.create_token import create_token
from tests.integration.downstream.downstream_test_case import DownstreamTestCase


class TestCensusHH2016OutputFormat(DownstreamTestCase):
    """
    This class tests the eQ application in a black box capacity by feeding
    inputs in and checking the output that would be sent to SDX.

    Specifically, it injects a new version of the submitter which captures the
    unencrypted message and interrogates it for the census hh 2016 survey.
    """

    def setUp(self):
        super().setUp()
        self.token = create_token('hh2016', '0')

    def get_first_page(self):
        resp = self.client.get('/session?token=' + self.token.decode(), follow_redirects=True)
        self.assertEquals(resp.status_code, 200)
        return resp

    def test_output_format(self):
        resp = self.get_first_page()

        # We are on the landing page
        content = resp.get_data(True)

        self.assertRegexpMatches(content, '<title>Introduction</title>')

        # We proceed to the questionnaire
        form_data = {
            'action[start_questionnaire]': 'Start Questionnaire'
        }
        resp = self.client.post('/questionnaire/0/hh2016/789/introduction', data=form_data, follow_redirects=False)
        self.assertEquals(resp.status_code, 302)

        block_one_url = resp.headers['Location']

        resp = self.client.get(block_one_url, follow_redirects=False)
        self.assertEquals(resp.status_code, 200)

        form_data = MultiDict({
            '6cf5c72a-c1bf-4d0c-af6c-d0f07bc5b65b': '4',  # agegroup
            '92e49d93-cbdc-4bcb-adb2-0e0af6c9a07c': '3',  # help1
            '92e49d94-cbdc-4bcb-adb2-0e0af6c9a07c': 'someone helped me',  # helpother
            'pre49d93-cbdc-4bcb-adb2-0e0af6c9a07c': '1',  # howcomplete
            'a5dc09e8-36f2-4bf4-97be-c9e6ca8cbe0d': ['1', '2', '5'],  # device
            'a5dc09e9-36f2-4bf4-97be-c9e6ca8cbe0d': 'Facebook Integration',  # deviceother
            '7587eb9b-f24e-4dc0-ac94-66118b896c10': ['5'],  # whypaper
            'a5dc09e9-36f2-4bf4-97be-c9e6ca8cbe1d': 'My computer crashed',  # paperother
            '9587eb9b-f24e-4dc0-ac94-66117b896c10': ['4', '8', '10'],  # help2
            'a5dc09e9-36f2-4bf4-97be-c9e6ca8cbe2d': 'Seek divine intervention',  # help2other
            '5587eb9b-f24e-4dc0-ac94-66117b896c10': 'Y',  # visit
            '5587eb9b-f24f-4dc0-ac94-66117b896c10': 'Y',  # find
            # user action
            'action[save_continue]': 'Save & Continue'
        })

        resp = self.client.post(block_one_url, data=form_data, follow_redirects=False)
        self.assertEquals(resp.status_code, 302)

        summary_url = resp.headers['Location']

        self.client.get(summary_url, follow_redirects=False)

        self.assertTrue(summary_url.endswith('summary'))

        form_data = {
            'action[submit_answers]': 'Submit Answers'
        }

        self.assertIsNone(TestCensusHH2016OutputFormat._submitter._message)

        resp = self.client.post('/questionnaire/0/hh2016/789/submit-answers', data=form_data, follow_redirects=False)
        self.assertEquals(resp.status_code, 302)

        self.assertIsNotNone(TestCensusHH2016OutputFormat._submitter._message)
        self.assertTrue(isinstance(TestCensusHH2016OutputFormat._submitter._message, dict))

        # Now check the data
        message = DownstreamTestCase._submitter._message

        self.assertIn('data', message.keys())
        self.assertIn('agegroup', message['data'].keys())
        self.assertEquals('4', message['data']['agegroup'])
        self.assertIn('help1', message['data'].keys())
        self.assertEquals('3', message['data']['help1'])
        self.assertIn('helpother', message['data'].keys())
        self.assertEquals('someone helped me', message['data']['helpother'])
        self.assertIn('howcomplete', message['data'].keys())
        self.assertEquals('1', message['data']['howcomplete'])
        self.assertIn('device', message['data'].keys())
        self.assertTrue(isinstance(message['data']['device'], list))
        self.assertEquals(3, len(message['data']['device']))
        self.assertIn('1', message['data']['device'])
        self.assertIn('2', message['data']['device'])
        self.assertIn('5', message['data']['device'])
        self.assertIn('deviceother', message['data'].keys())
        self.assertEquals('Facebook Integration', message['data']['deviceother'])
        self.assertIn('whypaper', message['data'].keys())
        self.assertTrue(isinstance(message['data']['whypaper'], list))
        self.assertEquals(1, len(message['data']['whypaper']))
        self.assertIn('5', message['data']['whypaper'])
        self.assertIn('paperother', message['data'].keys())
        self.assertEquals('My computer crashed', message['data']['paperother'])
        self.assertIn('help2', message['data'].keys())
        self.assertTrue(isinstance(message['data']['help2'], list))
        self.assertEquals(3, len(message['data']['help2']))
        self.assertIn('4', message['data']['help2'])
        self.assertIn('8', message['data']['help2'])
        self.assertIn('10', message['data']['help2'])
        self.assertIn('help2other', message['data'].keys())
        self.assertEquals('Seek divine intervention', message['data']['help2other'])
        self.assertIn('visit', message['data'].keys())
        self.assertEquals('Y', message['data']['visit'])
        self.assertIn('find', message['data'].keys())
        self.assertEquals('Y', message['data']['find'])
