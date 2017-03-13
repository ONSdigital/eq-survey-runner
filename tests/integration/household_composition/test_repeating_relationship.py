from tests.integration.integration_test_case import IntegrationTestCase


class TestRepeatingRelationship(IntegrationTestCase):

    def setUp(self):
        super().setUp()
        self.launchSurvey('census', 'household')
        self.post({'permanent-or-family-home-answer': 'Yes'})
        self.household_composition_url = self.last_url

    def test_should_ask_twenty_four_relationships_when_twenty_five_max_limit_and_twenty_six_people_added(self):
        # Given
        answer_id = 'household-{instance}-first-name'
        answer_value = 'Joe_{instance}'
        twenty_six_people = {}
        for i in range(27):
            twenty_six_people[answer_id.format(instance=i)] = answer_value.format(instance=i)

        # When
        self.post(twenty_six_people)

        # Mandatory visitors question
        self.post({'overnight-visitors-answer': 0})

        # Then
        last_relationship_page = 'questionnaire/census/household/789/who-lives-here-relationship/23/household-relationships'
        self.get(url=last_relationship_page)
        self.assertInPage('How is Joe_23 related to the people below')
        self.post(url=last_relationship_page)
        self.assertInUrl('who-lives-here-completed')

