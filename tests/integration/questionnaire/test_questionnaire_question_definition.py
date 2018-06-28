from tests.integration.integration_test_case import IntegrationTestCase


class TestQuestionnaireQuestionDefinition(IntegrationTestCase):

    def test_question_definition(self):
        # Given I launch a questionnaire with a definition
        self.launchSurvey('test', 'question_definition')

        # When I start the survey I am presented with the definition title and description correctly
        self.assertInPage('Do you connect a LiFePO4 battery to your photovoltaic system to store surplus energy?')
        self.assertInPage('What is a photovoltaic system?')
        self.assertInPage('A typical photovoltaic system employs solar panels, each comprising a number of solar cells, '
                          'which generate electrical power. PV installations may be ground-mounted, rooftop mounted or wall mounted. '
                          'The mount may be fixed, or use a solar tracker to follow the sun across the sky.')

        # When we continue we go to the summary page
        self.post(action='save_continue')
        self.assertInUrl('summary')

        # And Submit my answers
        self.post(action='submit_answers')
        self.assertInUrl('thank-you')
