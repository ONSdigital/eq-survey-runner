from tests.integration.integration_test_case import IntegrationTestCase


class MultipleSurveysOpen(IntegrationTestCase):

    def test_multiple_surveys_open(self):
        # We start the first survey
        self.launchSurvey('test', 'numbers')
        self.post(action='start_questionnaire')
        self.assertInUrl(r'/questionnaire/test/numbers/789/test/0/set-min-max-block')

        # Remember url for later
        first_url = self.last_url
        first_csrf_token = self.last_csrf_token

        # We start the second survey
        self.launchSurvey('test', 'dates')
        self.post(action='start_questionnaire')
        self.assertInUrl('/questionnaire/test/dates/789/dates/0/date-block')

        # We now try to post to the first survey,
        # which is out of date and using it's csrf token
        self.last_csrf_token = first_csrf_token
        form_data = {
            'set-minimum': '0',
            'set-maximum': '1001',
        }

        self.post(url=first_url, post_data=form_data)
        # Shows multiple survey error
        self.assertInBody('Information')
        self.assertInBody('Unfortunately you can only complete one survey at a time.')

    def test_different_metadata_store_to_url(self):
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

        # We now try to refresh the first survey, which is out of date
        self.get(url=first_url)
        # Shows multiple survey error
        self.assertInBody('Information')
        self.assertInBody('Unfortunately you can only complete one survey at a time.')

    def test_initial_survey_completed(self):
        # We complete the first survey
        self.launchSurvey('test', 'introduction')
        self.post(action='start_questionnaire')
        self.post(action=None)
        self.post(action=None)

        # check we're on the thank you page
        self.assertInUrl('thank-you')

        # Remember url for later
        first_url = self.last_url

        # We start the second survey
        self.launchSurvey('test', 'dates')
        self.post(action='start_questionnaire')
        self.assertInUrl('/questionnaire/test/dates/789/dates/0/date-block')

        # We now try to refresh the first survey, which is out of date
        self.get(url=first_url)

        # Shows session expired
        self.assertInBody('Your session has expired')
        self.assertInBody('To help protect your information we have signed you out.')
