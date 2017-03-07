from werkzeug.datastructures import MultiDict

from tests.integration.create_token import create_token
from tests.integration.integration_test_case import IntegrationTestCase
from tests.integration.navigation import navigate_to_page


class TestHouseholdQuestion(IntegrationTestCase):

    INTRODUCTION_PAGE = '/questionnaire/test/household_question/789/multiple-questions-group/0/introduction'

    def setUp(self):
        super(TestHouseholdQuestion, self).setUp()

    def tearDown(self):
        super(TestHouseholdQuestion, self).tearDown()

    def test_add_answer(self):
        self.add_answers()

    def test_remove_answer(self):
        resp, first_page = self.add_answers()
        self.remove_answer(first_page)

    def test_save_continue_should_save_answers(self):
        resp = self.login_and_check_introduction_text()
        resp = self.start_questionnaire(self.extract_csrf_token(resp.get_data(True)))

        # Add first person
        form_data = MultiDict()
        form_data.add("household-0-first-name", 'John')
        form_data.add("household-1-first-name", 'Jane')
        form_data.add("household-2-first-name", 'Joe')
        form_data.add("household-3-first-name", 'Bran')
        form_data.add("action[save_continue]", "")

        resp = self.get_and_post_with_csrf_token(resp.location, data=form_data, follow_redirects=False)
        composition_summary_page = resp.location

        _, resp_url = self.household_answer_correct(composition_summary_page, 'Yes')
        resp = self.client.get(resp_url)
        content = resp.get_data(True)

        # Check content on summary page
        self.assertRegex(content, 'John')
        self.assertRegex(content, 'Jane')
        self.assertRegex(content, 'Joe')
        self.assertRegex(content, 'Bran')

    def test_can_return_to_composition_and_add_entries(self):
        resp, first_page = self.add_answers()

        form_data = MultiDict()
        form_data.add("csrf_token", self.extract_csrf_token(resp.get_data(True)))
        form_data.add("household-0-first-name", 'John')
        form_data.add("household-1-first-name", 'Jane')
        form_data.add("action[save_continue]", "")

        resp_url, resp = self.postRedirectGet(first_page, form_data)

        resp, resp_url = self.household_answer_correct(resp_url, 'No')

        form_data = MultiDict()
        form_data.add("household-0-first-name", 'John')
        form_data.add("household-1-first-name", 'Jane')
        form_data.add("household-2-first-name", 'Joe')
        form_data.add("household-0-middle-names", '')
        form_data.add("household-1-middle-names", '')
        form_data.add("household-2-middle-names", '')
        form_data.add("household-0-last-name", '')
        form_data.add("household-1-last-name", '')
        form_data.add("household-2-last-name", '')
        form_data.add("action[save_continue]", "")

        resp = self.get_and_post_with_csrf_token(resp_url, form_data, True)
        content = resp.get_data(True)

        self.assertRegex(content, 'John')
        self.assertRegex(content, 'Jane')
        self.assertRegex(content, 'Joe')

        self.assertRegex(resp.get_data(True), 'household-summary')

    def test_composition_complete_progresses_to_summary(self):
        resp, first_page = self.add_answers()

        form_data = MultiDict()
        form_data.add("csrf_token", self.extract_csrf_token(resp.get_data(True)))
        form_data.add("household-0-first-name", 'John')
        form_data.add("household-1-first-name", 'Jane')
        form_data.add("action[save_continue]", "")

        resp_url, resp = self.postRedirectGet(first_page, form_data)

        self.assertRegex(resp_url, 'household-summary')

        form_data = MultiDict()
        form_data.add("csrf_token", self.extract_csrf_token(resp.get_data(True)))
        form_data.add("household-composition-add-another", 'Yes')
        form_data.add("action[save_continue]", "")

        resp = self.client.post(resp_url, data=form_data, follow_redirects=False)
        resp_url = resp.location

        self.assertEqual(resp.status_code, 302)

        self.assertRegex(resp_url, '/summary')

    def test_save_sign_out_with_household_question(self):

        resp, first_page = self.add_answers()

        form_data = MultiDict()
        form_data.add("csrf_token", self.extract_csrf_token(resp.get_data(True)))
        form_data.add("action[save_sign_out]", "")

        resp_url, resp = self.postRedirectGet(first_page, form_data)
        content = resp.get_data(True)
        self.assertRegex(content, 'Your survey has been saved')
        self.assertRegex(resp_url, 'signed-out')

    def remove_answer(self, page):
        # Add first person
        form_data = MultiDict()
        form_data.add("household-0-first-name", 'John')
        form_data.add("household-1-first-name", 'Jane')
        form_data.add("household-2-first-name", 'Joe')
        form_data.add("household-3-first-name", '')
        form_data.add("action[remove_answer]", "1") # Remove Jane.
        resp = self.get_and_post_with_csrf_token(page, data=form_data, follow_redirects=False)

        self.assertEqual(resp.status_code, 200)

        resp = navigate_to_page(self.client, page)
        content = resp.get_data(True)
        form_data.add("household-0-first-name", 'John')
        form_data.add("household-2-first-name", 'Joe')
        form_data.add("household-3-first-name", '')

        self.assertNotRegex(content, 'first-name_1')

    def add_answers(self):
        resp = self.login_and_check_introduction_text()
        resp = self.start_questionnaire(self.extract_csrf_token(resp.get_data(True)))
        first_page = resp.location

        # Add people
        form_data = MultiDict()
        form_data.add("household-0-first-name", 'John')
        form_data.add("household-1-first-name", 'Jane')
        form_data.add("household-2-first-name", 'Joe')
        form_data.add("action[add_answer]", "")
        resp = self.get_and_post_with_csrf_token(resp.location, data=form_data, follow_redirects=False)

        self.assertEqual(resp.status_code, 200)

        content = resp.get_data(True)
        self.assertRegex(content, 'household-0-first-name')
        self.assertRegex(content, 'household-1-first-name')
        self.assertRegex(content, 'household-2-first-name')

        return resp, first_page

    def login_and_check_introduction_text(self):
        self.token = create_token('household_question', 'test')
        resp = self.get_first_page()
        self.check_introduction_text(resp)
        return resp

    def get_first_page(self):
        resp = self.client.get('/session?token=' + self.token.decode(), follow_redirects=True)
        self.assertEqual(resp.status_code, 200)
        return resp

    def check_introduction_text(self, response):
        content = response.get_data(True)
        self.assertRegex(content, '<li>Household questions.</li>')

    def start_questionnaire(self, csrf_token):
        # Go to questionnaire
        post_data = {
            'csrf_token': csrf_token,
            'action[start_questionnaire]': 'Start survey'
        }
        resp = self.client.post(self.INTRODUCTION_PAGE, data=post_data, follow_redirects=False)
        self.assertEqual(resp.status_code, 302)

        return resp

    def household_answer_correct(self, resp_url, answer):
        form_data = MultiDict()
        form_data.add("household-composition-add-another", answer)
        form_data.add("action[save_continue]", "")
        resp = self.get_and_post_with_csrf_token(resp_url, data=form_data, follow_redirects=False)
        resp_url = resp.location
        return resp, resp_url


