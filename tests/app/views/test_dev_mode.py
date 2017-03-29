from app import settings
from tests.integration.integration_test_case import IntegrationTestCase
from app.views.dev_mode import *


class TestDevMode(IntegrationTestCase):
    def setUp(self):
        settings.EQ_DEV_MODE = True
        super().setUp()

    def test_dev_mode(self):
        self.get('/dev')
        self.assertStatusOK()

    def test_dev_flush_mode(self):
        self.get('/dev/flush')
        self.assertStatusOK()

    def test_dev_mode_submission(self):
        # Use the parameters from the dev page
        self.post(url='/dev',
                  post_data={
                      'exp': '1800',
                      'schema': '0_star_wars.json',
                      'period_str': 'May 2016',
                      'period_id': '201605',
                      'collection_exercise_sid': '789',
                      'ru_ref': '12346789012A',
                      'ru_name': 'Apple',
                      'trad_as': 'Apple',
                      'ref_p_start_date': '2016-05-01',
                      'ref_p_end_date': '2016-05-31',
                      'return_by': '2016-06-12',
                      'employment_date': '2016-06-10',
                      'region_code': 'GB-GBN',
                      'user_id': 'test'})

        self.assertStatusOK()

    def test_dev_flush_mode_submission(self):
        self.post(url='/dev/flush',
                  post_data={
                      'schema': '1_0205.json',
                      'collection_exercise_sid': '789',
                      'ru_ref': '12346789012A'})
        self.assertStatusNotFound()

    def test_extract_eq_id_and_form_type_no_form_type(self):
        #Given
        data_to_extract = extract_eq_id_and_form_type('rogueone.json')

        self.assertEqual(data_to_extract, ('rogueone', '-1'))

