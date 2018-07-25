from unittest import TestCase
from mock import MagicMock, patch
from app.data_model.answer_store import AnswerStore, Answer
from app.templating.schema_context import build_schema_context, _build_answers, build_schema_metadata
from app.utilities.schema import _load_schema_file
from app.questionnaire.questionnaire_schema import QuestionnaireSchema, DEFAULT_LANGUAGE_CODE


def get_metadata_sample():
    """Returns a metadata sample"""
    return {
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


def get_test_schema():
    test_json = _load_schema_file('test_schema_context.json', DEFAULT_LANGUAGE_CODE)
    schema = QuestionnaireSchema(test_json, DEFAULT_LANGUAGE_CODE)

    schema.is_repeating_answer_type = MagicMock(return_value=False)
    schema.answer_is_in_repeating_group = MagicMock(return_value=False)
    return schema


class TestBuildSchemaContext(TestCase):  # pylint: disable=too-many-public-methods

    def setUp(self):
        self.answer_store = AnswerStore()
        self.metadata = get_metadata_sample()
        self.schema = get_test_schema()

    def test_build_schema_context(self):
        # Given
        with patch('app.templating.schema_context.build_schema_metadata', return_value='schema_metadata'), \
                patch('app.templating.schema_context._build_answers', return_value='answer_context'):
            # When
            schema_context = build_schema_context(self.metadata, self.schema, self.answer_store, [])

        # Then
        self.assertIn('metadata', schema_context)
        self.assertEqual(schema_context['metadata'], 'schema_metadata')
        self.assertIn('answers', schema_context)
        self.assertEqual(schema_context['answers'], 'answer_context')


class TestBuildAnswersContext(TestCase):

    def setUp(self):
        self.answer_store = AnswerStore()
        self.metadata = get_metadata_sample()
        self.schema = get_test_schema()

    def test_build_answers(self):
        # Given
        self.answer_store.add(Answer(
            answer_id='first_name',
            value='Joe Bloggs',
        ))
        answer_ids_on_path = ['first_name']

        # When
        context_answers = _build_answers(self.answer_store, self.schema, answer_ids_on_path)

        # Then
        self.assertEqual(len(context_answers), 1)
        self.assertEqual(context_answers['first_name'], 'Joe Bloggs')

    def test_build_answers_context_repeating_answers(self):
        # Given
        self.answer_store.add(Answer(
            answer_id='full_name_answer',
            value='Person One',
        ))
        self.answer_store.add(Answer(
            answer_id='full_name_answer',
            value='Person Two',
            answer_instance=1,
        ))
        self.answer_store.add(Answer(
            answer_id='full_name_answer',
            value='Person One',
            answer_instance=2
        ))
        answer_ids_on_path = ['full_name_answer']

        # When
        self.schema.is_repeating_answer_type = MagicMock(return_value=True)
        context_answers = _build_answers(self.answer_store, self.schema, answer_ids_on_path)

        # Then
        self.assertIsInstance(context_answers['full_name_answer'], list)
        self.assertEqual(len(context_answers['full_name_answer']), 3)
        self.assertEqual(len(context_answers), 1)

    def test_build_answers_single_answer_should_not_return_list(self):
        # Given
        self.answer_store.add(Answer(
            answer_id='full_name_answer',
            value='Person One',
        ))
        answer_ids_on_path = ['full_name_answer']

        # When
        context_answers = _build_answers(self.answer_store, self.schema, answer_ids_on_path)

        # Then
        self.assertEqual(len(context_answers), 1)
        self.assertEqual(context_answers['full_name_answer'], 'Person One')

    def test_build_answers_alias_for_repeating_answer_returns_list(self):
        # Given
        self.answer_store.add(Answer(
            answer_id='repeating_answer_id',
            value='Some Value',
        ))
        answer_ids_on_path = ['repeating_answer_id']

        # When
        self.schema.is_repeating_answer_type = MagicMock(return_value=True)
        context_answers = _build_answers(self.answer_store, self.schema, answer_ids_on_path)

        # Then
        self.assertIsInstance(context_answers['repeating_answer_id'], list)

    def test_alias_for_non_repeating_answer_returns_string(self):
        # Given
        self.answer_store.add(Answer(
            answer_id='non_repeating_answer_id',
            value='Some Value',
        ))
        answer_ids_on_path = ['non_repeating_answer_id']

        # When
        context_answers = _build_answers(self.answer_store, self.schema, answer_ids_on_path)

        # Then
        self.assertIsInstance(context_answers['non_repeating_answer_id'], str)
        self.assertEqual(context_answers['non_repeating_answer_id'], 'Some Value')

    def test_alias_for_answer_in_repeating_group_returns_list(self):
        # Given
        self.answer_store.add(Answer(
            answer_id='answer_id',
            value='Some Value',
        ))
        answer_ids_on_path = ['answer_id']

        # When
        self.schema.is_repeating_answer_type = MagicMock(return_value=True)
        context_answers = _build_answers(self.answer_store, self.schema, answer_ids_on_path)

        # Then
        self.assertIsInstance(context_answers['answer_id'], list)

    def test_maximum_answers_must_be_limited_to_system_max(self):
        # Given
        for instance in range(26):
            self.answer_store.add(Answer(
                answer_id='repeating_answer_id',
                value='Some Value',
                answer_instance=instance,
            ))
        answer_ids_on_path = ['repeating_answer_id']

        # When
        self.schema.is_repeating_answer_type = MagicMock(return_value=True)
        context_answers = _build_answers(self.answer_store, self.schema, answer_ids_on_path)

        # Then
        print(context_answers)
        self.assertEqual(len(context_answers['repeating_answer_id']), 25)

    def test_given_quotes_in_answers_when_create_context_quotes_then_are_html_encoded(self):
        # Given
        self.answer_store.add(Answer(
            answer_id='first_name',
            value='"'
        ))
        answer_ids_on_path = ['first_name']

        # When
        context_answers = _build_answers(self.answer_store, self.schema, answer_ids_on_path)

        # Then
        self.assertEqual(len(context_answers), 1)
        self.assertEqual(context_answers['first_name'], r'&#34;')

    def test_given_backslash_in_answers_when_create_context_then_backslash_are_escaped(self):
        # Given
        self.answer_store.add(Answer(
            answer_id='first_name',
            value='\\'
        ))
        answer_ids_on_path = ['first_name']

        # When
        context_answers = _build_answers(self.answer_store, self.schema, answer_ids_on_path)

        # Then
        self.assertEqual(len(context_answers), 1)
        self.assertEqual(context_answers['first_name'], r'\\')

    def test_build_answers_excludes_answers_not_in_routing_path(self):
        # Given
        self.answer_store.add(Answer(
            answer_id='first_name',
            value='Joe',
        ))
        self.answer_store.add(Answer(
            answer_id='lastname',
            value='Bloggs',
        ))
        answer_ids_on_path = ['first_name']

        # When
        context_answers = _build_answers(self.answer_store, self.schema, answer_ids_on_path)

        # Then
        self.assertEqual(len(context_answers), 1)
        self.assertEqual(context_answers['first_name'], 'Joe')

    def test_build_answers_puts_answers_in_repeating_group_in_correct_index(self):
        """Tests that repeating answers get put in a padded list in the
        correct position
        """
        # Given
        self.answer_store.add(Answer(
            answer_id='first_name',
            value='Joe',
            group_instance=1,
        ))
        answer_ids_on_path = ['first_name']

        # When
        self.schema.answer_is_in_repeating_group = MagicMock(return_value=True)
        context_answers = _build_answers(self.answer_store, self.schema, answer_ids_on_path)

        # Then
        print(context_answers)
        self.assertEqual(len(context_answers), 1)
        self.assertEqual(context_answers['first_name'], ['', 'Joe'])

    def test_build_answers_puts_repeating_answers_in_correct_index(self):
        """Tests that repeating answers get put in a padded list in the
        correct position
        """
        # Given
        self.answer_store.add(Answer(
            answer_id='first_name',
            value='Joe',
            answer_instance=1,
        ))
        answer_ids_on_path = ['first_name']

        # When
        self.schema.is_repeating_answer_type = MagicMock(return_value=True)
        context_answers = _build_answers(self.answer_store, self.schema, answer_ids_on_path)

        # Then
        self.assertEqual(len(context_answers), 1)
        self.assertEqual(context_answers['first_name'], ['', 'Joe'])

    def test_build_answers_puts_answers_in_repeating_group(self):
        # Given
        self.answer_store.add(Answer(
            answer_id='first_name',
            value='Bloggs',
            answer_instance=1,
        ))
        self.answer_store.add(Answer(
            answer_id='first_name',
            value='Joe',
            answer_instance=0, # answer_instance deliberately in inverse order
        ))
        answer_ids_on_path = ['first_name']

        # When
        self.schema.is_repeating_answer_type = MagicMock(return_value=True)
        context_answers = _build_answers(self.answer_store, self.schema, answer_ids_on_path)

        # Then
        self.assertEqual(len(context_answers), 1)
        self.assertEqual(context_answers['first_name'], ['Joe', 'Bloggs'])


class TestBuildSchemaMetadata(TestCase):

    def setUp(self):
        self.metadata = get_metadata_sample()
        self.schema = get_test_schema()

    def test_build_schema_metadata(self):
        # When
        metadata_context = build_schema_metadata(self.metadata, self.schema)

        # Then
        self.assertEqual('2016-10-13', metadata_context['ref_p_start_date'])
        self.assertEqual('2016-10-14', metadata_context['ref_p_end_date'])
        self.assertEqual('201610', metadata_context['period_id'])
        self.assertEqual('2016-10-19', metadata_context['employment_date'])
        self.assertEqual('Steve', metadata_context['user_id'])

    def test_metadata_display_name_is_trad_as_when_trad_as_supplied(self):
        # Given

        # When
        metadata_context = build_schema_metadata(self.metadata, self.schema)

        # Then
        self.assertEqual(metadata_context['trad_as_or_ru_name'], self.metadata['trad_as'])

    def test_metadata_display_name_is_ru_name_as_when_trad_as_not_supplied(self):
        # Given
        self.metadata['trad_as'] = None

        # When
        metadata_context = build_schema_metadata(self.metadata, self.schema)

        # Then
        self.assertEqual(metadata_context['trad_as_or_ru_name'], self.metadata['ru_name'])

    def test_metadata_display_name_is_ru_name_as_when_trad_as_empty(self):
        # Given
        self.metadata['trad_as'] = ''

        # When
        metadata_context = build_schema_metadata(self.metadata, self.schema)

        # Then
        self.assertEqual(metadata_context['trad_as_or_ru_name'], self.metadata['ru_name'])

    def test_given_quotes_in_trading_name_when_create_context_then_quotes_are_html_encoded(self):
        # Given
        self.metadata['trad_as'] = '\"trading name\"'

        # When
        metadata_context = build_schema_metadata(self.metadata, self.schema)

        # Then
        self.assertEqual(metadata_context['trad_as'], r'&#34;trading name&#34;')

    def test_given_backslash_in_trading_name_when_create_context_then_backslash_are_escaped(self):
        # Given
        self.metadata['trad_as'] = '\\trading name\\'

        # When
        metadata_context = build_schema_metadata(self.metadata, self.schema)

        # Then
        self.assertEqual(metadata_context['trad_as'], r'\\trading name\\')

    def test_given_quotes_in_ru_name_when_create_context_then_quotes_are_html_encoded(self):
        # Given
        self.metadata['ru_name'] = '\"ru name\"'

        # When
        metadata_context = build_schema_metadata(self.metadata, self.schema)

        # Then
        self.assertEqual(metadata_context['ru_name'], r'&#34;ru name&#34;')

    def test_given_backslash_in_ru_name_when_create_context_then_backslash_are_escaped(self):
        # Given
        self.metadata['ru_name'] = '\\ru name\\'

        # When
        metadata_context = build_schema_metadata(self.metadata, self.schema)

        # Then
        self.assertEqual(metadata_context['ru_name'], r'\\ru name\\')

    def test_given_quotes_in_ru_name_or_trading_name_when_create_context_then_quotes_are_html_encoded(self):
        # Given
        self.metadata['ru_name'] = '\"ru_name\"'
        self.metadata['trad_as'] = None

        # When
        metadata_context = build_schema_metadata(self.metadata, self.schema)

        # Then
        self.assertEqual(metadata_context['trad_as_or_ru_name'], r'&#34;ru_name&#34;')

    def test_given_backslash_in_ru_name_or_trading_name_when_create_context_then_backslash_are_escaped(self):
        # Given
        self.metadata['trad_as'] = '\\trading name\\'

        # When
        metadata_context = build_schema_metadata(self.metadata, self.schema)

        # Then
        self.assertEqual(metadata_context['trad_as_or_ru_name'], r'\\trading name\\')
