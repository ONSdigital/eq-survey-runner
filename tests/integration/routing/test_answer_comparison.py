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


class TestAnswerComparisonsRepeating(IntegrationTestCase):
    """
    Test the repeat until clause using an answer comparison in the when
    clause.
    """

    def test_repeat_until_comparison(self):
        self.launchSurvey('test', 'repeating_answer_comparison')

        self.post(action='start_questionnaire')

        # We are in the Questionnaire
        self.assertInBody('Enter a number')

        self.post({
            'repeating-comparison-1-answer': 2
        })

        self.assertInBody('Enter the same number to stop')

        # Enter a different number, the question should repeat
        self.post({
            'repeating-comparison-2-answer': 3
        })

        self.assertInBody('Enter a number')

        # The question should have repeated
        self.post({
            'repeating-comparison-1-answer': 1
        })

        self.assertInBody('Enter the same number to stop')

        # Enter the same number, the summary should appear
        self.post({
            'repeating-comparison-2-answer': 1
        })

        self.assertInBody('Check your answers and submit')


class TestRepeatingAnswerComparisonToNormalAnswer(IntegrationTestCase):
    """
    Test that comparing a repeating group answer to a normal answer works
    """

    def test_repeating_answer_comparison_to_normal_answer(self):
        self.launchSurvey('test', 'repeating_answer_comparison_different_groups')

        self.post(action='start_questionnaire')

        # We are in the Questionnaire
        self.assertInBody('Enter a number')

        self.post({
            'primary-answer': 10
        })

        self.assertInBody('Enter a different number to repeat this question')

        # Enter a different number, the question should repeat
        self.post({
            'repeating-comparison-1-answer': 3
        })

        self.assertInBody('Enter a different number to repeat this question')

        # The question should have repeated
        self.post({
            'repeating-comparison-1-answer': 1
        })

        self.assertInBody('Enter a different number to repeat this question')

        # The question should have repeated
        self.post({
            'repeating-comparison-1-answer': 7
        })

        self.assertInBody('Enter a different number to repeat this question')

        # Enter the same number, the summary should appear
        self.post({
            'repeating-comparison-1-answer': 10
        })

        self.assertInBody('Check your answers and submit')
