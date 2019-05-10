from tests.integration.integration_test_case import IntegrationTestCase


class TestRenderPercentageWidget(IntegrationTestCase):

    def setUp(self):
        super().setUp()
        self.launchSurvey('test', 'percentage')

    def test_percentage_widget_has_icon(self):
        self.assertInSelectorCSS('%', 'abbr', {'class': 'input-type__type'})

    def test_entering_invalid_number_displays_error(self):
        self.post({'answer': 'not a percentage'})
        self.assertStatusOK()
        self.assertInBody('Enter a number.')

    def test_entering_value_less_than_zero_displays_error(self):
        self.post({'answer': '-50'})
        self.assertStatusOK()
        self.assertInBody('Enter an answer more than or equal to 0')

    def test_entering_value_greater_than_one_hundred_displays_error(self):
        self.post({'answer': '150'})
        self.assertStatusOK()
        self.assertInBody('Enter an answer less than or equal to 100')

    def test_entering_float_displays_error(self):
        self.post({'answer': '0.5'})
        self.assertStatusOK()
        self.assertInBody('Enter a whole number.')

    def test_entering_valid_percentage_redirects_to_summary(self):
        self.post({'answer': '50'})
        self.assertStatusOK()
        self.assertInUrl('summary')

    def test_description_label_is_rendered(self):
        self.assertInBody('Enter percentage of growth')
