from flask import g

from app.templating.metadata_context import build_metadata_context
from app.utilities.schema import load_schema_from_params
from tests.app.app_context_test_case import AppContextTestCase

PROPERTIES = 'user_id', 'collection_exercise_sid',\
             'period_id', 'ru_ref', 'ru_name', 'trad_as',\
             'region_code', 'period_str'


class TestMetadataContext(AppContextTestCase):

    def setUp(self):
        super().setUp()

        self.jwt = {
            'user_id': '1',
            'form_type': 'schema_context',
            'collection_exercise_sid': 'test-sid',
            'eq_id': 'test',
            'period_id': '3',
            'period_str': '2016-01-14',
            'ref_p_start_date': '2016-02-22',
            'ref_p_end_date': '2016-03-30',
            'ru_ref': '178324',
            'ru_name': 'Apple',
            'trad_as': 'Apple',
            'return_by': '2016-07-17',
            'tx_id': '4ec3aa9e-e8ac-4c8d-9793-6ed88b957c2f',
        }

        g.schema = load_schema_from_params(self.jwt['eq_id'], self.jwt['form_type'])

    def test_build_metadata_context(self):
        metadata_context = build_metadata_context(self.jwt)

        self.assertIsNotNone(metadata_context)
        self.assertEqual('2016-07-17', metadata_context['return_by'])
        self.assertEqual('2016-02-22', metadata_context['ref_p_start_date'])
        self.assertEqual('2016-03-30', metadata_context['ref_p_end_date'])
        self.assertIsNone(metadata_context.get('employment_date'))
        self.assertIsNone(metadata_context.get('region_code'))
        self.assertEqual(self.jwt['period_str'], metadata_context['period_str'])
        self.assertEqual(self.jwt['ru_ref'], metadata_context['ru_ref'])
        self.assertEqual(self.jwt['ru_name'], metadata_context['ru_name'])
        self.assertEqual(self.jwt['trad_as'], metadata_context['trad_as'])

    def test_defend_against_XSS_attack(self):
        jwt = self.jwt.copy()
        escaped_bad_characters = r'&lt;&#34;&gt;\\'

        for key in PROPERTIES:
            jwt[key] = '<">\\'

        metadata_context = build_metadata_context(jwt)

        self.assertEqual(escaped_bad_characters, metadata_context['user_id'])
        self.assertEqual(escaped_bad_characters, metadata_context['period_id'])
        self.assertEqual(escaped_bad_characters, metadata_context['period_str'])
        self.assertEqual(escaped_bad_characters, metadata_context['ru_ref'])
        self.assertEqual(escaped_bad_characters, metadata_context['ru_name'])
        self.assertEqual(escaped_bad_characters, metadata_context['trad_as'])
        self.assertEqual(escaped_bad_characters, metadata_context['trad_as_or_ru_name'])
        self.assertEqual(escaped_bad_characters, metadata_context['region_code'])
        self.assertEqual(escaped_bad_characters, metadata_context['collection_id'])
