from tests.integration.integration_test_case import IntegrationTestCase
from tests.integration.routing import routes


class TestRouting(IntegrationTestCase):

    def test_routing_paths(self):

        # Find all the routes through the questionnaire and step through each one
        all_routes = routes.get_all_routes()
        for route in all_routes:
            self._navigate_route(route)

    def _navigate_route(self, route):
        self.clearDatabase()
        self.launchSurvey('0', 'star_wars')
        self.post(action='start_questionnaire')

        summary_assertions = []

        # Each route has a list of blocks, each block has rules on routing
        for block in route:
            for rule in block:
                # Use the rule to generate the form data to submit and the assertion for the summary page
                form_data, rule_assertions = self._generate_form_data(rule)
                summary_assertions.append(rule_assertions)

                # Post the data
                self.post(form_data)

                # We must check we are on the next page
                self.assertInUrl(rule['destination_id'])

                if 'summary' in self.last_url:
                    self._summary_page_checks(summary_assertions)

    def _generate_form_data(self, rule):
        # each page needs data to submit, that information is stored in the rule
        form_data = {}
        rule_assertions = []
        for answer in rule['answers']:
            form_data[answer['answer_id']] = answer['user_answer']
            # We need to assert the answer is on the page
            self.assertInPage(answer['answer'])
            # We also need to prepare the assertions for the summary page
            rule_assertions.append(answer['user_answer'])
            rule_assertions.append(answer['answer'])

        return form_data, rule_assertions

    def _summary_page_checks(self, summary_assertions):
        # Check everything is on the summary page as expected
        for assertions in summary_assertions:
            for assertion in assertions:
                self.assertInPage(assertion)
