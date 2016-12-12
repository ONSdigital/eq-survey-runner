from werkzeug.datastructures import MultiDict

from tests.integration.create_token import create_token
from tests.integration.integration_test_case import IntegrationTestCase


class TestRepeatingHousehold(IntegrationTestCase):

    INTRODUCTION_PAGE = '/questionnaire/test/repeating_household/789/introduction'

    def setUp(self):
        super(TestRepeatingHousehold, self).setUp()

        self.token = create_token('repeating_household', 'test')
        self.client.get('/session?token=' + self.token.decode(), follow_redirects=True)
        resp = self.client.post(
            self.INTRODUCTION_PAGE,
            data={'action[start_questionnaire]': 'Start Questionnaire'},
            follow_redirects=False)
        self.first_page = resp.headers['Location']

    def tearDown(self):
        super(TestRepeatingHousehold, self).tearDown()

    def test_change_repeat_answer_removes_all_answers_for_repeated_groups(self):
        # Given I add some people
        household_composition_page = self.first_page
        form_data = MultiDict()
        form_data.add("first-name", 'Joe')
        form_data.add("last-name", 'Bloggs')
        form_data.add("first-name_1", 'Jane')
        form_data.add("last-name_1", 'Doe')
        form_data.add("action[save_continue]", '')
        resp = self.client.post(household_composition_page, data=form_data, follow_redirects=False)
        person1_age_page = resp.headers['Location']

        # And provide details
        self.navigate_to_page(person1_age_page)
        form_data = MultiDict()
        form_data.add("what-is-your-age", '9990')
        form_data.add("action[save_continue]", '')
        resp = self.client.post(person1_age_page, data=form_data, follow_redirects=False)
        person1_shoe_size_page = resp.headers['Location']

        self.navigate_to_page(person1_shoe_size_page)
        form_data = MultiDict()
        form_data.add("what-is-your-shoe-size", '9991')
        form_data.add("action[save_continue]", '')
        resp = self.client.post(person1_shoe_size_page, data=form_data, follow_redirects=False)
        person2_age_page = resp.headers['Location']

        self.navigate_to_page(person2_age_page)
        form_data = MultiDict()
        form_data.add("what-is-your-age", '9992')
        form_data.add("action[save_continue]", '')
        resp = self.client.post(person2_age_page, data=form_data, follow_redirects=False)
        person2_shoe_size_page = resp.headers['Location']

        self.navigate_to_page(person2_shoe_size_page)
        form_data = MultiDict()
        form_data.add("what-is-your-shoe-size", '9993')
        form_data.add("action[save_continue]", '')
        self.client.post(person2_shoe_size_page, data=form_data, follow_redirects=False)

        # When I go back to household composition page and submit
        self.navigate_to_page(household_composition_page)
        form_data = MultiDict()
        form_data.add("first-name", 'Joe')
        form_data.add("last-name", 'Bloggs')
        form_data.add("first-name_1", 'Jane')
        form_data.add("last-name_1", 'Doe')
        form_data.add("action[save_continue]", '')
        resp = self.client.post(household_composition_page, data=form_data, follow_redirects=True)

        # Then the details previously entered for the people should have been removed
        content = resp.get_data(True)
        self.assertRegex(content, 'Joe Bloggs')
        self.assertRegex(content, 'What is their age')
        self.assertNotRegex(content, '9990')
        form_data = MultiDict()
        form_data.add("what-is-your-age", '34')
        form_data.add("action[save_continue]", '')
        self.client.post(person1_age_page, data=form_data, follow_redirects=True)

        form_data = MultiDict()
        form_data.add("what-is-your-shoe-size", '10')
        form_data.add("action[save_continue]", '')
        resp = self.client.post(person1_shoe_size_page, data=form_data, follow_redirects=True)

        content = resp.get_data(True)
        self.assertRegex(content, 'Jane Doe')
        self.assertRegex(content, 'What is their age')
        self.assertNotRegex(content, '9992')

    def navigate_to_page(self, page):
        resp = self.client.get(page, follow_redirects=False)
        self.assertEquals(resp.status_code, 200)
        return resp
