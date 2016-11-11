from mock import Mock

from app.templating.schema_context import build_schema_context
from tests.app.framework.sr_unittest import SurveyRunnerTestCase


class TestMetadataContext(SurveyRunnerTestCase):

    metadata = {'return_by': '2016-10-10',
                'ref_p_start_date': '2016-10-11',
                'ref_p_end_date': '2016-10-12',
                'ru_ref': 'abc123',
                'ru_name': 'Mr Bloggs',
                'trad_as': 'Apple',
                'tx_id': '12345678-1234-5678-1234-567812345678',
                'period_str': '201610',
                'employment_date': '2016-10-09',
                'region_code': 'GB-GBN',
                }

    def test_build_schema_context(self):
        aliases = {'first_name': 'answer_id'}
        answers = Mock()

        schema_context = build_schema_context(self.metadata, aliases, answers)

        self.assertTrue('exercise' in schema_context)
        self.assertTrue('answers' in schema_context)

    def test_build_exercise(self):
        aliases = {'first_name': 'answer_id'}
        answers = Mock()

        schema_context = build_schema_context(self.metadata, aliases, answers)

        exercise = schema_context['exercise']
        self.assertEqual('2016-10-11', exercise['start_date'].date().isoformat())
        self.assertEqual('2016-10-12', exercise['end_date'].date().isoformat())
        self.assertEqual('2016-10-09', exercise['employment_date'].date().isoformat())
        self.assertEqual('2016-10-10', exercise['return_by'].date().isoformat())
        self.assertEqual('GB-GBN', exercise['region_code'])

    def test_build_answers(self):
        aliases = {'first_name': 'answer_id'}
        answers = {'answer_id': 'Joe Bloggs'}

        schema_context = build_schema_context(self.metadata, aliases, answers)

        answers = schema_context['answers']
        self.assertEqual(len(answers), 1)
        self.assertEqual(answers['first_name'], 'Joe Bloggs')
