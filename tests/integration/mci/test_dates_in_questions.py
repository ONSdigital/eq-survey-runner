from tests.integration.integration_test_case import IntegrationTestCase


class TestHappyPath(IntegrationTestCase):

    def test_try_date_203(self):
        self.try_date('1', '0203')

    def test_try_another_data_203(self):
        self.try_another_date('1', '0203')

    def test_try_date_205(self):
        self.try_date('1', '0205')

    def test_try_another_date_205(self):
        self.try_another_date('1', '0205')

    def try_date(self, eq_id, form_type_id):
        self.launchSurvey(eq_id, form_type_id,
                          ref_p_start_date='2016-04-01',
                          ref_p_end_date='2016-04-30')

        # We proceed to the questionnaire
        self.post(action='start_questionnaire')

        # We are in the Questionnaire
        self.assertInPage('>Monthly Business Survey - Retail Sales Index</')
        self.assertInPage('What are the dates of the sales period you are reporting for?')
        self.assertInPage('1 April 2016')
        self.assertInPage('30 April 2016')

    def try_another_date(self, form_type_id, eq_id):
        # Try another date
        self.launchSurvey(form_type_id, eq_id,
                          ref_p_start_date='2017-08-01',
                          ref_p_end_date='2017-08-31')

        # We proceed to the questionnaire
        self.post(action='start_questionnaire')

        # We are in the Questionnaire
        self.assertInPage('>Monthly Business Survey - Retail Sales Index</')
        self.assertInPage('What are the dates of the sales period you are reporting for?')
        self.assertInPage('1 August 2017')
        self.assertInPage('31 August 2017')
