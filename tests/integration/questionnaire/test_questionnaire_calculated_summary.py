from tests.integration.integration_test_case import IntegrationTestCase


class TestQuestionnaireCalculatedSummary(IntegrationTestCase):

    BASE_URL = '/questionnaire/'

    def test_calculated_summary(self):
        self.launchSurvey('test', 'calculated_summary')
        self.post({'first-number-answer': '10'})
        self.post(
            {
                'second-number-answer': '20',
                'second-number-answer-unit-total': '20',
                'second-number-answer-also-in-total': '20',
            }
        )
        self.post({'third-number-answer': '30'})
        self.post({'third-and-a-half-number-answer-unit-total': '30'})
        self.post({'skip-fourth-block-answer': 'Yes'})
        self.post({'fifth-percent-answer': '50', 'fifth-number-answer': '50'})
        self.post({'sixth-percent-answer': '60', 'sixth-number-answer': '60'})
        self.assertInBody('Skipped Fourth')
        self.assertInBody(
            'We calculate the total of currency values entered to be £80.00'
        )
