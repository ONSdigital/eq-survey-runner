from mock import patch

from tests.integration.integration_test_case import IntegrationTestCase


class TestRepeatingRelationship(IntegrationTestCase):

    def setUp(self):
        super().setUp()
        self.launchSurvey('test', 'relationship_household', roles=['dumper'])

    def test_should_ask_twenty_four_relationships_when_twenty_five_max_limit_and_twenty_six_people_added(self):
        # Given
        answer_id = 'household-{instance}-first-name'
        answer_value = 'Joe_{instance}'
        twenty_six_people = {}
        for i in range(27):
            twenty_six_people[answer_id.format(instance=i)] = answer_value.format(instance=i)

        # When
        self.post(twenty_six_people)

        # Then
        last_relationship_page = 'questionnaire/test/relationship_household/789/household-relationships/23/relationships'
        self.get(url=last_relationship_page)
        self.assertInBody('Describe how this person is related to the others')

    @patch('app.helpers.schema_helpers.uuid4', side_effect=range(100))
    def test_multiple_relationship_groups(self, mock): # pylint: disable=unused-argument
        # Given
        household_form_data = {
            'household-0-first-name': 'Han',
            'household-1-first-name': 'Leia',
            'household-2-first-name': 'Luke'
        }
        self.post(household_form_data)

        # When
        relationship_form_data_1 = {
            'who-is-related-0': 'Husband or wife',
            'who-is-related-1': 'Relation - other'
        }
        self.post(relationship_form_data_1)

        relationship_form_data_2 = {
            'who-is-related-0': 'Brother or sister'
        }
        self.post(relationship_form_data_2)

        # Then
        relationship_answers = [
            answer for answer in self.dumpAnswers()['answers']
            if answer['answer_id'] == 'who-is-related'
        ]

        expected_relationship_answers = [
            {
                'answer_id': 'who-is-related',
                'answer_instance': 0,
                'group_instance': 0,
                'group_instance_id': '1',
                'value': 'Husband or wife'
            },
            {
                'answer_id': 'who-is-related',
                'answer_instance': 1,
                'group_instance': 0,
                'group_instance_id': '1',
                'value': 'Relation - other'
            },
            {
                'answer_id': 'who-is-related',
                'answer_instance': 0,
                'group_instance': 1,
                'group_instance_id': '2',
                'value': 'Brother or sister'
            }
        ]
        self.assertEqual(expected_relationship_answers, relationship_answers)
