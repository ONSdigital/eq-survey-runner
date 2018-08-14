from freezegun import freeze_time
from tests.integration.integration_test_case import IntegrationTestCase

@freeze_time('2018-10-08')
class TestHappyPath(IntegrationTestCase):

    def test_date_range(self):
        self.launchSurvey('test',
                          'date_reference_ranges',
                          )

        self.post(action='start_questionnaire')

        # We are in the Questionnaire
        self.assertInPage('Did you have a paid job, either as an employee or self-employed, in the week')
        self.assertInPage('Monday 1 October 2018')
        self.assertInPage('Sunday 7 October 2018')

        self.post({
            'manual-range-radio': 'Yes'
        })

        # We're on the second question

        self.assertInPage('If you had been offered a job in the week starting')
        self.assertInPage('Monday 1 October')
        self.assertInPage('Monday 15 October')


        self.post({
            'date-separate-radio': 'Yes'
        })

        # We're on the third question

        self.assertInPage('In the 4 weeks between')
        self.assertInPage('10 September')
        self.assertInPage('7 October 2018')
