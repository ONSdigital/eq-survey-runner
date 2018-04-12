from app.data_model.answer_store import AnswerStore
from app.questionnaire.location import Location
from app.templating.schema_context import build_schema_context
from tests.app.app_context_test_case import AppContextTestCase


class TestSchemaContext(AppContextTestCase):  # pylint: disable=too-many-public-methods

    metadata = {
        'return_by': '2016-10-20',
        'ref_p_start_date': '2016-10-13',
        'ref_p_end_date': '2016-10-14',
        'ru_ref': 'abc123',
        'ru_name': 'Mr Bloggs',
        'trad_as': 'Apple',
        'tx_id': '12345678-1234-5678-1234-567812345678',
        'period_str': 'October 2016',
        'employment_date': '2016-10-19',
        'region_code': 'GB-GBN',
    }

    def setUp(self):
        super().setUp()
        self.answer_store = AnswerStore([])

        self.routing_path = [Location('group1', 0, 'block1')]

    def test_build_schema_context(self):
        aliases = {
            'first_name': {
                'answer_id': 'answer_id',
                'repeats': False,
            },
        }
        answers = []

        answer_ids_on_path = []

        schema_context = build_schema_context(self.metadata, aliases, AnswerStore(answers), answer_ids_on_path)

        self.assertTrue('metadata' in schema_context)
        self.assertTrue('answers' in schema_context)

    def test_build_metadata(self):
        aliases = {
            'first_name': {
                'answer_id': 'answer_id',
                'repeats': False,
            },
        }
        answers = []

        answer_ids_on_path = []

        schema_context = build_schema_context(self.metadata, aliases, AnswerStore(answers), answer_ids_on_path)

        metadata = schema_context['metadata']
        self.assertEqual('2016-10-13', metadata['ref_p_start_date'])
        self.assertEqual('2016-10-14', metadata['ref_p_end_date'])
        self.assertEqual('October 2016', metadata['period_str'])
        self.assertEqual('2016-10-19', metadata['employment_date'])
        self.assertEqual('2016-10-20', metadata['return_by'])
        self.assertEqual('GB-GBN', metadata['region_code'])

    def test_build_answers(self):
        aliases = {
            'first_name': {
                'answer_id': 'answer_id',
                'repeats': False,
            },
        }
        answers = [{
            'group_id': 'group1',
            'group_instance': 0,
            'block_id': 'block1',
            'answer_id': 'answer_id',
            'answer_instance': 0,
            'value': 'Joe Bloggs',
        }]

        answer_ids_on_path = ['answer_id']

        schema_context = build_schema_context(self.metadata, aliases, AnswerStore(answers), answer_ids_on_path)

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
                'group_id': 'group1',
                'group_instance': 0,
                'block_id': 'block1',
                'answer_id': 'full_name_answer',
                'answer_instance': 0,
                'value': 'Person One',
            },
            {
                'group_id': 'group1',
                'group_instance': 0,
                'block_id': 'block1',
                'answer_id': 'full_name_answer',
                'answer_instance': 1,
                'value': 'Person Two',
            },
            {
                'group_id': 'group1',
                'group_instance': 0,
                'block_id': 'block1',
                'answer_id': 'full_name_answer',
                'answer_instance': 2,
                'value': 'Person Three',
            }
        ]

        answer_ids_on_path = ['full_name_answer']

        schema_context = build_schema_context(self.metadata, aliases, AnswerStore(answers), answer_ids_on_path)

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
            'group_id': 'group1',
            'group_instance': 0,
            'block_id': 'block1',
            'answer_id': 'full_name_answer',
            'answer_instance': 0,
            'value': 'Person One',
        }]

        answer_ids_on_path = ['full_name_answer']

        schema_context = build_schema_context(self.metadata, aliases, AnswerStore(answers), answer_ids_on_path)

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

        answer_ids_on_path = []

        schema_context = build_schema_context(self.metadata, aliases, AnswerStore(answers), answer_ids_on_path)

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
            'group_id': 'group1',
            'group_instance': 0,
            'block_id': 'block1',
            'answer_id': 'answer_id',
            'answer_instance': 0,
            'value': 'Some Value',
        }]

        answer_ids_on_path = ['answer_id']

        schema_context = build_schema_context(self.metadata, aliases, AnswerStore(answers), answer_ids_on_path)

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
            'group_id': 'group1',
            'group_instance': 0,
            'block_id': 'block1',
            'answer_id': 'answer_id',
            'answer_instance': 0,
            'value': 'Some Value',
        }]

        answer_ids_on_path = ['answer_id']

        schema_context = build_schema_context(self.metadata, aliases, AnswerStore(answers), answer_ids_on_path)

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
            'group_id': 'group1',
            'group_instance': 0,
            'block_id': 'block1',
            'answer_id': 'answer_id',
            'answer_instance': instance,
            'value': 'Some Value',
        } for instance in range(26)]

        answer_ids_on_path = ['answer_id']

        schema_context = build_schema_context(self.metadata, aliases, AnswerStore(answers), answer_ids_on_path)

        context_answers = schema_context['answers']
        self.assertEqual(len(context_answers['repeating_answer_alias']), 25)

    def test_metadata_display_name_is_trad_as_when_trad_as_supplied(self):
        answer_ids_on_path = []
        schema_context = build_schema_context(self.metadata, {}, self.answer_store, answer_ids_on_path)

        self.assertEqual(schema_context['metadata']['trad_as_or_ru_name'], self.metadata['trad_as'])

    def test_metadata_display_name_is_ru_name_as_when_trad_as_not_supplied(self):
        metadata = self.metadata.copy()
        metadata['trad_as'] = None

        answer_ids_on_path = []

        schema_context = build_schema_context(metadata, {}, self.answer_store, answer_ids_on_path)

        self.assertEqual(schema_context['metadata']['trad_as_or_ru_name'], metadata['ru_name'])

    def test_metadata_display_name_is_ru_name_as_when_trad_as_empty(self):
        metadata = self.metadata.copy()
        metadata['trad_as'] = ''

        answer_ids_on_path = []

        schema_context = build_schema_context(metadata, {}, self.answer_store, answer_ids_on_path)

        self.assertEqual(schema_context['metadata']['trad_as_or_ru_name'], metadata['ru_name'])

    def test_given_quotes_in_trading_name_when_create_context_then_quotes_are_html_encoded(self):
        # Given
        metadata = self.metadata.copy()
        metadata['trad_as'] = '\"trading name\"'

        answer_ids_on_path = []

        # When
        schema_context = build_schema_context(metadata, {}, self.answer_store, answer_ids_on_path)

        # Then
        self.assertEqual(schema_context['metadata']['trad_as'], r'&#34;trading name&#34;')

    def test_given_backslash_in_trading_name_when_create_context_then_backslash_are_escaped(self):
        # Given
        metadata = self.metadata.copy()
        metadata['trad_as'] = '\\trading name\\'

        answer_ids_on_path = []

        # When
        schema_context = build_schema_context(metadata, {}, self.answer_store, answer_ids_on_path)

        # Then
        self.assertEqual(schema_context['metadata']['trad_as'], r'\\trading name\\')

    def test_given_quotes_in_ru_name_when_create_context_then_quotes_are_html_encoded(self):
        # Given
        metadata = self.metadata.copy()
        metadata['ru_name'] = '\"ru name\"'

        answer_ids_on_path = []

        # When
        schema_context = build_schema_context(metadata, {}, self.answer_store, answer_ids_on_path)

        # Then
        self.assertEqual(schema_context['metadata']['ru_name'], r'&#34;ru name&#34;')

    def test_given_backslash_in_ru_name_when_create_context_then_backslash_are_escaped(self):
        # Given
        metadata = self.metadata.copy()
        metadata['ru_name'] = '\\ru name\\'

        answer_ids_on_path = []

        # When
        schema_context = build_schema_context(metadata, {}, self.answer_store, answer_ids_on_path)

        # Then
        self.assertEqual(schema_context['metadata']['ru_name'], r'\\ru name\\')

    def test_given_quotes_in_ru_name_or_trading_name_when_create_context_then_quotes_are_html_encoded(self):
        # Given
        metadata = self.metadata.copy()
        metadata['ru_name'] = '\"ru_name\"'
        metadata['trad_as'] = None

        answer_ids_on_path = []

        # When
        schema_context = build_schema_context(metadata, {}, self.answer_store, answer_ids_on_path)

        # Then
        self.assertEqual(schema_context['metadata']['trad_as_or_ru_name'], r'&#34;ru_name&#34;')

    def test_given_backslash_in_ru_name_or_trading_name_when_create_context_then_backslash_are_escaped(self):
        # Given
        metadata = self.metadata.copy()
        metadata['trad_as'] = '\\trading name\\'

        answer_ids_on_path = []

        # When
        schema_context = build_schema_context(metadata, {}, self.answer_store, answer_ids_on_path)

        # Then
        self.assertEqual(schema_context['metadata']['trad_as_or_ru_name'], r'\\trading name\\')

    def test_given_quotes_in_answers_when_create_context_quotes_then_are_html_encoded(self):
        aliases = {
            'first_name': {
                'answer_id': 'answer_id',
                'repeats': False,
            },
        }
        answers = [{
            'group_id': 'group1',
            'group_instance': 0,
            'block_id': 'block1',
            'answer_id': 'answer_id',
            'answer_instance': 0,
            'value': '"',
        }]

        answer_ids_on_path = ['answer_id']

        schema_context = build_schema_context(self.metadata, aliases, AnswerStore(answers), answer_ids_on_path)

        context_answers = schema_context['answers']
        self.assertEqual(len(context_answers), 1)
        self.assertEqual(context_answers['first_name'], r'&#34;')

    def test_given_backslash_in_answers_when_create_context_then_backslash_are_escaped(self):
        aliases = {
            'first_name': {
                'answer_id': 'answer_id',
                'repeats': False,
            },
        }
        answers = [{
            'group_id': 'group1',
            'group_instance': 0,
            'block_id': 'block1',
            'answer_id': 'answer_id',
            'answer_instance': 0,
            'value': '\\',
        }]

        answer_ids_on_path = ['answer_id']

        schema_context = build_schema_context(self.metadata, aliases, AnswerStore(answers), answer_ids_on_path)

        context_answers = schema_context['answers']
        self.assertEqual(len(context_answers), 1)
        self.assertEqual(context_answers['first_name'], r'\\')

    def test_build_answers_excludes_answers_not_in_routing_path(self):
        aliases = {
            'first_name': {
                'answer_id': 'first_name',
                'repeats': False,
            },
            'last_name': {
                'answer_id': 'last_name',
                'repeats': False,
            },
        }
        answers = [
            {
                'group_id': 'group1',
                'group_instance': 0,
                'block_id': 'block1',
                'answer_id': 'first_name',
                'answer_instance': 0,
                'value': 'Joe',
            },
            {
                'group_id': 'group2',
                'group_instance': 0,
                'block_id': 'block2',
                'answer_id': 'last_name',
                'answer_instance': 0,
                'value': 'Bloggs',
            }
        ]

        answer_ids_on_path = ['first_name']

        schema_context = build_schema_context(self.metadata, aliases, AnswerStore(answers), answer_ids_on_path)

        context_answers = schema_context['answers']
        self.assertEqual(len(context_answers), 2)
        self.assertEqual(context_answers['first_name'], 'Joe')
        self.assertEqual(context_answers['last_name'], '')
