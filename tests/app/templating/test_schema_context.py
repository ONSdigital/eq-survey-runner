from unittest.mock import MagicMock

from app.data_model.answer_store import AnswerStore
from app.templating.schema_context import build_schema_context
from tests.app.framework.survey_runner_test_case import SurveyRunnerTestCase


class TestSchemaContext(SurveyRunnerTestCase):  # pylint: disable=too-many-public-methods

    metadata = {
        'return_by': '2016-10-10',
        'ref_p_start_date': '2016-10-11',
        'ref_p_end_date': '2016-10-12',
        'ru_ref': 'abc123',
        'ru_name': 'Mr Bloggs',
        'trad_as': 'Apple',
        'tx_id': '12345678-1234-5678-1234-567812345678',
        'period_str': 'October 2016',
        'employment_date': '2016-10-09',
        'region_code': 'GB-GBN',
    }

    def setUp(self):
        super().setUp()
        self.answer_store = MagicMock()

    def test_build_schema_context(self):
        aliases = {
            'first_name': {
                'answer_id': 'answer_id',
                'repeats': False,
            },
        }
        answers = []

        self.answer_store.filter = MagicMock(return_value=answers)

        schema_context = build_schema_context(self.metadata, aliases, self.answer_store)

        self.assertTrue('exercise' in schema_context)
        self.assertTrue('answers' in schema_context)

    def test_build_exercise(self):
        aliases = {
            'first_name': {
                'answer_id': 'answer_id',
                'repeats': False,
            },
        }
        answers = []

        self.answer_store.filter = MagicMock(return_value=answers)

        schema_context = build_schema_context(self.metadata, aliases, self.answer_store)

        exercise = schema_context['exercise']
        self.assertEqual('2016-10-11', exercise['start_date'].date().isoformat())
        self.assertEqual('2016-10-12', exercise['end_date'].date().isoformat())
        self.assertEqual('October 2016', exercise['period_str'])
        self.assertEqual('2016-10-09', exercise['employment_date'].date().isoformat())
        self.assertEqual('2016-10-10', exercise['return_by'].date().isoformat())
        self.assertEqual('GB-GBN', exercise['region_code'])

    def test_build_answers(self):
        aliases = {
            'first_name': {
                'answer_id': 'answer_id',
                'repeats': False,
            },
        }
        answers = [{
            'answer_id': 'answer_id',
            'answer_instance': 0,
            'value': 'Joe Bloggs',
        }]

        self.answer_store.filter = MagicMock(return_value=answers)

        schema_context = build_schema_context(self.metadata, aliases, self.answer_store)

        context_answers = schema_context['answers']
        self.assertEqual(len(context_answers), 1)
        self.assertEqual(context_answers['first_name'], 'Joe Bloggs')

    def test_build_schema_context_repeating_answers(self):
        aliases = {
            '_full_name': {
                'answer_id': 'full_name_answer',
                'repeats': True,
            },
        }
        answers = [
            {
                'answer_id': 'full_name_answer',
                'answer_instance': 0,
                'value': 'Person One',
            },
            {
                'answer_id': 'full_name_answer',
                'answer_instance': 1,
                'value': 'Person Two',
            },
            {
                'answer_id': 'full_name_answer',
                'answer_instance': 2,
                'value': 'Person Three',
            }
        ]

        self.answer_store.filter = MagicMock(return_value=answers)

        schema_context = build_schema_context(self.metadata, aliases, self.answer_store)

        context_answers = schema_context['answers']
        self.assertIsInstance(context_answers['_full_name'], list)
        self.assertEqual(len(context_answers['_full_name']), 3)
        self.assertEqual(len(context_answers), 1)

    def test_build_schema_context_single_answer_should_not_return_list(self):
        aliases = {
            'full_name': {
                'answer_id': 'full_name_answer',
                'repeats': False,
            },
        }
        answers = [{
            'answer_id': 'full_name_answer',
            'answer_instance': 0,
            'value': 'Person One',
        }]

        self.answer_store.filter = MagicMock(return_value=answers)

        schema_context = build_schema_context(self.metadata, aliases, self.answer_store)

        context_answers = schema_context['answers']
        self.assertEqual(len(answers), 1)
        self.assertEqual(context_answers['full_name'], 'Person One')

    def test_build_schema_context_no_answers_should_return_empty_alias_value(self):
        aliases = {
            'alias_with_no_matching_answer': {
                'answer_id': 'answer_not_provided',
                'repeats': False,
            },
        }
        answers = []

        self.answer_store.filter = MagicMock(return_value=answers)

        schema_context = build_schema_context(self.metadata, aliases, self.answer_store)

        context_answers = schema_context['answers']
        self.assertEqual(len(context_answers), 1)
        self.assertEqual(context_answers['alias_with_no_matching_answer'], '')

    def test_alias_for_repeating_answer_returns_list(self):
        aliases = {
            'repeating_answer_alias': {
                'answer_id': 'answer_id',
                'repeats': True,
            },
        }
        answers = [{
            'answer_id': 'answer_id',
            'answer_instance': 0,
            'value': 'Some Value',
        }]

        self.answer_store.filter = MagicMock(return_value=answers)

        schema_context = build_schema_context(self.metadata, aliases, self.answer_store)

        context_answers = schema_context['answers']
        self.assertIsInstance(context_answers['repeating_answer_alias'], list)

    def test_alias_for_non_repeating_answer_returns_string(self):
        aliases = {
            'non_repeating_answer_alias': {
                'answer_id': 'answer_id',
                'repeats': False,
            },
        }
        answers = [{
            'answer_id': 'answer_id',
            'answer_instance': 0,
            'value': 'Some Value',
        }]

        self.answer_store.filter = MagicMock(return_value=answers)

        schema_context = build_schema_context(self.metadata, aliases, self.answer_store)

        context_answers = schema_context['answers']
        self.assertIsInstance(context_answers['non_repeating_answer_alias'], str)
        self.assertEqual(context_answers['non_repeating_answer_alias'], 'Some Value')

    def test_maximum_answers_must_be_limited_to_system_max(self):
        aliases = {
            'repeating_answer_alias': {
                'answer_id': 'answer_id',
                'repeats': True,
            },
        }
        answers = [{
            'answer_id': 'answer_id',
            'answer_instance': instance,
            'value': 'Some Value',
        } for instance in range(26)]

        schema_context = build_schema_context(self.metadata, aliases, AnswerStore(answers))

        context_answers = schema_context['answers']
        self.assertEqual(len(context_answers['repeating_answer_alias']), 25)

    def test_respondent_display_name_is_trading_as_when_trading_as_supplied(self):
        schema_context = build_schema_context(self.metadata, {}, self.answer_store)

        self.assertEqual(schema_context['respondent']['trad_as_or_ru_name'], self.metadata['trad_as'])

    def test_respondent_display_name_is_ru_name_as_when_trading_as_not_supplied(self):
        metadata = self.metadata.copy()
        metadata['trad_as'] = None

        schema_context = build_schema_context(metadata, {}, self.answer_store)

        self.assertEqual(schema_context['respondent']['trad_as_or_ru_name'], metadata['ru_name'])

    def test_respondent_display_name_is_ru_name_as_when_trading_as_empty(self):
        metadata = self.metadata.copy()
        metadata['trad_as'] = ""

        schema_context = build_schema_context(metadata, {}, self.answer_store)

        self.assertEqual(schema_context['respondent']['trad_as_or_ru_name'], metadata['ru_name'])

    def test_given_quotes_in_trading_name_when_create_context_then_quotes_are_escaped(self):
        # Given
        metadata = self.metadata.copy()
        metadata['trad_as'] = "\"trading name\""

        # When
        schema_context = build_schema_context(metadata, {}, self.answer_store)

        # Then
        self.assertEqual(schema_context['respondent']['trad_as'], r'\"trading name\"')

    def test_given_backslash_in_trading_name_when_create_context_then_backslash_are_escaped(self):
        # Given
        metadata = self.metadata.copy()
        metadata['trad_as'] = "\\trading name\\"

        # When
        schema_context = build_schema_context(metadata, {}, self.answer_store)

        # Then
        self.assertEqual(schema_context['respondent']['trad_as'], r'\\trading name\\')

    def test_given_quotes_in_ru_name_when_create_context_then_quotes_are_escaped(self):
        # Given
        metadata = self.metadata.copy()
        metadata['ru_name'] = "\"ru name\""

        # When
        schema_context = build_schema_context(metadata, {}, self.answer_store)

        # Then
        self.assertEqual(schema_context['respondent']['ru_name'], r'\"ru name\"')

    def test_given_backslash_in_ru_name_when_create_context_then_backslash_are_escaped(self):
        # Given
        metadata = self.metadata.copy()
        metadata['ru_name'] = "\\ru name\\"

        # When
        schema_context = build_schema_context(metadata, {}, self.answer_store)

        # Then
        self.assertEqual(schema_context['respondent']['ru_name'], r'\\ru name\\')

    def test_given_quotes_in_ru_name_or_trading_name_when_create_context_then_quotes_are_escaped(self):
        # Given
        metadata = self.metadata.copy()
        metadata['ru_name'] = '"ru_name"'
        metadata['trad_as'] = None

        # When
        schema_context = build_schema_context(metadata, {}, self.answer_store)

        # Then
        self.assertEqual(schema_context['respondent']['trad_as_or_ru_name'], r'\"ru_name\"')

    def test_given_backslash_in_ru_name_or_trading_name_when_create_context_then_backslash_are_escaped(self):
        # Given
        metadata = self.metadata.copy()
        metadata['trad_as'] = "\\trading name\\"

        # When
        schema_context = build_schema_context(metadata, {}, self.answer_store)

        # Then
        self.assertEqual(schema_context['respondent']['trad_as_or_ru_name'], r'\\trading name\\')

    def test_given_quotes_in_answers_when_create_context_quotes_then_are_escaped(self):
        aliases = {
            'first_name': {
                'answer_id': 'answer_id',
                'repeats': False,
            },
        }
        answers = [{
            'answer_id': 'answer_id',
            'answer_instance': 0,
            'value': '"',
        }]

        self.answer_store.filter = MagicMock(return_value=answers)

        schema_context = build_schema_context(self.metadata, aliases, self.answer_store)

        context_answers = schema_context['answers']
        self.assertEqual(len(context_answers), 1)
        self.assertEqual(context_answers['first_name'], r'\"')

    def test_given_backslash_in_answers_when_create_context_then_backslash_are_escaped(self):
        aliases = {
            'first_name': {
                'answer_id': 'answer_id',
                'repeats': False,
            },
        }
        answers = [{
            'answer_id': 'answer_id',
            'answer_instance': 0,
            'value': '\\',
        }]

        self.answer_store.filter = MagicMock(return_value=answers)

        schema_context = build_schema_context(self.metadata, aliases, self.answer_store)

        context_answers = schema_context['answers']
        self.assertEqual(len(context_answers), 1)
        self.assertEqual(context_answers['first_name'], r'\\')
