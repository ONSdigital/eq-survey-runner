from tests.integration.navigation import navigate_to_page
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

        self.login()

        first_page = self.start_questionnaire_and_navigate_routing()
        resp = navigate_to_page(self.client, first_page)

        # We are in the Questionnaire
        content = resp.get_data(True)
        self.assertRegex(content, 'Theme selected: Star Wars')
