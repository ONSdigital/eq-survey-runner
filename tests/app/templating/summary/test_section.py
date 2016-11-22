from unittest import TestCase

import mock

from app.templating.summary.section import Section


def build_block_schema(answer_schema, id):
    question_schema = build_question_schema(id, [answer_schema])
    section_schema = {'id': 'section' + id, 'title': '', 'questions': [question_schema]}
    block_schema = {'id': id, 'sections': [section_schema]}
    return block_schema


def build_question_schema(id, answer_schemas):
    return {'id': id, 'answers': answer_schemas, 'skipped': False, 'title': 'title', 'type': 'GENERAL'}


class TestSection(TestCase):

    metadata = {
        'collection_exercise_sid': '789',
        'form_type': '0102',
        'eq_id': '1',
    }

    def test_create_section(self):
        # Given
        answers = mock.MagicMock()
        first_answer_schema = mock.MagicMock()
        question_schema = build_question_schema(1, [first_answer_schema])
        section_schema = {'id': 'section_id', 'title': 'A section title', 'questions': [question_schema]}

        # When
        section = Section(section_schema, answers, "some_link")

        # Then
        self.assertEqual(section.id, 'section_id')
        self.assertEqual(section.title, 'A section title')
        self.assertEqual(len(section.questions), 1)

    def test_create_section_with_multiple_questions(self):
        # Given
        answers = mock.MagicMock()
        first_answer_schema = mock.MagicMock()
        second_answer_schema = mock.MagicMock()
        first_question_schema = build_question_schema(1, [first_answer_schema])
        second_question_schema = build_question_schema(1, [second_answer_schema])
        section_schema = {'id': 'section_id', 'title': 'A section title', 'questions': [first_question_schema, second_question_schema]}

        # When
        section = Section(section_schema, answers, "some_link")

        # Then
        self.assertEqual(len(section.questions), 2)
