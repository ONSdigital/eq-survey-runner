from werkzeug.datastructures import MultiDict

from tests.integration.create_token import create_token
from tests.integration.integration_test_case import IntegrationTestCase


class TestRenderPercentageWidget(IntegrationTestCase):

    def setUp(self):
        super().setUp()

        self.token = create_token('percentage', 'test')
        self.client.get('/session?token=' + self.token.decode(), follow_redirects=True)
        resp = self.client.post('/questionnaire/test/percentage/789/introduction',
                                data={'action[start_questionnaire]': 'Start Questionnaire'},
                                follow_redirects=False)
        self.first_page = resp.location

    def test_percentage_widget_has_icon(self):
        # Given
        resp = self.client.get(self.first_page)
        percent_regex = 'span.+input\-type\_\_type.+\%\<\/span\>'

        # When
        body = resp.get_data(True)

        # Then
        self.assertRegex(body, percent_regex)

    def test_entering_invalid_number_displays_error(self):
        # Given
        form_data = self.create_form_data('not a percentage')

        # When
        self.client.get(self.first_page)
        resp = self.client.post(self.first_page, data=form_data, follow_redirects=True)

        # Then
        self.assertEqual(resp.status_code, 200)
        self.assertRegex(resp.get_data(True), 'Please enter an integer')

    def test_entering_value_less_than_zero_displays_error(self):
        # Given
        form_data = self.create_form_data('-50')

        # When
        self.client.get(self.first_page)
        resp = self.client.post(self.first_page, data=form_data, follow_redirects=True)

        # Then
        self.assertEqual(resp.status_code, 200)
        self.assertRegex(resp.get_data(True), 'Number cannot be less than zero')

    def test_entering_value_greater_than_one_hundred_displays_error(self):
        # Given
        form_data = self.create_form_data('150')

        # When
        self.client.get(self.first_page)
        resp = self.client.post(self.first_page, data=form_data, follow_redirects=True)

        # Then
        self.assertEqual(resp.status_code, 200)
        self.assertRegex(resp.get_data(True), 'Number cannot be greater than one hundred')

    def test_entering_float_displays_error(self):
        # Given
        form_data = self.create_form_data('0.5')

        # When
        self.client.get(self.first_page)
        resp = self.client.post(self.first_page, data=form_data, follow_redirects=True)

        # Then
        self.assertEqual(resp.status_code, 200)
        self.assertRegex(resp.get_data(True), 'Please enter an integer')

    def test_entering_valid_percentage_redirects_to_next_page(self):
        # Given
        form_data = self.create_form_data('50')

        # When
        self.client.get(self.first_page)
        resp = self.client.post(self.first_page, data=form_data, follow_redirects=True)

        # Then
        answer_summary_regex = 'summary\_\_answer-text.+\>50\%\<\/div\>'
        self.assertEqual(resp.status_code, 200)
        self.assertRegex(resp.get_data(True), answer_summary_regex)

    def test_description_label_is_rendered(self):
        resp = self.client.get(self.first_page)
        self.assertIn('Enter percentage of growth', resp.get_data(True))

    @staticmethod
    def create_form_data(percentage):
        form_data = MultiDict()
        form_data.add("answer", percentage)
        form_data.add("action[save_continue]", '')
        return form_data
