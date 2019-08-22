from unittest import TestCase
from mock import MagicMock, patch
from app.views.contexts.summary.block import Block
from app.questionnaire.location import Location


def build_block_schema(question_schema):
    block_schema = {
        'id': 'block_id',
        'title': 'A section title',
        'number': '1',
        'question': question_schema,
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
        self.list_store = MagicMock()
        self.metadata = MagicMock()
        self.schema = MagicMock()

    def test_create_block(self):
        # Given
        block_schema = build_block_schema({'id': 'mock_question_schema'})
        location = Location(section_id='a-section')

        # When
        with patch(
            'app.views.contexts.summary.block.Question',
            return_value=get_mock_question('A Question'),
        ), patch(
            'app.views.contexts.summary.block.url_for', return_value='http://a.url/'
        ):
            block = Block(
                block_schema,
                self.answer_store,
                self.list_store,
                self.metadata,
                self.schema,
                location
            )

        # Then
        self.assertEqual(block.id, 'block_id')
        self.assertEqual(block.title, 'A section title')
        self.assertEqual(block.number, '1')
        self.assertEqual(block.question, 'A Question')
