from werkzeug.datastructures import MultiDict

from tests.integration.integration_test_case import IntegrationTestCase


class TestRepeatingHousehold(IntegrationTestCase):

    def setUp(self):
        super().setUp()
        self.launchSurvey('test', 'repeating_household')
        self.post(action='start_questionnaire')
        self.household_composition_url = self.last_url

    def test_change_repeat_answer_removes_all_answers_for_repeated_groups(self):
        # Given I add some people
        form_data = MultiDict()
        form_data.add('household-0-first-name', 'Joe')
        form_data.add('household-0-middle-names', '')
        form_data.add('household-0-last-name', 'Bloggs')
        form_data.add('household-1-first-name', 'Jane')
        form_data.add('household-1-middle-names', '')
        form_data.add('household-1-last-name', 'Doe')
        self.post(form_data)

        # And provide details
        self.post({'what-is-your-age': '9990'})
        self.post({'what-is-your-shoe-size': '9991'})
        self.post({'what-is-your-age': '9992'})
        self.post({'what-is-your-shoe-size': '9993'})

        # When I go back to household composition page and make changes and submit
        self.get(self.household_composition_url)

        form_data = MultiDict()
        form_data.add('household-0-first-name', 'Joe')
        form_data.add('household-0-middle-names', 'S')
        form_data.add('household-0-last-name', 'Bloggs')
        form_data.add('household-1-first-name', 'Jane')
        form_data.add('household-1-middle-names', '')
        form_data.add('household-1-last-name', 'Doe')
        self.post(form_data)

        # Then the details previously entered for the people should have been removed
        self.assertInPage('Joe Bloggs')
        self.assertInPage('What is their age')
        self.assertNotInPage('9990')

        self.post({'what-is-your-age': '34'})
        self.post({'what-is-your-shoe-size': '10'})

        self.assertInPage('Jane Doe')
        self.assertInPage('What is their age')
        self.assertNotInPage('9992')

    def test_no_change_repeat_answer_keeps_repeated_groups(self):
        # Given I add some people
        household_data = MultiDict()
        household_data.add('household-0-first-name', 'Joe')
        household_data.add('household-0-middle-names', '')
        household_data.add('household-0-last-name', 'Bloggs')
        household_data.add('household-1-first-name', 'Jane')
        household_data.add('household-1-middle-names', '')
        household_data.add('household-1-last-name', 'Doe')
        self.post(household_data)

        # And answer a question about the first persion
        self.post({'what-is-your-age': '18'})

        # When I go back to household composition page and submit without any changes
        self.get(self.household_composition_url)
        self.post(household_data)

        # Then the details previously entered for the people should have been kept
        self.assertInPage('Joe Bloggs')
        self.assertInPage('What is their age')
        self.assertInPage('18')
