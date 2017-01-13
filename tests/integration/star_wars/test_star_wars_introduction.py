from tests.integration.star_wars.star_wars_tests import StarWarsTestCase


class TestStarWarsIntroduction(StarWarsTestCase):

    def test_introduction(self):
        response = self.login()

        # Landing page tests
        content = response.get_data(True)
        self.assertIn('<title>Introduction</title>', content)
        self.assertIn('Star Wars', content)
        self.assertIn('If actual figures are not available, please provide informed estimates.', content)
        self.assertIn('Legal Information', content)
        self.assertIn('>Start survey<', content)
        self.assertRegex(content, '(?s)Trading as.*?Integration Tests')
        self.assertRegex(content, '(?s)Business name.*?MCI Integration Testing')
        self.assertRegex(content, '(?s)PLEASE SUBMIT BY.*?6 May 2016')
        self.assertRegex(content, '(?s)PERIOD.*?1 April 2016.*?30 April 2016')
        self.assertIn('questionnaire by 6 May 2016, penalties may be incurred', content)

        # Legal checks
        self.assertIn('We will treat your data securely and confidentially', content)
        self.assertIn('You are required to complete this questionnaire', content)

        # Information to provide
        self.assertIn('Total Yearly cost of Rebel Alliance', content)
        self.assertIn('Yoda&#39;s siblings', content)
