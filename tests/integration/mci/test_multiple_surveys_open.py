from tests.integration.integration_test_case import IntegrationTestCase


class MultipleSurveysOpen(IntegrationTestCase):

    def test_multiple_surveys_open(self):
        # We start the first survey
        self.launchSurvey('1', '0205')
        self.post(action='start_questionnaire')
        self.assertInUrl('/questionnaire/1/0205/789/mci/0/reporting-period')

        # Remember url for later
        first_url = self.last_url

        # We start the second survey
        self.launchSurvey('1', '0203')
        self.post(action='start_questionnaire')
        self.assertInUrl(r'/questionnaire/1/0203/789/mci/0/reporting-period')

        # We now try to post to the first survey, which is out of date
        form_data = {
            'period-from-day': '01',
            'period-from-month': '4',
            'period-from-year': '2016',
            'period-to-day': '30',
            'period-to-month': '4',
            'period-to-year': '2016',
            'total-retail-turnover': '100000'
        }

        self.post(url=first_url, post_data=form_data)
        self.assertInPage('Information')
        self.assertInPage('Unfortunately you can only complete one survey at a time.')
        self.assertInPage('Close this window to continue with your current survey.')
