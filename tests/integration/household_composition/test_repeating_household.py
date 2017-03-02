from werkzeug.datastructures import MultiDict

from tests.integration.create_token import create_token
from tests.integration.integration_test_case import IntegrationTestCase
from tests.integration.navigation import navigate_to_page


class TestRepeatingHousehold(IntegrationTestCase):

    INTRODUCTION_PAGE = '/questionnaire/test/repeating_household/789/multiple-questions-group/0/introduction'

    def setUp(self):
        super().setUp()

        self.token = create_token('repeating_household', 'test')
        self.client.get('/session?token=' + self.token.decode(), follow_redirects=False)
        resp = self.get_and_post_with_csrf_token(
            self.INTRODUCTION_PAGE,
            data={'action[start_questionnaire]': 'Start Questionnaire'},
            follow_redirects=False)
        self.first_page = resp.location

    def tearDown(self):
        super(TestRepeatingHousehold, self).tearDown()

    def test_change_repeat_answer_removes_all_answers_for_repeated_groups(self):
        # Given I add some people
        household_composition_page = self.first_page

        form_data = MultiDict()
        form_data.add("household-0-first-name", 'Joe')
        form_data.add("household-0-middle-names", '')
        form_data.add("household-0-last-name", 'Bloggs')
        form_data.add("household-1-first-name", 'Jane')
        form_data.add("household-1-middle-names", '')
        form_data.add("household-1-last-name", 'Doe')
        form_data.add("action[save_continue]", '')

        resp = self.get_and_post_with_csrf_token(household_composition_page, data=form_data, follow_redirects=False)
        person1_age_page = resp.location

        # And provide details
        navigate_to_page(self.client, person1_age_page)
        form_data = MultiDict()
        form_data.add("what-is-your-age", '9990')
        form_data.add("action[save_continue]", '')
        resp = self.get_and_post_with_csrf_token(person1_age_page, data=form_data, follow_redirects=False)
        person1_shoe_size_page = resp.location

        navigate_to_page(self.client, person1_shoe_size_page)
        form_data = MultiDict()
        form_data.add("what-is-your-shoe-size", '9991')
        form_data.add("action[save_continue]", '')
        resp = self.get_and_post_with_csrf_token(person1_shoe_size_page, data=form_data, follow_redirects=False)
        person2_age_page = resp.location

        navigate_to_page(self.client, person2_age_page)
        form_data = MultiDict()
        form_data.add("what-is-your-age", '9992')
        form_data.add("action[save_continue]", '')
        resp = self.get_and_post_with_csrf_token(person2_age_page, data=form_data, follow_redirects=False)
        person2_shoe_size_page = resp.location

        navigate_to_page(self.client, person2_shoe_size_page)
        form_data = MultiDict()
        form_data.add("what-is-your-shoe-size", '9993')
        form_data.add("action[save_continue]", '')
        self.get_and_post_with_csrf_token(person2_shoe_size_page, data=form_data, follow_redirects=False)

        # When I go back to household composition page and make changes and submit
        navigate_to_page(self.client, household_composition_page)
        form_data = MultiDict()

        form_data.add("household-0-first-name", 'Joe')
        form_data.add("household-0-middle-names", 'S')
        form_data.add("household-0-last-name", 'Bloggs')
        form_data.add("household-1-first-name", 'Jane')
        form_data.add("household-1-middle-names", '')
        form_data.add("household-1-last-name", 'Doe')

        form_data.add("action[save_continue]", '')
        resp = self.get_and_post_with_csrf_token(household_composition_page, data=form_data, follow_redirects=True)

        # Then the details previously entered for the people should have been removed
        content = resp.get_data(True)
        self.assertRegex(content, 'Joe Bloggs')
        self.assertRegex(content, 'What is their age')
        self.assertNotRegex(content, '9990')
        form_data = MultiDict()
        form_data.add("what-is-your-age", '34')
        form_data.add("action[save_continue]", '')
        self.get_and_post_with_csrf_token(person1_age_page, data=form_data, follow_redirects=True)

        form_data = MultiDict()
        form_data.add("what-is-your-shoe-size", '10')
        form_data.add("action[save_continue]", '')
        resp = self.get_and_post_with_csrf_token(person1_shoe_size_page, data=form_data, follow_redirects=True)

        content = resp.get_data(True)
        self.assertRegex(content, 'Jane Doe')
        self.assertRegex(content, 'What is their age')
        self.assertNotRegex(content, '9992')

    def test_no_change_repeat_answer_keeps_repeated_groups(self):

        # Given I add some people
        household_composition_page = self.first_page

        household_data = MultiDict()

        household_data.add("household-0-first-name", 'Joe')
        household_data.add("household-0-middle-names", '')
        household_data.add("household-0-last-name", 'Bloggs')
        household_data.add("household-1-first-name", 'Jane')
        household_data.add("household-1-middle-names", '')
        household_data.add("household-1-last-name", 'Doe')

        household_data.add("action[save_continue]", '')

        resp = self.get_and_post_with_csrf_token(household_composition_page, data=household_data, follow_redirects=False)
        person1_age_page = resp.location

        # And provide details
        navigate_to_page(self.client, person1_age_page)
        form_data = MultiDict()
        form_data.add("what-is-your-age", '18')
        form_data.add("action[save_continue]", '')
        self.get_and_post_with_csrf_token(person1_age_page, data=form_data, follow_redirects=False)

        # When I go back to household composition page and submit without any changes
        resp = navigate_to_page(self.client, household_composition_page)

        post_data = household_data.copy()
        post_data.update({"csrf_token": self.extract_csrf_token(resp.get_data(True))})
        resp = self.client.post(household_composition_page, data=post_data, follow_redirects=True)

        # Then the details previously entered for the people should have been kept
        content = resp.get_data(True)
        self.assertRegex(content, 'Joe Bloggs')
        self.assertRegex(content, 'What is their age')
        self.assertRegex(content, '18')
