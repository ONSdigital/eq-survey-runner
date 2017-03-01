from tests.integration.create_token import create_token
from tests.integration.integration_test_case import IntegrationTestCase


class TestRepeatingRelationship(IntegrationTestCase):

    def setUp(self):
        super(TestRepeatingRelationship, self).setUp()

        self.token = create_token('household', 'census')
        resp = self.client.get('/session?token=' + self.token.decode(), follow_redirects=False)
        is_home = {'permanent-or-family-home-answer': 'Yes'}
        resp = self.client.post(resp.location, data=is_home, follow_redirects=False)
        self.household_composition_location = resp.location

    def test_should_ask_twenty_four_relationships_when_twenty_five_max_limit_and_twenty_six_people_added(self):
        # Given
        answer_id = 'household-{instance}-first-name'
        save_continue = {'action[save_continue]': ''}
        twenty_six_people = save_continue.copy()
        for i in range(27):
            twenty_six_people[answer_id.format(instance=i)] = 'Joe'

        # When
        resp = self.client.post(self.household_composition_location, data=twenty_six_people, follow_redirects=False)
        self.answer_mandatory_visitors_question(resp, save_continue)

        # Then
        last_relationship_page = 'questionnaire/census/household/789/who-lives-here-relationship/23/household-relationships'
        resp = self.client.post(last_relationship_page, data=save_continue, follow_redirects=False)
        self.assertIn('who-lives-here-completed', resp.location)

    def answer_mandatory_visitors_question(self, resp, save_continue):
        self.client.post(resp.location, data=save_continue, follow_redirects=False)
        visitors = save_continue.copy()
        visitors['overnight-visitors-answer'] = 0
        self.client.post(resp.location, data=save_continue, follow_redirects=False)
