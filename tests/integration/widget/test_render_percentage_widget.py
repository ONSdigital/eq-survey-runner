from tests.integration.integration_test_case import IntegrationTestCase


class TestRenderPercentageWidget(IntegrationTestCase):

    def setUp(self):
        super().setUp()
        self.launchSurvey('test', 'percentage')

    def test_percentage_widget_has_icon(self):
        self.assertRegexPage('span.+input\-type\_\_type.+\%\<\/span\>')

    def test_entering_invalid_number_displays_error(self):
        self.post({'answer': 'not a percentage'})
        self.assertStatusOK()
        self.assertInPage('Please enter an integer')

    def test_entering_value_less_than_zero_displays_error(self):
        self.post({'answer': '-50'})
        self.assertStatusOK()
        self.assertInPage('Number cannot be less than zero')

    def test_entering_value_greater_than_one_hundred_displays_error(self):
        self.post({'answer': '150'})
        self.assertStatusOK()
        self.assertInPage('Number cannot be greater than one hundred')

    def test_entering_float_displays_error(self):
        self.post({'answer': '0.5'})
        self.assertStatusOK()
        self.assertInPage('Please enter an integer')

    def test_entering_valid_percentage_redirects_to_summary(self):
        self.post({'answer': '50'})
        self.assertStatusOK()
        self.assertInUrl('summary')
        self.assertRegexPage('summary\_\_answer-text.+\>50\%\<\/div\>')

    def test_description_label_is_rendered(self):
        self.assertInPage('Enter percentage of growth')
