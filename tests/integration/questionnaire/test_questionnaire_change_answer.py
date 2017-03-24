from tests.integration.integration_test_case import IntegrationTestCase


class TestQuestionnaireChangeAnswer(IntegrationTestCase):

    def test_change_non_mandatory_date_from_answered_to_not_answered(self):

        # Given the test_dates questionnaire with a non-mandatory date answered.
        self.launchSurvey('test', 'dates')

        post_data = {
            'date-range-from-day': '1',
            'date-range-from-month': '1',
            'date-range-from-year': '2017',
            'date-range-to-day': '2',
            'date-range-to-month': '1',
            'date-range-to-year': '2017',
            'month-year-answer-month': '1',
            'month-year-answer-year': '2016',
            'single-date-answer-day': '1',
            'single-date-answer-month': '1',
            'single-date-answer-year': '2016',

            # non-mandatory date answered
            'non-mandatory-date-answer-day': '22',
            'non-mandatory-date-answer-month': '2',
            'non-mandatory-date-answer-year': '2099',
        }

        self.post(post_data)
        self.assertInPage('22 February 2099')
        self.assertNotInPage('No answer provided')

        # When we change the non-mandatory date from answered to not answered
        self.get('questionnaire/test/dates/789/dates/0/date-block')

        post_data = {
            'date-range-from-day': '1',
            'date-range-from-month': '1',
            'date-range-from-year': '2017',
            'date-range-to-day': '2',
            'date-range-to-month': '1',
            'date-range-to-year': '2017',
            'month-year-answer-month': '1',
            'month-year-answer-year': '2016',
            'single-date-answer-day': '1',
            'single-date-answer-month': '1',
            'single-date-answer-year': '2016',

            # non-mandatory date not answered
            'non-mandatory-date-answer-day': '',
            'non-mandatory-date-answer-month': '',
            'non-mandatory-date-answer-year': '',
        }

        self.post(post_data)

        # Then the original value is replaced with 'No answer provided' on the summary page
        self.assertNotInPage('22 February 2099')
        self.assertInPage('No answer provided')
