from app import settings
from app.views.dev_mode import extract_eq_id_and_form_type

from tests.integration.integration_test_case import IntegrationTestCase


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

    #Valid inputs
    def test_extract_eq_id_and_form_type(self):
        data_to_extract = extract_eq_id_and_form_type('census_household.json')
        self.assertEqual(data_to_extract, ('census', 'household'))

    def test_extract_eq_id_and_form_type_more_than_one_underscore(self):
        data_to_extract = extract_eq_id_and_form_type('0_rogue_one.json')
        self.assertEqual(data_to_extract, ('0', 'rogue_one'))

    def test_extract_eq_id_and_form_type_multiple_characters(self):
        data_to_extract = extract_eq_id_and_form_type('abc123_456xyz.json')
        self.assertEqual(data_to_extract, ('abc123', '456xyz'))

    #Not valid inputs
    def test_extract_eq_id_and_form_type_no_underscore(self):
        with self.assertRaises(ValueError) as ite:
            extract_eq_id_and_form_type('rogueone.json')
        self.assertEqual(('Schema filename incorrect format: %s', 'rogueone.json'), ite.exception.args)

    def test_extract_eq_id_and_form_type_no_underscore_no_extension(self):
        with self.assertRaises(ValueError) as ite:
            extract_eq_id_and_form_type('rogueone')
        self.assertEqual(('Schema filename incorrect format: %s', 'rogueone'), ite.exception.args)

    def test_extract_eq_id_and_form_type_blank(self):
        with self.assertRaises(ValueError) as ite:
            extract_eq_id_and_form_type('')
        self.assertEqual(('Schema filename incorrect format: %s', ''), ite.exception.args)

    def test_extract_eq_id_and_form_type_none(self):
        with self.assertRaises(TypeError):
            extract_eq_id_and_form_type(None)

    def test_extract_eq_id_and_form_type_wrong_extension(self):
        with self.assertRaises(ValueError) as ite:
            extract_eq_id_and_form_type('census_household.txt')
        self.assertEqual(('Schema filename incorrect format: %s', 'census_household.txt'), ite.exception.args)

    def test_extract_eq_id_and_form_type_format_backwards(self):
        with self.assertRaises(ValueError) as ite:
            extract_eq_id_and_form_type('abc.json_123')
        self.assertEqual(('Schema filename incorrect format: %s', 'abc.json_123'), ite.exception.args)
