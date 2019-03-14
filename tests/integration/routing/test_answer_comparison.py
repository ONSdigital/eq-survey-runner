from tests.integration.integration_test_case import IntegrationTestCase


class TestAnswerComparisonsSkips(IntegrationTestCase):
    """
    Test that skip conditions work correctly when answer comparisons are
    used in the `when` clause.
    """

    def test_skip_condition_answer_comparison(self):
        self.launchSurvey('test',
                          'skip_condition_answer_comparison',
                          )

        self.post(action='start_questionnaire')

        # We are in the Questionnaire
        self.assertInBody('Enter your first number')

        self.post({
            'comparison-1-answer': 2
        })

        self.assertInBody('Enter your second number')

        second_page = self.last_url

        self.post({
            'comparison-2-answer': 3
        })

        self.assertInBody('First less than second')

        # Go back to the second question and change the answer
        self.post({
            'comparison-2-answer': 2
        }, url=second_page)

        self.assertInBody('Second equal first')

        # Go back to the second question and change the answer
        self.post({
            'comparison-2-answer': 1
        }, url=second_page)

        self.assertInBody('First greater than second')

class TestAnswerComparisonsRoutes(IntegrationTestCase):
    """
    Test routing when answer comparisons are used in the `when` clause.
    """

    def test_routes_over_interstitial(self):
        self.launchSurvey('test', 'routing_answer_comparison')

        self.post(action='start_questionnaire')

        # We are in the Questionnaire
        self.assertInBody('Enter your first number')

        self.post({
            'route-comparison-1-answer': 2
        })

        self.assertInBody('Enter a higher number to skip')

        second_page = self.last_url

        # Enter a higher number
        self.post({
            'route-comparison-2-answer': 3
        })

        self.assertInBody('Your second number was higher')

        # Go back to the second question and change the answer to a lower one
        self.post({
            'route-comparison-2-answer': 1
        }, url=second_page)

        self.assertInBody('Your second number was lower or equal')
