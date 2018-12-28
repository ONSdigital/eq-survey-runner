from tests.integration.integration_test_case import IntegrationTestCase


class MultipleSurveysOpen(IntegrationTestCase):

    def test_multiple_surveys_open(self):
        # We start the first survey
        self.launchSurvey('test', 'numbers')
        self.post(action='start_questionnaire')
        self.assertInUrl(r'/questionnaire/test/numbers/789/test/0/set-min-max-block')

        # Remember url for later
        first_url = self.last_url

        # We start the second survey
        self.launchSurvey('test', 'dates')
        self.post(action='start_questionnaire')
        self.assertInUrl('/questionnaire/test/dates/789/dates/0/date-block')

        # We now try to post to the first survey, which is out of date
        form_data = {
            'set-minimum': '0',
            'set-maximum': '1001',
        }

        self.post(url=first_url, post_data=form_data)
        self.assertInBody('Information')
        self.assertInBody('Unfortunately you can only complete one survey at a time.')
        self.assertInBody('Close this window to continue with your current survey.')


    def test_multiple_surveys_open_invalid_csrf(self):
        # We start the first survey
        self.launchSurvey('test', 'numbers')
        self.post(action='start_questionnaire')
        self.assertInUrl(r'/questionnaire/test/numbers/789/test/0/set-min-max-block')

        # Remember url for later
        first_url = self.last_url

        # We start the second survey
        self.launchSurvey('test', 'dates')
        self.post(action='start_questionnaire')
        self.assertInUrl('/questionnaire/test/dates/789/dates/0/date-block')

        # We now try to post to the first survey, which is out of date
        form_data = {
            'set-minimum': '0',
            'set-maximum': '1001',
        }

        self.last_csrf_token = None

        self.post(url=first_url, post_data=form_data)
        self.assertInBody('Information')
        self.assertInBody('Unfortunately you can only complete one survey at a time.')
        self.assertInBody('Close this window to continue with your current survey.')
