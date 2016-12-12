from werkzeug.datastructures import MultiDict

from tests.integration.create_token import create_token
from tests.integration.integration_test_case import IntegrationTestCase


class TestHouseholdQuestion(IntegrationTestCase):

    INTRODUCTION_PAGE = '/questionnaire/test/household_question/789/introduction'

    def setUp(self):
        super(TestHouseholdQuestion, self).setUp()

    def tearDown(self):
        super(TestHouseholdQuestion, self).tearDown()

    def test_add_answer(self):
        self.add_answers()

    def test_remove_answer(self):
        first_page = self.add_answers()
        self.remove_answer(first_page)

    def test_save_continue_should_save_answers(self):
        self.login_and_check_introduction_text()
        first_page = self.start_questionnaire()

        # Add first person
        form_data = MultiDict()

        form_data.add("first-name", 'John')
        form_data.add("first-name_1", 'Jane')
        form_data.add("first-name_2", 'Joe')
        form_data.add("first-name_3", 'Bran')
        form_data.add("action[save_continue]", "")

        resp = self.client.post(first_page, data=form_data, follow_redirects=False)
        composition_summary_page = resp.headers['Location']

        _, resp_url = self.household_answer_correct(composition_summary_page, 'Yes')
        resp = self.client.get(resp_url)
        content = resp.get_data(True)

        # Check content on summary page
        self.assertRegex(content, 'John')
        self.assertRegex(content, 'Jane')
        self.assertRegex(content, 'Joe')
        self.assertRegex(content, 'Bran')

    def test_can_return_to_composition_and_add_entries(self):
        first_page = self.add_answers()

        form_data = MultiDict()
        form_data.add("first-name", 'John')
        form_data.add("first-name_1", 'Jane')
        form_data.add("action[save_continue]", "")

        resp_url, resp = self.postRedirectGet(first_page, form_data)

        resp, resp_url = self.household_answer_correct(resp_url, 'No')

        form_data = MultiDict()
        form_data.add("first-name", 'John')
        form_data.add("first-name_1", 'Jane')
        form_data.add("first-name_2", 'Joe')
        form_data.add("middle-names", '')
        form_data.add("middle-names_1", '')
        form_data.add("middle-names_2", '')
        form_data.add("last-name", '')
        form_data.add("last-name_1", '')
        form_data.add("last-name_2", '')
        form_data.add("action[save_continue]", "")

        resp_url, resp = self.postRedirectGet(resp_url, form_data)
        content = resp.get_data(True)

        self.assertRegex(content, 'John')
        self.assertRegex(content, 'Jane')
        self.assertRegex(content, 'Joe')

        self.assertRegex(resp_url, 'household-summary')

    def test_composition_complete_progresses_to_summary(self):
        first_page = self.add_answers()

        form_data = MultiDict()
        form_data.add("first-name", 'John')
        form_data.add("first-name_1", 'Jane')
        form_data.add("action[save_continue]", "")

        resp_url, resp = self.postRedirectGet(first_page, form_data)

        self.assertRegex(resp_url, 'household-summary')

        form_data = MultiDict()
        form_data.add("household-composition-add-another", 'Yes')
        form_data.add("action[save_continue]", "")

        resp = self.client.post(resp_url, data=form_data, follow_redirects=False)
        resp_url = resp.headers['Location']

        self.assertEquals(resp.status_code, 302)

        self.assertRegex(resp_url, '/summary')

    def remove_answer(self, page):
        # Add first person
        form_data = MultiDict()
        form_data.add("first-name", 'John')
        form_data.add("first-name_1", 'Jane')
        form_data.add("first-name_2", 'Joe')
        form_data.add("first-name_3", '')
        form_data.add("action[remove_answer]", "1") # Remove Jane.
        resp = self.client.post(page, data=form_data, follow_redirects=False)

        self.assertEquals(resp.status_code, 200)

        resp = self.navigate_to_page(page)
        content = resp.get_data(True)
        self.assertRegex(content, 'first-name')
        self.assertRegex(content, 'first-name_2')
        self.assertRegex(content, 'first-name_3')

        self.assertNotRegex(content, 'first-name_1')

    def add_answers(self):
        self.login_and_check_introduction_text()
        first_page = self.start_questionnaire()

        # Add people
        form_data = MultiDict()
        form_data.add("first-name", 'John')
        form_data.add("first-name_1", 'Jane')
        form_data.add("first-name_2", 'Joe')
        form_data.add("action[add_answer]", "")
        resp = self.client.post(first_page, data=form_data, follow_redirects=False)

        self.assertEquals(resp.status_code, 200)

        resp = self.navigate_to_page(first_page)
        content = resp.get_data(True)
        self.assertRegex(content, 'first-name_1')
        self.assertRegex(content, 'first-name_2')
        self.assertRegex(content, 'first-name_3')

        return first_page

    def login_and_check_introduction_text(self):
        self.token = create_token('household_question', 'test')
        resp = self.get_first_page()
        self.check_introduction_text(resp)

    def get_first_page(self):
        resp = self.client.get('/session?token=' + self.token.decode(), follow_redirects=True)
        self.assertEquals(resp.status_code, 200)
        return resp

    def check_introduction_text(self, response):
        content = response.get_data(True)
        self.assertRegex(content, '<li>Household questions.</li>')

    def start_questionnaire(self):
        # Go to questionnaire
        post_data = {
            'action[start_questionnaire]': 'Start Questionnaire'
        }
        resp = self.client.post(self.INTRODUCTION_PAGE, data=post_data, follow_redirects=False)
        self.assertEquals(resp.status_code, 302)

        return resp.headers['Location']

    def navigate_to_page(self, page):
        resp = self.client.get(page, follow_redirects=False)
        self.assertEquals(resp.status_code, 200)
        return resp

    def household_answer_correct(self, resp_url, answer):
        form_data = MultiDict()
        form_data.add("household-composition-add-another", answer)
        form_data.add("action[save_continue]", "")
        resp = self.client.post(resp_url, data=form_data, follow_redirects=False)
        resp_url = resp.headers['Location']
        return resp, resp_url
