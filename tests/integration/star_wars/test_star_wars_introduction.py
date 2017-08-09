from tests.integration.star_wars.star_wars_tests import StarWarsTestCase


class TestStarWarsIntroduction(StarWarsTestCase):

    def test_introduction(self):
        self.launchSurvey()

        # Landing page tests
        self.assertInPage('Star Wars')
        self.assertInPage('If actual figures are not available, please provide informed estimates.')
        self.assertInPage('>Start survey<')
        self.assertRegexPage('(?s)Trading as.*?Integration Tests')
        self.assertRegexPage('(?s)Business name.*?Integration Testing')
        self.assertRegexPage('(?s)PLEASE SUBMIT BY.*?6 May 2016')
        self.assertRegexPage('(?s)PERIOD.*?1 April 2016.*?30 April 2016')

        # Legal checks
        self.assertInPage('All information you provide is strictly confidential')

        # Information to provide
        self.assertInPage('Total Yearly cost of Rebel Alliance')
        self.assertInPage("Yoda's siblings")
