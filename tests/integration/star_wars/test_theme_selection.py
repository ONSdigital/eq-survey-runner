from .test_light_side_path import TestLightSidePath


class TestThemeSelection(TestLightSidePath):
    """
    This test checks that we are using the Star wars theme as
    specified in the test survey schema.
    """


    def test_theme(self):
        """
        Theme Test case
        """

        self.login_and_check_introduction_text()

        first_page = self.start_questionnaire()
        resp = self.navigate_to_page(first_page)

        # We are in the Questionnaire
        content = resp.get_data(True)
        self.assertRegexpMatches(content,
                                 'Theme selected: Star Wars')
