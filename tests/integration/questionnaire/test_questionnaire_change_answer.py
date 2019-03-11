from tests.integration.integration_test_case import IntegrationTestCase


class TestQuestionnaireChangeAnswer(IntegrationTestCase):

    def test_change_non_mandatory_date_from_answered_to_not_answered(self):

        # Given the test_dates questionnaire with a non-mandatory date answered.
        self.launchSurvey('test', 'dates')

        post_data = [
            {
                'date-range-from-answer-day': '1',
                'date-range-from-answer-month': '1',
                'date-range-from-answer-year': '2017',
                'date-range-to-answer-day': '2',
                'date-range-to-answer-month': '1',
                'date-range-to-answer-year': '2017'
            }, {
                'month-year-answer-month': '1',
                'month-year-answer-year': '2016'
            }, {
                'single-date-answer-day': '1',
                'single-date-answer-month': '1',
                'single-date-answer-year': '2016'
            }, {
                # non-mandatory dates answered
                'non-mandatory-date-answer-day': '22',
                'non-mandatory-date-answer-month': '2',
                'non-mandatory-date-answer-year': '2099'
            }, {
                'year-date-answer-year': '2017'
            }
        ]

        for datum in post_data:
            self.post(datum)

        self.assertInBody('Application of min and max filters to dates')
        self.post(action='save_continue')
        self.assertInBody('22 February 2099')
        self.assertNotInBody('No answer provided')

        # When we change the non-mandatory date from answered to not answered
        self.get('questionnaire/date-non-mandatory-block')

        unanswered_post_data = {
            'non-mandatory-date-answer-day': '',
            'non-mandatory-date-answer-month': '',
            'non-mandatory-date-answer-year': ''
        }

        self.post(unanswered_post_data)

        # Then the original value is replaced with 'No answer provided' on the summary page
        self.assertNotInBody('22 February 2099')
        self.assertInBody('No answer provided')
