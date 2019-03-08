from unittest import TestCase
from mock import MagicMock, patch
from app.templating.summary.block import Block


def build_block_schema(question_schema):
    block_schema = {
        'id': 'block_id',
        'title': 'A section title',
        'number': '1',
        'questions': question_schema
    }
    return block_schema

def get_mock_question(placeholder):
    """Returns a mocked question, which returns `placeholder` from the serialize method"""
    question = MagicMock()
    question.serialize = MagicMock(return_value=placeholder)
    return question

class TestSection(TestCase):

    def setUp(self):
        self.answer_store = MagicMock()
        self.metadata = MagicMock()
        self.schema = MagicMock()

    def test_create_block(self):
        # Given
        block_schema = build_block_schema([{'id': 'mock_question_schema'}])

        # When
        with patch('app.templating.summary.block.Question', return_value=get_mock_question('A Question')), \
                patch('app.templating.summary.block.evaluate_skip_conditions', return_value=False), \
                patch('app.templating.summary.block.url_for', return_value='http://a.url/'):
            block = Block(block_schema, self.answer_store, self.metadata, self.schema)

        # Then
        self.assertEqual(block.id, 'block_id')
        self.assertEqual(block.title, 'A section title')
        self.assertEqual(block.number, '1')
        self.assertEqual(len(block.questions), 1)
        self.assertEqual(block.questions[0], 'A Question')

    def test_create_section_with_multiple_questions(self):
        # Given
        block_schema = build_block_schema([{'id': 'mock_question_schema'}, {'id': 'mock_question_schema'}])

        # When
        with patch('app.templating.summary.block.Question',
                   side_effect=[get_mock_question('A Question'), get_mock_question('A Second Question')]), \
                patch('app.templating.summary.block.evaluate_skip_conditions', return_value=False), \
                patch('app.templating.summary.block.url_for', return_value='http://a.url/'):
            block = Block(block_schema, self.answer_store, self.metadata, self.schema)

        # Then
        self.assertEqual(len(block.questions), 2)
        self.assertEqual(block.questions[0], 'A Question')
        self.assertEqual(block.questions[1], 'A Second Question')

    def test_question_should_be_skipped(self):
        # Given
        block_schema = build_block_schema([
            {'id': 'mock_question_schema', 'skip_conditions': 'mocked'},
            {'id': 'mock_question_schema'}
        ])

        with patch('app.templating.summary.block.Question',
                   side_effect=[get_mock_question('A Second Question')]) as patched_question_context, \
                patch('app.templating.summary.block.evaluate_skip_conditions', side_effect=[False, True]), \
                patch('app.templating.summary.block.url_for', return_value='http://a.url/'):
            # When
            block = Block(block_schema, self.answer_store, self.metadata, self.schema)

        # Then
        patched_question_context.assert_called_once()
        self.assertTrue(len(block.questions) == 1)
        self.assertEqual(block.questions[0], 'A Second Question')
