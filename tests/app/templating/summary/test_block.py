from unittest import TestCase

import mock

from app.templating.summary.block import Block


def build_block_schema(question_schema):
    block_schema = {
        'id': 'block_id',
        'title': 'A section title',
        'number': "1",
        'questions': question_schema
    }
    return block_schema


def build_question_schema(id, answer_schemas):
    return {'id': id, 'answers': answer_schemas, 'skipped': False, 'title': 'title', 'type': 'GENERAL'}


class TestSection(TestCase):

    def test_create_block(self):
        # Given

        answer_schema = mock.MagicMock()
        question_schema = build_question_schema('question_id', [answer_schema])
        block_schema = build_block_schema([question_schema])
        answers_map = mock.MagicMock()
        answer_store = mock.MagicMock()
        metadata = mock.MagicMock()
        url_for = mock.MagicMock()

        # When
        block = Block(block_schema, answers_map, 'group_id', answer_store, metadata, url_for)

        # Then
        self.assertEqual(block.id, 'block_id')
        self.assertEqual(block.title, 'A section title')
        self.assertEqual(block.number, "1")
        self.assertEqual(len(block.questions), 1)

    def test_create_section_with_multiple_questions(self):
        # Given
        first_answer_schema = mock.MagicMock()
        second_answer_schema = mock.MagicMock()
        first_question_schema = build_question_schema('question_1', [first_answer_schema])
        second_question_schema = build_question_schema('question_2', [second_answer_schema])
        block_schema = build_block_schema([first_question_schema, second_question_schema])
        answers_map = mock.MagicMock()
        answer_store = mock.MagicMock()
        metadata = mock.MagicMock()
        url_for = mock.MagicMock()

        # When
        block = Block(block_schema, answers_map, 'group_id', answer_store, metadata, url_for)

        # Then
        self.assertEqual(len(block.questions), 2)
