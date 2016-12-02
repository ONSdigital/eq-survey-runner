from app.questionnaire_state.state_answer import StateAnswer
from app.schema.answers.month_year_date_answer import MonthYearDateAnswer
from app.schema.widgets.month_year_date_widget import MonthYearDateWidget

from tests.integration.integration_test_case import IntegrationTestCase

from app import create_app


class TestRenderMonthYearDateAnswer(IntegrationTestCase):

    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_month_year_date_answer_mandatory_without_place_holder(self):
        user_answer = '2/2016'
        is_mandatory = True
        response = self.render_widget(user_answer, is_mandatory)
        self.assertRegexpMatches(response, 'February')
        self.assertRegexpMatches(response, '2016')
        self.assertRegexpMatches(response, 'Select month')

    def test_month_year_date_answer_mandatory_with_place_holder(self):
        user_answer = None
        is_mandatory = True
        response = self.render_widget(user_answer, is_mandatory)
        self.assertRegexpMatches(response, 'Select month')

    def test_month_year_date_answer_non_mandatory_with_place_holder(self):
        user_answer = '2/2016'
        is_mandatory = False
        response = self.render_widget(user_answer, is_mandatory)
        self.assertRegexpMatches(response, 'Select month')

    def test_month_year_date_answer_none_input(self):
        user_answer = None
        self.render_widget(user_answer, False)

    def render_widget(self, user_answer, is_mandatory):
        month_year_date_widget = MonthYearDateWidget('1234')
        month_year_date_answer = MonthYearDateAnswer()

        answer_state = StateAnswer('1', month_year_date_answer)
        answer_state.schema_item.label = 'Date month year Label'
        answer_state.schema_item.mandatory = is_mandatory
        answer_state.schema_item.type = "DateMonthYear"
        answer_state.input = user_answer

        response = month_year_date_widget.render(answer_state)
        self.assertRegexpMatches(response, 'input-1234-month')
        self.assertRegexpMatches(response, 'input-1234-year')
        self.assertRegexpMatches(response, 'Date month year Label')
        return response
