from tests.integration.routing import routes
from tests.integration.create_token import create_token
from tests.integration.integration_test_case import IntegrationTestCase
from tests.integration.star_wars import star_wars_test_urls


class TestRouting(IntegrationTestCase):

    def setUp(self):
        super().setUp()

    def test_routing_paths(self):

        # Find all the routes through the questionnaire and step through each one
        all_routes = routes.get_all_routes()
        for route in all_routes:
            self.navigate_route(route)

    def navigate_route(self, route):

        resp = self.start_questionnaire()
        current_page = resp.headers['Location']
        resp = self.client.get(resp.headers['Location'], follow_redirects=True)

        summary_assertions = []

        # Each route has a list of blocks, each block has rules on routing
        for block in route:
            for rule in block:
                content = resp.get_data(True)

                # Use the rule to generate the form data to submit and the assertion for the summary page
                form_data, rule_assertions = self.generate_form_data(rule, content)
                summary_assertions.append(rule_assertions)

                # Post the data
                resp = self.client.post(current_page, data=form_data, follow_redirects=False)
                current_page = resp.headers['Location']

                # We must check we are on the next page
                self.assertRegexpMatches(resp.headers['Location'], rule['destination_id'])
                resp = self.client.get(current_page, follow_redirects=False)

                if 'summary' in current_page:
                    self.summary_page_checks(resp, summary_assertions)

    def summary_page_checks(self, resp, summary_assertions):
        # Check everything is on the summary page as expected
        content = resp.get_data(True)
        for assertions in summary_assertions:
            for assertion in assertions:
                self.assertRegexpMatches(content, assertion)

    def generate_form_data(self, rule, content):
        # each page needs data to submit, that information is stored in the rule
        form_data = {}
        rule_assertions = []
        for answer in rule['answers']:
            form_data[answer['answer_id']] = answer['user_answer']
            # We need to assert the answer is on the page
            self.assertRegexpMatches(content, answer['answer'])
            # We also need to prepare the assertions for the summary page
            rule_assertions.append(answer['user_answer'])
            rule_assertions.append(answer['answer'])
        form_data["action[save_continue]"] = "Save &amp; Continue"

        return form_data, rule_assertions

    def start_questionnaire(self):
        self.token = create_token('star_wars', '0')
        self.client.get('/session?token=' + self.token.decode(), follow_redirects=True)
        post_data = {
          'action[start_questionnaire]': 'Start Questionnaire'
        }
        resp = self.client.post(star_wars_test_urls.STAR_WARS_INTRODUCTION, data=post_data, follow_redirects=False)
        return resp
