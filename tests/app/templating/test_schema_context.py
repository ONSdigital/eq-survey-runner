import mock
from flask import g
from app.data_model.answer_store import AnswerStore
from app.questionnaire.location import Location
from app.templating.schema_context import build_schema_context
from app.utilities.schema import load_schema_from_params
from tests.app.app_context_test_case import AppContextTestCase


class TestSchemaContext(AppContextTestCase):  # pylint: disable=too-many-public-methods

    metadata = {
        'user_id': 'Steve',
        'ref_p_start_date': '2016-10-13',
        'ref_p_end_date': '2016-10-14',
        'ru_ref': 'abc123',
        'ru_name': 'Mr Bloggs',
        'trad_as': 'Apple',
        'tx_id': '12345678-1234-5678-1234-567812345678',
        'period_id': '201610',
        'employment_date': '2016-10-19',
        'eq_id': 'test',
        'form_type': 'schema_context'
    }

    def setUp(self):
        super().setUp()
        g.schema = load_schema_from_params(self.metadata['eq_id'], self.metadata['form_type'])

        self.answer_store = AnswerStore([])

        self.routing_path = [Location('group1', 0, 'block1')]

        self._get_is_repeating_answer_patcher = mock.patch('app.templating.schema_context._get_is_repeating_answer', return_value=False)
        self._get_is_repeating_answer = self._get_is_repeating_answer_patcher.start()

        self._get_answer_is_in_repeating_group_patcher = mock.patch(
            'app.templating.schema_context._get_answer_is_in_repeating_group',
            return_value=False)
        self._get_answer_is_in_repeating_group = self._get_answer_is_in_repeating_group_patcher.start()

    def tearDown(self):
        self._get_is_repeating_answer_patcher.stop()
        self._get_answer_is_in_repeating_group_patcher.stop()
        super().tearDown()

    def test_build_schema_context(self):
        schema_context = build_schema_context(self.metadata, AnswerStore([]), [])

        self.assertIn('metadata', schema_context)
        self.assertIn('answers', schema_context)

    def test_build_schema_metadata(self):
        schema_context = build_schema_context(self.metadata, AnswerStore([]), [])

        metadata = schema_context['metadata']
        self.assertEqual('2016-10-13', metadata['ref_p_start_date'])
        self.assertEqual('2016-10-14', metadata['ref_p_end_date'])
        self.assertEqual('201610', metadata['period_id'])
        self.assertEqual('2016-10-19', metadata['employment_date'])
        self.assertEqual('Steve', metadata['user_id'])

    def test_build_answers(self):
        answers = [{
            'group_id': 'group1',
            'group_instance': 0,
            'block_id': 'block1',
            'answer_id': 'first_name',
            'answer_instance': 0,
            'value': 'Joe Bloggs',
        }]

        answer_ids_on_path = ['first_name']

        schema_context = build_schema_context(self.metadata, AnswerStore(answers), answer_ids_on_path)

        context_answers = schema_context['answers']
        self.assertEqual(len(context_answers), 1)
        self.assertEqual(context_answers['first_name'], 'Joe Bloggs')

    def test_build_schema_context_repeating_answers(self):
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

        self._get_is_repeating_answer.return_value = True
        schema_context = build_schema_context(self.metadata, AnswerStore(answers), answer_ids_on_path)

        context_answers = schema_context['answers']
        self.assertIsInstance(context_answers['full_name_answer'], list)
        self.assertEqual(len(context_answers['full_name_answer']), 3)
        self.assertEqual(len(context_answers), 1)

    def test_build_schema_context_single_answer_should_not_return_list(self):
        answers = [{
            'group_id': 'group1',
            'group_instance': 0,
            'block_id': 'block1',
            'answer_id': 'full_name_answer',
            'answer_instance': 0,
            'value': 'Person One',
        }]

        answer_ids_on_path = ['full_name_answer']

        schema_context = build_schema_context(self.metadata, AnswerStore(answers), answer_ids_on_path)

        context_answers = schema_context['answers']
        self.assertEqual(len(answers), 1)
        self.assertEqual(context_answers['full_name_answer'], 'Person One')

    def test_alias_for_repeating_answer_returns_list(self):
        answers = [{
            'group_id': 'group1',
            'group_instance': 0,
            'block_id': 'block1',
            'answer_id': 'repeating_answer_id',
            'answer_instance': 0,
            'value': 'Some Value',
        }]

        answer_ids_on_path = ['repeating_answer_id']

        self._get_is_repeating_answer.return_value = True
        schema_context = build_schema_context(self.metadata, AnswerStore(answers), answer_ids_on_path)

        context_answers = schema_context['answers']
        self.assertIsInstance(context_answers['repeating_answer_id'], list)

    def test_alias_for_non_repeating_answer_returns_string(self):
        answers = [{
            'group_id': 'group1',
            'group_instance': 0,
            'block_id': 'block1',
            'answer_id': 'non_repeating_answer_id',
            'answer_instance': 0,
            'value': 'Some Value',
        }]

        answer_ids_on_path = ['non_repeating_answer_id']

        schema_context = build_schema_context(self.metadata, AnswerStore(answers), answer_ids_on_path)

        context_answers = schema_context['answers']
        self.assertIsInstance(context_answers['non_repeating_answer_id'], str)
        self.assertEqual(context_answers['non_repeating_answer_id'], 'Some Value')

    def test_alias_for_answer_in_repeating_group_returns_list(self):
        answers = [{
            'group_id': 'group1',
            'group_instance': 0,
            'block_id': 'block1',
            'answer_id': 'answer_id',
            'answer_instance': 0,
            'value': 'Some Value',
        }]

        answer_ids_on_path = ['answer_id']

        self._get_answer_is_in_repeating_group.return_value = True
        schema_context = build_schema_context(self.metadata,
                                              AnswerStore(answers),
                                              answer_ids_on_path)

        context_answers = schema_context['answers']
        self.assertIsInstance(context_answers['answer_id'], list)

    def test_maximum_answers_must_be_limited_to_system_max(self):
        answers = [{
            'group_id': 'group1',
            'group_instance': 0,
            'block_id': 'block1',
            'answer_id': 'repeating_answer_id',
            'answer_instance': instance,
            'value': 'Some Value',
        } for instance in range(26)]

        answer_ids_on_path = ['repeating_answer_id']

        self._get_is_repeating_answer.return_value = True
        schema_context = build_schema_context(self.metadata, AnswerStore(answers), answer_ids_on_path)

        context_answers = schema_context['answers']
        self.assertEqual(len(context_answers['repeating_answer_id']), 25)

    def test_metadata_display_name_is_trad_as_when_trad_as_supplied(self):
        answer_ids_on_path = []
        schema_context = build_schema_context(self.metadata, self.answer_store, answer_ids_on_path)

        self.assertEqual(schema_context['metadata']['trad_as_or_ru_name'], self.metadata['trad_as'])

    def test_metadata_display_name_is_ru_name_as_when_trad_as_not_supplied(self):
        metadata = self.metadata.copy()
        metadata['trad_as'] = None

        answer_ids_on_path = []

        schema_context = build_schema_context(metadata, self.answer_store, answer_ids_on_path)

        self.assertEqual(schema_context['metadata']['trad_as_or_ru_name'], metadata['ru_name'])

    def test_metadata_display_name_is_ru_name_as_when_trad_as_empty(self):
        metadata = self.metadata.copy()
        metadata['trad_as'] = ''

        answer_ids_on_path = []

        schema_context = build_schema_context(metadata, self.answer_store, answer_ids_on_path)

        self.assertEqual(schema_context['metadata']['trad_as_or_ru_name'], metadata['ru_name'])

    def test_given_quotes_in_trading_name_when_create_context_then_quotes_are_html_encoded(self):
        # Given
        metadata = self.metadata.copy()
        metadata['trad_as'] = '\"trading name\"'

        answer_ids_on_path = []

        # When
        schema_context = build_schema_context(metadata, self.answer_store, answer_ids_on_path)

        # Then
        self.assertEqual(schema_context['metadata']['trad_as'], r'&#34;trading name&#34;')

    def test_given_backslash_in_trading_name_when_create_context_then_backslash_are_escaped(self):
        # Given
        metadata = self.metadata.copy()
        metadata['trad_as'] = '\\trading name\\'

        answer_ids_on_path = []

        # When
        schema_context = build_schema_context(metadata, self.answer_store, answer_ids_on_path)

        # Then
        self.assertEqual(schema_context['metadata']['trad_as'], r'\\trading name\\')

    def test_given_quotes_in_ru_name_when_create_context_then_quotes_are_html_encoded(self):
        # Given
        metadata = self.metadata.copy()
        metadata['ru_name'] = '\"ru name\"'

        answer_ids_on_path = []

        # When
        schema_context = build_schema_context(metadata, self.answer_store, answer_ids_on_path)

        # Then
        self.assertEqual(schema_context['metadata']['ru_name'], r'&#34;ru name&#34;')

    def test_given_backslash_in_ru_name_when_create_context_then_backslash_are_escaped(self):
        # Given
        metadata = self.metadata.copy()
        metadata['ru_name'] = '\\ru name\\'

        answer_ids_on_path = []

        # When
        schema_context = build_schema_context(metadata, self.answer_store, answer_ids_on_path)

        # Then
        self.assertEqual(schema_context['metadata']['ru_name'], r'\\ru name\\')

    def test_given_quotes_in_ru_name_or_trading_name_when_create_context_then_quotes_are_html_encoded(self):
        # Given
        metadata = self.metadata.copy()
        metadata['ru_name'] = '\"ru_name\"'
        metadata['trad_as'] = None

        answer_ids_on_path = []

        # When
        schema_context = build_schema_context(metadata, self.answer_store, answer_ids_on_path)

        # Then
        self.assertEqual(schema_context['metadata']['trad_as_or_ru_name'], r'&#34;ru_name&#34;')

    def test_given_backslash_in_ru_name_or_trading_name_when_create_context_then_backslash_are_escaped(self):
        # Given
        metadata = self.metadata.copy()
        metadata['trad_as'] = '\\trading name\\'

        answer_ids_on_path = []

        # When
        schema_context = build_schema_context(metadata, self.answer_store, answer_ids_on_path)

        # Then
        self.assertEqual(schema_context['metadata']['trad_as_or_ru_name'], r'\\trading name\\')

    def test_given_quotes_in_answers_when_create_context_quotes_then_are_html_encoded(self):
        answers = [{
            'group_id': 'group1',
            'group_instance': 0,
            'block_id': 'block1',
            'answer_id': 'first_name',
            'answer_instance': 0,
            'value': '"',
        }]

        answer_ids_on_path = ['first_name']

        schema_context = build_schema_context(self.metadata, AnswerStore(answers), answer_ids_on_path)

        context_answers = schema_context['answers']
        self.assertEqual(len(context_answers), 1)
        self.assertEqual(context_answers['first_name'], r'&#34;')

    def test_given_backslash_in_answers_when_create_context_then_backslash_are_escaped(self):
        answers = [{
            'group_id': 'group1',
            'group_instance': 0,
            'block_id': 'block1',
            'answer_id': 'first_name',
            'answer_instance': 0,
            'value': '\\',
        }]

        answer_ids_on_path = ['first_name']

        schema_context = build_schema_context(self.metadata, AnswerStore(answers), answer_ids_on_path)

        context_answers = schema_context['answers']
        self.assertEqual(len(context_answers), 1)
        self.assertEqual(context_answers['first_name'], r'\\')

    def test_build_answers_excludes_answers_not_in_routing_path(self):
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

        schema_context = build_schema_context(self.metadata, AnswerStore(answers), answer_ids_on_path)

        context_answers = schema_context['answers']
        self.assertEqual(len(context_answers), 1)
        self.assertEqual(context_answers['first_name'], 'Joe')

    def test_build_answers_puts_answers_in_repeating_group_in_correct_index(self):
        """Tests that repeating answers get put in a padded list in the
        correct position
        """
        answers = [{
            'group_id': 'group1',
            'group_instance': 1,
            'block_id': 'block1',
            'answer_id': 'first_name',
            'answer_instance': 0,
            'value': 'Joe',
        }]

        answer_ids_on_path = ['first_name']
        self._get_answer_is_in_repeating_group.return_value = True
        schema_context = build_schema_context(self.metadata,
                                              AnswerStore(answers),
                                              answer_ids_on_path)

        context_answers = schema_context['answers']
        self.assertEqual(len(context_answers), 1)
        self.assertEqual(context_answers['first_name'], ['', 'Joe'])

    def test_build_answers_puts_repeating_answers_in_correct_index(self):
        """Tests that repeating answers get put in a padded list in the
        correct position
        """
        answers = [{
            'group_id': 'group1',
            'group_instance': 0,
            'block_id': 'block1',
            'answer_id': 'first_name',
            'answer_instance': 1,
            'value': 'Joe',
        }]

        answer_ids_on_path = ['first_name']
        self._get_is_repeating_answer.return_value = True
        schema_context = build_schema_context(self.metadata,
                                              AnswerStore(answers),
                                              answer_ids_on_path)

        context_answers = schema_context['answers']
        self.assertEqual(len(context_answers), 1)
        self.assertEqual(context_answers['first_name'], ['', 'Joe'])

    def test_build_answers_puts_answers_in_repeating_group(self):
        answers = [
            {
                'group_id': 'group1',
                'group_instance': 0,
                'block_id': 'block1',
                'answer_id': 'first_name',
                'answer_instance': 1,
                'value': 'Bloggs',
            }, {
                'group_id': 'group1',
                'group_instance': 0,
                'block_id': 'block1',
                'answer_id': 'first_name',
                'answer_instance': 0, # answer_instance deliberately in inverse order
                'value': 'Joe',
            }
        ]

        answer_ids_on_path = ['first_name']
        self._get_is_repeating_answer.return_value = True
        schema_context = build_schema_context(self.metadata,
                                              AnswerStore(answers),
                                              answer_ids_on_path)

        context_answers = schema_context['answers']
        self.assertEqual(len(context_answers), 1)
        self.assertEqual(context_answers['first_name'], ['Joe', 'Bloggs'])
